"""Build the UX4G component registry from CSS/JS parsing and curated metadata."""

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ..config import (
    CACHE_DIR,
    CSS_FILES,
    FORCE_REBUILD_REGISTRY_CACHE,
    JS_FILES,
    METADATA_DIR,
    UX4G_VERSION,
)
from .css_parser import CSSParser
from .js_parser import JSParser
from .models import Component, ComponentRegistry, Token, Variant


class RegistryBuilder:
    """Build and manage the UX4G component registry."""

    def __init__(self):
        self.registry = ComponentRegistry()
        self._cache_file = CACHE_DIR / "registry_cache.json"
        # Bump when cache shape/derivation semantics change.
        self._cache_format_version = 3

    def build(
        self, use_cache: bool = True, force_rebuild: bool = False
    ) -> ComponentRegistry:
        """Build the registry from CSS/JS files and metadata."""
        source_fingerprint = self._compute_source_fingerprint()

        # Try to load from cache first
        if use_cache and not force_rebuild and self._cache_file.exists():
            try:
                return self._load_from_cache(source_fingerprint)
            except Exception:
                pass  # Fall through to rebuild

        # Load curated metadata first (component definitions)
        self._load_metadata()

        # Parse CSS files
        self._parse_css_files()

        # Parse JS files
        self._parse_js_files()

        # Extract tokens
        self._extract_tokens()

        # Save to cache
        if use_cache:
            self._save_to_cache(source_fingerprint)

        return self.registry

    def _tracked_source_files(self) -> list[Path]:
        """Return source files that influence the registry contents."""
        files = [
            METADATA_DIR / "components.yaml",
            *CSS_FILES.values(),
            *JS_FILES.values(),
        ]
        # De-duplicate while preserving deterministic ordering by path string.
        unique = {str(path): path for path in files}
        return [unique[key] for key in sorted(unique)]

    def _file_sha256(self, path: Path) -> str:
        """Compute SHA-256 checksum for a source file."""
        digest = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _compute_source_fingerprint(self) -> dict[str, Any]:
        """
        Build a fingerprint from source metadata/content.

        Includes cache/version metadata plus each source file's mtime, size,
        and content hash so cache reuse is invalidated on changes.
        """
        sources: list[dict[str, Any]] = []
        for path in self._tracked_source_files():
            source_entry: dict[str, Any] = {"path": str(path)}
            if path.exists():
                stat = path.stat()
                source_entry["mtime_ns"] = stat.st_mtime_ns
                source_entry["size"] = stat.st_size
                source_entry["sha256"] = self._file_sha256(path)
            else:
                source_entry["missing"] = True
            sources.append(source_entry)

        fingerprint = {
            "cache_format_version": self._cache_format_version,
            "ux4g_version": UX4G_VERSION,
            "sources": sources,
        }
        canonical = json.dumps(fingerprint, sort_keys=True, separators=(",", ":"))
        fingerprint["digest"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return fingerprint

    def _load_metadata(self):
        """Load curated component metadata from YAML/JSON files."""
        metadata_file = METADATA_DIR / "components.yaml"
        if not metadata_file.exists():
            # Create default metadata if it doesn't exist
            self._create_default_metadata()
            return

        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f) or {}

        for comp_data in metadata.get("components", []):
            component = self._component_from_metadata(comp_data)
            self.registry.components[component.id] = component

    def _component_from_metadata(self, data: dict) -> Component:
        """Create Component from metadata dict."""
        variants = []
        for var_data in data.get("variants", []):
            variants.append(
                Variant(
                    name=var_data.get("name", ""),
                    class_list=var_data.get("class_list", []),
                    additional_attributes=var_data.get("additional_attributes", {}),
                    description=var_data.get("description"),
                    snippet_html=var_data.get("snippet_html"),
                    snippet_react=var_data.get("snippet_react"),
                )
            )

        return Component(
            id=data.get("id", ""),
            name=data.get("name", ""),
            category=data.get("category", "component"),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            default_markup_skeleton=data.get("default_markup_skeleton"),
            variants=variants,
            requires_js=data.get("requires_js", False),
            js_initialization=data.get("js_initialization"),
            required_classes=data.get("required_classes", []),
            required_attributes=data.get("required_attributes", {}),
            aria_roles=data.get("aria_roles", []),
            dependencies=data.get("dependencies", []),
            supported_frameworks=data.get("supported_frameworks", ["html", "react"]),
        )

    def _parse_css_files(self):
        """Parse all CSS files and update component classes."""
        all_classes = {}
        all_tokens = {}
        all_css_vars = {}

        for name, css_file in CSS_FILES.items():
            parser = CSSParser(css_file)
            classes, tokens, css_vars = parser.parse()
            all_classes.update(classes)
            all_tokens.update(tokens)
            all_css_vars.update(css_vars)

        # Update components with discovered classes
        for comp_id, component in self.registry.components.items():
            if comp_id in all_classes:
                # Merge discovered classes with existing
                existing_classes = set(component.required_classes)
                discovered_classes = set(all_classes[comp_id])
                component.required_classes = sorted(
                    list(existing_classes | discovered_classes)
                )

    def _parse_js_files(self):
        """Parse JS files and update component JS requirements."""
        js_info = {}

        for name, js_file in JS_FILES.items():
            parser = JSParser(js_file)
            components = parser.parse()
            js_info.update(components)

        # Update components with JS info
        for comp_id, component in self.registry.components.items():
            comp_key = comp_id.lower()
            if comp_key in js_info:
                info = js_info[comp_key]
                component.requires_js = True
                if info.get("init_pattern"):
                    component.js_initialization = info["init_pattern"]
                if info.get("data_attributes"):
                    for attr in info["data_attributes"]:
                        if attr not in component.required_attributes:
                            component.required_attributes[attr] = ""

    def _extract_tokens(self):
        """Extract design tokens from CSS variables."""
        # Parse main CSS for variables
        parser = CSSParser(CSS_FILES["main"])
        _, tokens, css_vars = parser.parse()

        # Create Token objects
        for token_type, token_dict in tokens.items():
            for name, value in token_dict.items():
                token_id = f"{token_type}_{name}"
                self.registry.tokens[token_id] = Token(
                    name=name,
                    token_type=token_type,
                    value=value,
                    css_variable=f"--{name}" if not name.startswith("--") else name,
                )

        # Add breakpoints from grid CSS
        self._extract_breakpoints()

    def _extract_breakpoints(self):
        """Extract breakpoint tokens from grid CSS."""
        grid_file = CSS_FILES.get("grid")
        if grid_file and grid_file.exists():
            content = grid_file.read_text(encoding="utf-8")
            # Common breakpoint pattern: @media (min-width: XXXpx)
            breakpoint_pattern = r"@media\s*\(min-width:\s*(\d+)px\)"
            breakpoints = {}
            for match in re.finditer(breakpoint_pattern, content):
                value = match.group(1)
                # Try to infer name from context
                breakpoints[f"breakpoint_{value}"] = value

            for name, value in breakpoints.items():
                self.registry.tokens[name] = Token(
                    name=name,
                    token_type="breakpoint",
                    value=f"{value}px",
                )

    def _create_default_metadata(self):
        """Create default component metadata if none exists."""
        METADATA_DIR.mkdir(parents=True, exist_ok=True)

        # Basic component definitions based on UX4G structure
        default_components = {
            "components": [
                {
                    "id": "button",
                    "name": "Button",
                    "category": "component",
                    "description": "UX4G button component with multiple variants",
                    "tags": ["form", "action", "interactive"],
                    "requires_js": False,
                    "required_classes": ["btn"],
                    "variants": [
                        {
                            "name": "primary",
                            "class_list": ["btn", "btn-primary"],
                        },
                        {
                            "name": "secondary",
                            "class_list": ["btn", "btn-secondary"],
                        },
                        {
                            "name": "outline",
                            "class_list": ["btn", "btn-outline-primary"],
                        },
                    ],
                },
                {
                    "id": "card",
                    "name": "Card",
                    "category": "component",
                    "description": "Card component for displaying content",
                    "tags": ["layout", "content"],
                    "requires_js": False,
                    "required_classes": ["card"],
                },
                {
                    "id": "modal",
                    "name": "Modal",
                    "category": "component",
                    "description": "Modal dialog component",
                    "tags": ["dialog", "overlay"],
                    "requires_js": True,
                    "required_classes": ["modal"],
                },
            ]
        }

        metadata_file = METADATA_DIR / "components.yaml"
        with open(metadata_file, "w", encoding="utf-8") as f:
            yaml.dump(default_components, f, default_flow_style=False)

    def _save_to_cache(self, source_fingerprint: dict[str, Any]):
        """Save registry to cache file."""
        cache_data = {
            "cache_format_version": self._cache_format_version,
            "source_fingerprint": source_fingerprint,
            "version": self.registry.version,
            "components": {
                comp_id: self._component_to_dict(comp)
                for comp_id, comp in self.registry.components.items()
            },
            "tokens": {
                token_id: {
                    "name": token.name,
                    "token_type": token.token_type,
                    "value": token.value,
                    "css_variable": token.css_variable,
                }
                for token_id, token in self.registry.tokens.items()
            },
        }
        with open(self._cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)

    def _load_from_cache(
        self, expected_source_fingerprint: dict[str, Any]
    ) -> ComponentRegistry:
        """Load registry from cache file."""
        with open(self._cache_file, "r", encoding="utf-8") as f:
            cache_data = json.load(f)

        if cache_data.get("cache_format_version") != self._cache_format_version:
            raise ValueError("Registry cache format/version mismatch")
        cached_fingerprint = cache_data.get("source_fingerprint")
        if not isinstance(cached_fingerprint, dict):
            raise ValueError("Registry source fingerprint missing")
        if cached_fingerprint.get("digest") != expected_source_fingerprint.get(
            "digest"
        ):
            raise ValueError("Registry source fingerprint mismatch")

        registry = ComponentRegistry(version=cache_data.get("version", "2.0.8"))

        # Load components
        for comp_id, comp_data in cache_data.get("components", {}).items():
            registry.components[comp_id] = self._component_from_dict(comp_data)

        # Load tokens
        for token_id, token_data in cache_data.get("tokens", {}).items():
            registry.tokens[token_id] = Token(**token_data)

        return registry

    def _component_to_dict(self, comp: Component) -> dict:
        """Convert Component to dict for caching."""
        return {
            "id": comp.id,
            "name": comp.name,
            "category": comp.category,
            "description": comp.description,
            "tags": comp.tags,
            "default_markup_skeleton": comp.default_markup_skeleton,
            "variants": [
                {
                    "name": v.name,
                    "class_list": v.class_list,
                    "additional_attributes": v.additional_attributes,
                    "description": v.description,
                    "snippet_html": getattr(v, "snippet_html", None),
                    "snippet_react": getattr(v, "snippet_react", None),
                }
                for v in comp.variants
            ],
            "requires_js": comp.requires_js,
            "js_initialization": comp.js_initialization,
            "required_classes": comp.required_classes,
            "required_attributes": comp.required_attributes,
            "aria_roles": comp.aria_roles,
            "dependencies": comp.dependencies,
            "supported_frameworks": comp.supported_frameworks,
        }

    def _component_from_dict(self, data: dict) -> Component:
        """Create Component from dict."""
        variants = [
            Variant(
                name=vd["name"],
                class_list=vd["class_list"],
                additional_attributes=vd.get("additional_attributes", {}),
                description=vd.get("description"),
                snippet_html=vd.get("snippet_html"),
                snippet_react=vd.get("snippet_react"),
            )
            for vd in data.get("variants", [])
        ]

        return Component(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            description=data["description"],
            tags=data.get("tags", []),
            default_markup_skeleton=data.get("default_markup_skeleton"),
            variants=variants,
            requires_js=data.get("requires_js", False),
            js_initialization=data.get("js_initialization"),
            required_classes=data.get("required_classes", []),
            required_attributes=data.get("required_attributes", {}),
            aria_roles=data.get("aria_roles", []),
            dependencies=data.get("dependencies", []),
            supported_frameworks=data.get("supported_frameworks", ["html", "react"]),
        )


# Global registry instance
_registry_instance: Optional[ComponentRegistry] = None


def get_registry(
    use_cache: bool = True, force_rebuild: bool | None = None
) -> ComponentRegistry:
    """Get or build the global registry instance."""
    global _registry_instance
    effective_force_rebuild = (
        FORCE_REBUILD_REGISTRY_CACHE if force_rebuild is None else force_rebuild
    )
    if _registry_instance is None or effective_force_rebuild:
        builder = RegistryBuilder()
        _registry_instance = builder.build(
            use_cache=use_cache,
            force_rebuild=effective_force_rebuild,
        )
    return _registry_instance

"""Component service for structured listing and component code retrieval."""
import re
from typing import Any

from ..config import CSS_FILES, JS_FILES
from ..registry import get_registry


class ComponentService:
    """Provide structured component catalog and usage payloads."""

    def __init__(self) -> None:
        self.registry = get_registry()

    def list_components(
        self,
        category: str | None = None,
        tag: str | None = None,
        requires_js: bool | None = None,
        layout_vs_component: str | None = None,
    ) -> dict[str, Any]:
        components = self.registry.list_components(
            category=category,
            tag=tag,
            requires_js=requires_js,
            layout_vs_component=layout_vs_component,
        )

        return {
            "total": len(components),
            "components": [self._component_metadata(comp.id) for comp in components],
        }

    def use_components(
        self,
        component_ids: list[str],
        framework: str = "html",
        include_css: bool = True,
        include_js: bool = True,
    ) -> dict[str, Any]:
        found: list[dict[str, Any]] = []
        missing: list[str] = []

        for component_id in component_ids:
            component = self.registry.get_component(component_id)
            if not component:
                missing.append(component_id)
                continue

            payload = self._component_metadata(component_id)
            payload["code"] = {
                "html": self.registry.get_snippet(component_id, None, "html") or "",
                "react": self.registry.get_snippet(component_id, None, "react") or "",
            }

            if framework == "react":
                payload["code"]["preferred"] = payload["code"]["react"]
            else:
                payload["code"]["preferred"] = payload["code"]["html"]

            payload["assets"] = {
                "css": self._collect_component_css(component_id) if include_css else "",
                "js": self._collect_component_js(component_id) if include_js else "",
            }
            found.append(payload)

        return {
            "requested_components": component_ids,
            "resolved_count": len(found),
            "missing_components": missing,
            "components": found,
        }

    def _component_metadata(self, component_id: str) -> dict[str, Any]:
        comp = self.registry.get_component(component_id)
        if not comp:
            return {}

        return {
            "id": comp.id,
            "name": comp.name,
            "category": comp.category,
            "description": comp.description,
            "tags": comp.tags,
            "requires_js": comp.requires_js,
            "supported_frameworks": comp.supported_frameworks,
            "required_classes": comp.required_classes,
            "required_attributes": comp.required_attributes,
            "aria_roles": comp.aria_roles,
            "dependencies": comp.dependencies,
            "variants": [
                {
                    "name": v.name,
                    "description": v.description,
                    "class_list": v.class_list,
                }
                for v in comp.variants
            ],
        }

    def _collect_component_css(self, component_id: str) -> str:
        comp = self.registry.get_component(component_id)
        if not comp:
            return ""

        selectors = set(comp.required_classes)
        for variant in comp.variants:
            selectors.update(variant.class_list)

        patterns = [re.compile(rf"\.{re.escape(s)}(?:[\s\.:#\[,{{]|$)") for s in selectors if s]
        matched_rules: list[str] = []

        for css_file in CSS_FILES.values():
            if not css_file.exists():
                continue
            content = css_file.read_text(encoding="utf-8", errors="ignore")
            blocks = content.split("}")
            for block in blocks:
                candidate = block.strip()
                if not candidate or "{" not in candidate:
                    continue
                if any(p.search(candidate) for p in patterns):
                    matched_rules.append(candidate + "}\n")

        # De-duplicate while preserving order
        deduped = list(dict.fromkeys(matched_rules))
        return "".join(deduped).strip()

    def _collect_component_js(self, component_id: str) -> str:
        comp = self.registry.get_component(component_id)
        if not comp:
            return ""

        chunks: list[str] = []

        if comp.js_initialization:
            chunks.append(f"// Initialization\n{comp.js_initialization};\n")

        # Pull constructor/static references from key JS files where possible.
        constructor_names = []
        if comp.js_initialization:
            constructor_names.extend(re.findall(r"new\s+([A-Za-z0-9_]+)", comp.js_initialization))

        for js_file in JS_FILES.values():
            if not js_file.exists():
                continue
            source = js_file.read_text(encoding="utf-8", errors="ignore")
            for ctor in constructor_names:
                class_pattern = re.compile(
                    rf"class\s+{re.escape(ctor)}\b.*?(?=\nclass\s+|\Z)",
                    re.DOTALL,
                )
                for match in class_pattern.finditer(source):
                    chunks.append(match.group(0).strip() + "\n")

        return "\n".join(dict.fromkeys(chunks)).strip()

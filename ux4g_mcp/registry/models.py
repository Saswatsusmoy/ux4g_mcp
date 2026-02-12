"""Data models for UX4G components and tokens."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Set, Literal


@dataclass
class Variant:
    """Component variant definition with optional direct snippets."""
    name: str
    class_list: List[str]
    additional_attributes: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None
    snippet_html: Optional[str] = None  # Full HTML snippet for this variant
    snippet_react: Optional[str] = None  # Full JSX snippet for this variant


@dataclass
class Component:
    """UX4G component definition."""
    id: str
    name: str
    category: str
    description: str
    tags: List[str] = field(default_factory=list)
    default_markup_skeleton: Optional[str] = None
    variants: List[Variant] = field(default_factory=list)
    requires_js: bool = False
    js_initialization: Optional[str] = None
    required_classes: List[str] = field(default_factory=list)
    required_attributes: Dict[str, str] = field(default_factory=dict)
    aria_roles: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # CSS/JS file dependencies
    supported_frameworks: List[Literal["html", "react"]] = field(
        default_factory=lambda: ["html", "react"]
    )


@dataclass
class Token:
    """Design token definition."""
    name: str
    token_type: Literal["color", "spacing", "typography", "breakpoint", "radius", "other"]
    value: str
    css_variable: Optional[str] = None
    css_class: Optional[str] = None
    description: Optional[str] = None
    usage_examples: List[str] = field(default_factory=list)


@dataclass
class ComponentRegistry:
    """Main registry holding all components and tokens."""
    components: Dict[str, Component] = field(default_factory=dict)
    tokens: Dict[str, Token] = field(default_factory=dict)
    version: str = "2.0.8"

    def get_component(self, component_id: str) -> Optional[Component]:
        """Get component by ID."""
        return self.components.get(component_id)

    def list_components(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        requires_js: Optional[bool] = None,
        layout_vs_component: Optional[str] = None,
    ) -> List[Component]:
        """List components with optional filters."""
        result = list(self.components.values())

        if category:
            result = [c for c in result if c.category == category]

        if tag:
            result = [c for c in result if tag in c.tags]

        if requires_js is not None:
            result = [c for c in result if c.requires_js == requires_js]

        if layout_vs_component:
            if layout_vs_component == "layout":
                result = [c for c in result if c.category == "layout"]
            elif layout_vs_component == "component":
                result = [c for c in result if c.category != "layout"]

        return result

    def get_tokens(self, token_type: Optional[str] = None) -> List[Token]:
        """Get tokens, optionally filtered by type."""
        result = list(self.tokens.values())
        if token_type and token_type != "all":
            result = [t for t in result if t.token_type == token_type]
        return result

    def get_snippet(
        self,
        component_id: str,
        variant_name: Optional[str] = None,
        framework: str = "html",
    ) -> Optional[str]:
        """
        Return the full snippet code for a component (no paths).
        Direct access: returns the actual HTML or JSX string to use as-is.
        """
        comp = self.get_component(component_id)
        if not comp:
            return None

        # Resolve variant
        variant = None
        if variant_name:
            variant = next((v for v in comp.variants if v.name == variant_name), None)
        if not variant and comp.variants:
            variant = comp.variants[0]

        # Prefer stored direct snippet per variant
        if variant:
            if framework == "react" and getattr(variant, "snippet_react", None):
                return variant.snippet_react
            if framework == "html" and getattr(variant, "snippet_html", None):
                return variant.snippet_html

        # Build from skeleton + variant classes
        markup = comp.default_markup_skeleton or ""
        if not markup.strip():
            base = " ".join(comp.required_classes) if comp.required_classes else comp.id
            markup = f'<div class="{base}">Content</div>'

        if variant:
            variant_classes = " ".join(variant.class_list)
            if comp.required_classes:
                base_class = comp.required_classes[0]
                if base_class in markup:
                    markup = markup.replace(base_class, variant_classes, 1)
                else:
                    markup = markup.replace('class="', f'class="{variant_classes} ', 1)

        if framework == "react":
            markup = markup.replace('class="', 'className="')
            markup = markup.replace("class='", "className='")
            markup = markup.replace(' for="', ' htmlFor="')
            markup = markup.replace(" for='", " htmlFor='")

        return markup.strip()

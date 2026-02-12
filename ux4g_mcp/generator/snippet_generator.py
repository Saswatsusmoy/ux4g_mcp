"""Generate UX4G code snippets from natural language descriptions."""
import re
from typing import Dict, List, Optional
from ..registry import get_registry
from .page_templates import PageTemplates


class SnippetGenerator:
    """Generate UX4G-compliant code from descriptions."""

    def __init__(self):
        self.registry = get_registry()
        self.page_templates = PageTemplates()

    def generate(
        self,
        description: str,
        framework: str = "html",
        page_context: Optional[Dict] = None,
        validation_level: str = "relaxed",
    ) -> Dict:
        """Generate code snippet from description."""
        description_lower = description.lower()

        # Check for page-level patterns first
        page_type = self._detect_page_type(description_lower)
        if page_type:
            return self._generate_page(page_type, description, framework)

        # Step 1: Identify components mentioned in description
        components_to_use = self._identify_components(description_lower)
        layout_hints = self._extract_layout_hints(description_lower, page_context)

        # Step 2: Fetch canonical code snippet for each component from registry
        code_parts = []
        component_details = []

        # Add container if needed
        if layout_hints.get("container"):
            class_attr = "className" if framework == "react" else "class"
            code_parts.append(f'<div {class_attr}="container">')

        # For each identified component, get its canonical snippet
        for comp_info in components_to_use:
            comp = comp_info["component"]
            variant = comp_info.get("variant")
            props = comp_info.get("props", {})
            
            # Get canonical markup from component definition
            comp_code = self._get_component_snippet(
                comp,
                variant,
                props,
                framework,
            )
            
            code_parts.append(comp_code)
            
            component_details.append({
                "id": comp.id,
                "name": comp.name,
                "variant": variant,
                "markup_source": "registry",
            })

        # Close container if opened
        if layout_hints.get("container"):
            code_parts.append("</div>")

        code = "\n".join(code_parts)

        # STRICT: Remove any custom CSS - only UX4G utility classes allowed
        code = self._strip_custom_css(code)

        # Convert to React if needed
        if framework == "react":
            code = self._convert_to_react(code)

        # Collect dependencies
        dependencies = set()
        for comp_info in components_to_use:
            comp = comp_info["component"]
            dependencies.update(comp.dependencies)

        notes = self._generate_notes(components_to_use)
        notes.insert(0, f"Generated using {len(component_details)} component(s) from UX4G registry. Each component snippet was fetched from the canonical component definitions.")
        
        return {
            "code": code,
            "components_used": component_details,
            "dependencies": list(dependencies),
            "notes": notes,
        }

    def _detect_page_type(self, description: str) -> Optional[str]:
        """Detect if this is a page-level request."""
        landing_keywords = ["landing page", "homepage", "home page", "main page", "department", "government portal"]
        if any(kw in description for kw in landing_keywords):
            return "landing_page"
        return None

    def _generate_page(self, page_type: str, description: str, framework: str) -> Dict:
        """Generate a full page using templates - ONLY UX4G utility classes, NO custom CSS."""
        # Extract department/entity name from description
        dept_match = re.search(r"(?:for|of|department|ministry)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", description, re.IGNORECASE)
        dept_name = dept_match.group(1) if dept_match else "Department"
        
        title_match = re.search(r"(?:title|name)[:\s]+([A-Z][^\.]+)", description, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else f"{dept_name} Portal"

        if page_type == "landing_page":
            code = self.page_templates.landing_page(title, dept_name, framework)
        else:
            code = f"<!-- Page template for {page_type} not yet implemented -->"

        # STRICT: Remove any custom CSS - only UX4G utility classes allowed
        code = self._strip_custom_css(code)

        return {
            "code": code,
            "components_used": [{"id": "landing_page", "variant": None}],
            "dependencies": ["ux4g.min.css", "ux4g-grid.css", "ux4g.bundle.min.js"],
            "notes": [
                "Generated using ONLY UX4G design system utility classes",
                "NO custom CSS - all styling uses UX4G utility classes (bg-*, text-*, py-*, mb-*, etc.)",
                "Ensure UX4G CSS and JS files are loaded from CDN or local assets",
                "All components use canonical snippets from UX4G registry",
            ],
        }

    def _identify_components(self, description: str) -> List[Dict]:
        """Identify components from description - Step 1: List components."""
        components = []
        description_lower = description.lower()

        # Component keywords mapping
        component_keywords = {
            "button": ["button", "btn", "submit", "click"],
            "form": ["form", "input", "field", "textbox", "select", "dropdown"],
            "card": ["card", "panel", "box"],
            "modal": ["modal", "dialog", "popup"],
            "alert": ["alert", "message", "notification", "warning"],
            "table": ["table", "grid", "list", "data"],
            "nav": ["nav", "navigation", "menu", "tab", "navbar"],
            "badge": ["badge", "label", "tag"],
            "progress": ["progress", "loading", "bar"],
            "spinner": ["spinner", "loading", "wait"],
            "container": ["container", "layout", "page"],
            "grid": ["grid", "row", "column", "columns"],
        }

        for comp_id, keywords in component_keywords.items():
            if any(kw in description_lower for kw in keywords):
                comp = self.registry.get_component(comp_id)
                if comp:
                    variant = self._extract_variant(description_lower, comp)
                    props = self._extract_props(description_lower, comp_id)
                    components.append({
                        "component": comp,
                        "variant": variant,
                        "props": props,
                    })

        # If no components found, default to a simple container
        if not components:
            container_comp = self.registry.get_component("container")
            if container_comp:
                components.append({"component": container_comp})

        return components

    def _extract_variant(self, description: str, component) -> Optional[str]:
        """Extract variant from description."""
        variant_keywords = {
            "primary": ["primary", "main"],
            "secondary": ["secondary"],
            "success": ["success", "successful"],
            "danger": ["danger", "delete", "remove", "error"],
            "warning": ["warning", "warn"],
            "info": ["info", "information"],
            "outline": ["outline", "outlined"],
        }

        for variant_name, keywords in variant_keywords.items():
            if any(kw in description for kw in keywords):
                # Check if component has this variant
                if any(v.name == variant_name for v in component.variants):
                    return variant_name

        # Default to first variant if available
        if component.variants:
            return component.variants[0].name

        return None

    def _extract_props(self, description: str, component_id: str) -> Dict:
        """Extract component-specific props from description."""
        props = {}

        if component_id == "button":
            if "submit" in description:
                props["type"] = "submit"
            if "cancel" in description or "close" in description:
                props["text"] = "Cancel"

        if component_id == "form":
            # Extract field names
            field_patterns = [
                r"(\w+)\s+field",
                r"field\s+for\s+(\w+)",
                r"(\w+)\s+input",
            ]
            for pattern in field_patterns:
                matches = re.findall(pattern, description)
                if matches:
                    props["fields"] = matches

        return props

    def _extract_layout_hints(self, description: str, page_context: Optional[Dict]) -> Dict:
        """Extract layout hints from description and context."""
        hints = {
            "container": True,  # Default to using container
            "grid": False,
            "responsive": False,
        }

        description_lower = description.lower()

        if "two-column" in description_lower or "two column" in description_lower:
            hints["grid"] = True
            hints["columns"] = 2
        elif "three-column" in description_lower or "three column" in description_lower:
            hints["grid"] = True
            hints["columns"] = 3
        elif "grid" in description_lower:
            hints["grid"] = True

        if "responsive" in description_lower or "mobile" in description_lower:
            hints["responsive"] = True

        if page_context:
            hints.update(page_context)

        return hints

    def _get_component_snippet(
        self,
        component,
        variant: Optional[str],
        props: Dict,
        framework: str,
    ) -> str:
        """Get snippet directly from registry (single source of truth), then apply props/spacing."""
        markup = self.registry.get_snippet(component.id, variant, framework) or ""
        class_attr = "className" if framework == "react" else "class"

        if not markup.strip():
            variant_obj = next((v for v in component.variants if v.name == variant), None) if variant else None
            if not variant_obj and component.variants:
                variant_obj = component.variants[0]
            classes = " ".join(variant_obj.class_list) if variant_obj else (" ".join(component.required_classes) if component.required_classes else component.id)
            markup = f'<div {class_attr}="{classes}">Content</div>'

        if props:
            if "text" in props:
                markup = markup.replace("Button", props["text"])
                markup = markup.replace("button", props["text"].lower())
            if "type" in props:
                markup = markup.replace('type="button"', f'type="{props["type"]}"')

        if "mb-" not in markup and "my-" not in markup and component.id in ["card", "alert", "button"]:
            markup = markup.replace(f'{class_attr}="', f'{class_attr}="mb-3 ', 1)

        return markup

    def _strip_custom_css(self, code: str) -> str:
        """Remove any custom CSS - ensure only UX4G utility classes are used."""
        import re
        # Remove <style> blocks
        code = re.sub(r'<style[^>]*>.*?</style>', '', code, flags=re.DOTALL | re.IGNORECASE)
        # Remove inline style attributes
        code = re.sub(r'\s+style="[^"]*"', '', code)
        code = re.sub(r"\s+style='[^']*'", '', code)
        return code

    def _convert_to_react(self, code: str) -> str:
        """Convert HTML to React JSX."""
        code = code.replace('class="', 'className="')
        code = code.replace("class='", "className='")
        code = code.replace(' for="', ' htmlFor="')
        code = code.replace(" for='", " htmlFor='")
        return code

    def _generate_notes(self, components: List[Dict]) -> List[str]:
        """Generate helpful notes about the generated code."""
        notes = []
        for comp_info in components:
            comp = comp_info["component"]
            if comp.requires_js:
                notes.append(
                    f"Component '{comp.name}' requires JavaScript initialization. "
                    f"Ensure {', '.join(comp.dependencies) if comp.dependencies else 'ux4g.bundle.js'} is loaded."
                )
        return notes

    def refine(
        self,
        existing_code: str,
        change_request: str,
        framework: Optional[str] = None,
    ) -> Dict:
        """Refine existing code based on change request."""
        # Auto-detect framework
        if not framework:
            if "className=" in existing_code:
                framework = "react"
            else:
                framework = "html"

        change_lower = change_request.lower()

        # Simple refinement: convert to React if requested
        if "react" in change_lower and framework == "html":
            refined_code = self._convert_to_react(existing_code)
            return {
                "code": refined_code,
                "diff_summary": "Converted HTML to React JSX",
                "dependencies": [],
            }

        # Refinement: change button variants
        if "ghost" in change_lower or "outline" in change_lower:
            refined_code = existing_code.replace("btn-primary", "btn-outline-primary")
            refined_code = refined_code.replace("btn-secondary", "btn-outline-secondary")
            return {
                "code": refined_code,
                "diff_summary": "Changed buttons to outline/ghost variant",
                "dependencies": [],
            }

        # Default: return as-is with note
        return {
            "code": existing_code,
            "diff_summary": "No changes applied (refinement not implemented for this request)",
            "dependencies": [],
        }

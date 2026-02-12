"""Component-related tool implementations. Return direct code snippets (no paths)."""
import json
from ..registry import get_registry


def _component_summary(registry, comp, include_snippet: bool = True, framework: str = "html"):
    """Build a structured component summary with optional inline snippet."""
    out = {
        "id": comp.id,
        "name": comp.name,
        "category": comp.category,
        "description": comp.description,
        "tags": comp.tags,
        "requires_js": comp.requires_js,
        "supported_frameworks": comp.supported_frameworks,
        "variants": [{"name": v.name, "description": v.description} for v in comp.variants],
    }
    if include_snippet:
        snippet = registry.get_snippet(comp.id, None, framework)
        if snippet:
            out["snippet"] = snippet
        if framework == "html":
            snippet_react = registry.get_snippet(comp.id, None, "react")
            if snippet_react and snippet_react != snippet:
                out["snippet_react"] = snippet_react
    return out


async def list_components_tool(arguments: dict) -> str:
    """List UX4G components with direct code snippets inline (no paths). Use the returned snippet as-is."""
    registry = get_registry()

    category = arguments.get("category")
    tag = arguments.get("tag")
    requires_js = arguments.get("requires_js")
    layout_vs_component = arguments.get("layout_vs_component")
    framework = arguments.get("framework", "html")

    components = registry.list_components(
        category=category,
        tag=tag,
        requires_js=requires_js,
        layout_vs_component=layout_vs_component,
    )

    result = []
    for comp in components:
        result.append(_component_summary(registry, comp, include_snippet=True, framework=framework))

    return json.dumps({"components": result}, indent=2)


async def get_component_tool(arguments: dict) -> str:
    """Get a UX4G component with full snippet code inline. No paths — use the returned snippet directly."""
    registry = get_registry()
    component_id = arguments.get("component_id")
    variant_name = arguments.get("variant")
    framework = arguments.get("framework", "html")

    if not component_id:
        return json.dumps({"error": "component_id is required"}, indent=2)

    component = registry.get_component(component_id)
    if not component:
        return json.dumps({"error": f"Component '{component_id}' not found"}, indent=2)

    if variant_name and not next((v for v in component.variants if v.name == variant_name), None):
        return json.dumps({
            "error": f"Variant '{variant_name}' not found for component '{component_id}'"
        }, indent=2)

    # Primary snippet: requested variant or default
    snippet = registry.get_snippet(component_id, variant_name, framework)
    result = {
        "id": component.id,
        "name": component.name,
        "category": component.category,
        "description": component.description,
        "tags": component.tags,
        "requires_js": component.requires_js,
        "supported_frameworks": component.supported_frameworks,
        "dependencies": component.dependencies,
        "required_attributes": component.required_attributes or {},
        "aria_roles": component.aria_roles or [],
        "snippet": snippet or "",
    }

    # All variants with their snippets (direct code for each)
    result["variants"] = []
    for v in component.variants:
        v_snippet_html = registry.get_snippet(component_id, v.name, "html")
        v_snippet_react = registry.get_snippet(component_id, v.name, "react")
        result["variants"].append({
            "name": v.name,
            "description": v.description,
            "class_list": v.class_list,
            "snippet": v_snippet_html or "",
            "snippet_react": v_snippet_react or "",
        })

    if component.requires_js and component.js_initialization:
        result["js_initialization"] = component.js_initialization
        result["usage_notes"] = f"Requires JS: {component.js_initialization}"

    return json.dumps(result, indent=2)

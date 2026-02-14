"""Component-oriented MCP tools."""
import json

from ..services import ComponentService


async def list_components_tool(arguments: dict) -> str:
    """Return component catalog in a strict JSON structure."""
    service = ComponentService()
    result = service.list_components(
        category=arguments.get("category"),
        tag=arguments.get("tag"),
        requires_js=arguments.get("requires_js"),
        layout_vs_component=arguments.get("layout_vs_component"),
    )
    return json.dumps(result, indent=2)


async def use_component_tool(arguments: dict) -> str:
    """
    Return metadata plus code payload (HTML/React/CSS/JS) for selected components.
    Expects `component_ids` as a list populated by the agent after `list_components`.
    """
    component_ids = arguments.get("component_ids") or []
    framework = arguments.get("framework", "html")
    include_css = arguments.get("include_css", True)
    include_js = arguments.get("include_js", True)

    if not isinstance(component_ids, list) or not component_ids:
        return json.dumps(
            {"error": "component_ids must be a non-empty array of component IDs"},
            indent=2,
        )

    service = ComponentService()
    result = service.use_components(
        component_ids=component_ids,
        framework=framework,
        include_css=include_css,
        include_js=include_js,
    )
    return json.dumps(result, indent=2)

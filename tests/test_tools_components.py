import asyncio
import json

from ux4g_mcp.tools.components import list_components_tool, use_component_tool


def test_list_components_tool_returns_structure():
    result = asyncio.run(list_components_tool({}))
    data = json.loads(result)

    assert "total" in data
    assert "components" in data
    assert isinstance(data["components"], list)
    if data["components"]:
        sample = data["components"][0]
        assert "id" in sample
        assert "name" in sample


def test_use_component_tool_returns_payload():
    result = asyncio.run(
        use_component_tool({"component_ids": ["button"], "framework": "react"})
    )
    data = json.loads(result)

    assert data["resolved_count"] == 1
    assert data["missing_components"] == []
    component = data["components"][0]
    assert component["id"] == "button"
    assert "code" in component
    assert "preferred" in component["code"]
    assert "className=" in component["code"]["preferred"]

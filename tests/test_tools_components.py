import asyncio
import json

from ux4g_mcp.tools.components import get_component_tool


def test_get_component_tool_returns_snippet():
    result = asyncio.run(get_component_tool({"component_id": "button", "framework": "html"}))
    data = json.loads(result)

    assert data["id"] == "button"
    assert "<button" in data["snippet"]
    assert any(variant["name"] == "primary" for variant in data["variants"])

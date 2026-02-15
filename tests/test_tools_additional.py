import asyncio
import json

from ux4g_mcp.tools.best_practices import get_bestpractices_tool
from ux4g_mcp.tools.generation import generate_snippet_tool, refine_snippet_tool
from ux4g_mcp.tools.tokens import list_tokens_tool
from ux4g_mcp.tools.version import get_version_tool


def test_get_version_tool_shape():
    result = asyncio.run(get_version_tool({}))
    data = json.loads(result)

    assert "version" in data
    assert "asset_root" in data
    assert "mcp_version" in data


def test_get_bestpractices_tool_shape():
    result = asyncio.run(get_bestpractices_tool({"limit": 1}))
    data = json.loads(result)

    assert "source" in data
    assert "result_count" in data
    assert "practices" in data
    assert isinstance(data["practices"], list)


def test_list_tokens_tool_shape():
    result = asyncio.run(list_tokens_tool({}))
    data = json.loads(result)

    assert "tokens" in data
    assert isinstance(data["tokens"], list)
    if data["tokens"]:
        token = data["tokens"][0]
        assert "name" in token
        assert "type" in token
        assert "value" in token


def test_generate_snippet_tool_shape():
    result = asyncio.run(generate_snippet_tool({"description": "primary button"}))
    data = json.loads(result)

    assert "code" in data
    assert "components_used" in data
    assert isinstance(data["components_used"], list)
    assert "notes" in data


def test_refine_snippet_tool_shape():
    existing = '<button type="button" class="btn btn-primary">Button</button>'
    result = asyncio.run(
        refine_snippet_tool(
            {
                "existing_code": existing,
                "change_request": "make outline",
            }
        )
    )
    data = json.loads(result)

    assert "code" in data
    assert "diff_summary" in data
    assert "btn-outline-primary" in data["code"]

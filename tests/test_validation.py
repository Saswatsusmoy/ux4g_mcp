import asyncio
import json

from ux4g_mcp.tools.validation import validate_snippet_tool


def test_validate_snippet_warns_missing_button_variant():
    code = '<button class="btn">Click</button>'
    result = asyncio.run(validate_snippet_tool({"code": code}))
    data = json.loads(result)

    issue_codes = {issue["code"] for issue in data["issues"]}
    assert "MISSING_BUTTON_VARIANT" in issue_codes
    assert data["is_valid"] is True

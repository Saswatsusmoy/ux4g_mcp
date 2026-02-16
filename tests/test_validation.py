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


def test_validate_snippet_modal_with_id_has_no_missing_id_issue():
    code = """
    <div class="modal fade" id="exampleModal">
      <div class="modal-dialog">
        <div class="modal-content">Content</div>
      </div>
    </div>
    """
    result = asyncio.run(validate_snippet_tool({"code": code}))
    data = json.loads(result)

    issue_codes = {issue["code"] for issue in data["issues"]}
    assert "MISSING_MODAL_ID" not in issue_codes
    assert data["is_valid"] is True


def test_validate_snippet_modal_missing_id_reported_once():
    code = """
    <div class="modal">
      <div class="modal-dialog">
        <div class="modal-content">Content</div>
      </div>
    </div>
    """
    result = asyncio.run(validate_snippet_tool({"code": code}))
    data = json.loads(result)

    missing_modal_id_count = sum(
        1 for issue in data["issues"] if issue["code"] == "MISSING_MODAL_ID"
    )
    assert missing_modal_id_count == 1
    assert data["is_valid"] is False

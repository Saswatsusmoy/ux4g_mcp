import re

from ux4g_mcp.services.component_service import ComponentService
from ux4g_mcp.utils.jsx import html_to_jsx


def test_html_to_jsx_handles_void_boolean_style_and_fragments():
    jsx = html_to_jsx(
        '<input class="form-control" disabled style="width: 25%; background-color: red;">'
        '<span class="visually-hidden">Label</span>'
    )

    assert jsx.startswith("<>")
    assert 'className="form-control"' in jsx
    assert re.search(r"<input\b[^>]*\s/>", jsx)
    assert "disabled" in jsx
    assert "style={{" in jsx
    assert 'width: "25%"' in jsx
    assert 'backgroundColor: "red"' in jsx


def test_component_service_react_snippets_are_valid_jsx_for_form_modal_card():
    service = ComponentService()
    result = service.use_components(
        ["form", "modal", "card"],
        framework="react",
        include_css=False,
        include_js=False,
    )
    by_id = {component["id"]: component for component in result["components"]}

    form_code = by_id["form"]["code"]["preferred"]
    assert re.search(r"<input\b[^>]*\s/>", form_code)
    assert 'htmlFor="exampleInput"' in form_code
    assert 'for="exampleInput"' not in form_code
    assert 'class="' not in form_code

    modal_code = by_id["modal"]["code"]["preferred"]
    assert 'tabIndex="-1"' in modal_code
    assert 'class="' not in modal_code
    assert 'className="modal fade"' in modal_code

    card_code = by_id["card"]["code"]["preferred"]
    assert 'className="card"' in card_code
    assert 'class="' not in card_code

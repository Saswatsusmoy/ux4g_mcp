from ux4g_mcp.registry.js_parser import JSParser


def test_js_parser_scopes_data_attributes_per_component_constants_block(tmp_path):
    js = """
    /**
     * Constants
     */
    const SELECTOR_DATA_TOGGLE_BUTTON = '[data-bs-toggle="button"]';
    class Button extends BaseComponent {}
    EventHandler.on(document, 'click', SELECTOR_DATA_TOGGLE_BUTTON, event => {
      Button.getOrCreateInstance(event.target).toggle();
    });

    /**
     * Constants
     */
    const SELECTOR_DATA_TOGGLE_MODAL = '[data-bs-toggle="modal"]';
    const SELECTOR_DATA_TARGET_MODAL = '[data-bs-target="#exampleModal"]';
    class Modal extends BaseComponent {}
    EventHandler.on(document, 'click', SELECTOR_DATA_TOGGLE_MODAL, event => {
      Modal.getOrCreateInstance(event.target).show();
    });
    """
    js_file = tmp_path / "sample.js"
    js_file.write_text(js, encoding="utf-8")

    parser = JSParser(js_file)
    components = parser.parse()

    assert "button" in components
    assert "modal" in components

    button_attrs = set(components["button"]["data_attributes"])
    modal_attrs = set(components["modal"]["data_attributes"])

    assert button_attrs == {"data-bs-toggle"}
    assert modal_attrs == {"data-bs-target", "data-bs-toggle"}
    assert "data-bs-target" not in button_attrs


def test_js_parser_falls_back_to_class_bounds_without_constants_markers(tmp_path):
    js = """
    class Button extends BaseComponent {}
    const BUTTON_SELECTOR = '[data-bs-toggle="button"]';

    class Modal extends BaseComponent {}
    const MODAL_SELECTOR = '[data-bs-target="#exampleModal"]';
    """
    js_file = tmp_path / "fallback.js"
    js_file.write_text(js, encoding="utf-8")

    parser = JSParser(js_file)
    components = parser.parse()

    assert "button" in components
    assert "modal" in components
    assert set(components["button"]["data_attributes"]) == {"data-bs-toggle"}
    assert set(components["modal"]["data_attributes"]) == {"data-bs-target"}

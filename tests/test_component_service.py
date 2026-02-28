from ux4g_mcp.registry.models import Component, Variant
from ux4g_mcp.services.component_service import ComponentService


def test_use_components_prefers_react_and_respects_asset_flags():
    service = ComponentService()
    result = service.use_components(
        ["button"], framework="react", include_css=False, include_js=False
    )

    assert result["resolved_count"] == 1
    component = result["components"][0]
    assert component["id"] == "button"
    assert "className=" in component["code"]["preferred"]
    assert component["assets"]["css"] == ""
    assert component["assets"]["js"] == ""


def test_use_components_reports_missing():
    service = ComponentService()
    result = service.use_components(["does-not-exist"])

    assert result["resolved_count"] == 0
    assert "does-not-exist" in result["missing_components"]
    assert result["components"] == []


def test_list_components_filter_by_category():
    service = ComponentService()
    result = service.list_components(category="component")

    assert "components" in result
    assert isinstance(result["components"], list)
    if result["components"]:
        assert all(comp["category"] == "component" for comp in result["components"])


def test_collect_component_css_handles_nested_media_rules(monkeypatch, tmp_path):
    css = """
    .btn-primary { color: red; }
    @media (min-width: 768px) {
      .btn-primary { color: blue; }
      .other { display: block; }
    }
    """
    css_file = tmp_path / "component.css"
    css_file.write_text(css)
    monkeypatch.setattr(
        "ux4g_mcp.services.component_service.CSS_FILES",
        {"main": css_file},
    )

    component = Component(
        id="button",
        name="Button",
        category="component",
        description="Button",
        required_classes=["btn-primary"],
        variants=[Variant(name="primary", class_list=["btn-primary"])],
    )

    class FakeRegistry:
        def get_component(self, component_id):
            if component_id == "button":
                return component
            return None

    service = ComponentService()
    service.registry = FakeRegistry()

    extracted = service._collect_component_css("button")

    assert ".btn-primary" in extracted
    assert "@media (min-width: 768px)" in extracted
    assert ".other" not in extracted

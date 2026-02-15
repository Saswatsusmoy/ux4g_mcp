from ux4g_mcp.services.component_service import ComponentService


def test_use_components_prefers_react_and_respects_asset_flags():
    service = ComponentService()
    result = service.use_components(["button"], framework="react", include_css=False, include_js=False)

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

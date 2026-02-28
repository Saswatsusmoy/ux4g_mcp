from ux4g_mcp.registry.css_parser import CSSParser


def test_css_parser_extracts_tokens_and_classes(tmp_path):
    css = """
    :root {
      --primary-color: #123456;
      --spacing-1: 4px;
      --font-base: 16px;
      --border-radius-sm: 2px;
    }
    .btn-primary { color: var(--primary-color); }
    .card { border-radius: var(--border-radius-sm); }
    .mt-3 { margin-top: 1rem; }
    """
    css_file = tmp_path / "test.css"
    css_file.write_text(css)

    parser = CSSParser(css_file)
    classes, tokens, css_vars = parser.parse()

    assert "primary-color" in css_vars
    assert "color" in tokens and "primary-color" in tokens["color"]
    assert "spacing" in tokens and "spacing-1" in tokens["spacing"]
    assert "typography" in tokens and "font-base" in tokens["typography"]
    assert "radius" in tokens and "border-radius-sm" in tokens["radius"]

    assert "button" in classes and "btn-primary" in classes["button"]
    assert "card" in classes and "card" in classes["card"]


def test_css_parser_extracts_from_multiple_roots_and_utility_tokens(tmp_path):
    css = """
    :root { --space-1: 4px; --font-size-base: 16px; }
    :root { --space-2: 8px; --line-height-base: 1.5; }
    @media (min-width: 768px) {
      .px-4 { padding-left: 1.5rem; padding-right: 1.5rem; }
      .fs-1 { font-size: 2.5rem; }
    }
    """
    css_file = tmp_path / "tokens.css"
    css_file.write_text(css)

    parser = CSSParser(css_file)
    _, tokens, css_vars = parser.parse()

    assert "space-1" in css_vars
    assert "space-2" in css_vars
    assert "spacing" in tokens and "space-1" in tokens["spacing"]
    assert "spacing" in tokens and "px-4" in tokens["spacing"]
    assert "typography" in tokens and "font-size-base" in tokens["typography"]
    assert "typography" in tokens and "fs-1" in tokens["typography"]

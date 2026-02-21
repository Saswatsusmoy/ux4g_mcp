"""Utilities for converting HTML snippets to React JSX."""

from __future__ import annotations

from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype, NavigableString, Tag

_VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

_ATTR_ALIASES = {
    "class": "className",
    "classname": "className",
    "for": "htmlFor",
    "htmlfor": "htmlFor",
    "tabindex": "tabIndex",
    "readonly": "readOnly",
    "maxlength": "maxLength",
    "minlength": "minLength",
    "contenteditable": "contentEditable",
    "spellcheck": "spellCheck",
    "autocomplete": "autoComplete",
    "autofocus": "autoFocus",
    "srcset": "srcSet",
    "colspan": "colSpan",
    "rowspan": "rowSpan",
    "crossorigin": "crossOrigin",
    "referrerpolicy": "referrerPolicy",
    "allowfullscreen": "allowFullScreen",
    "http-equiv": "httpEquiv",
    "formnovalidate": "formNoValidate",
    "novalidate": "noValidate",
    "playsinline": "playsInline",
}

_BOOLEAN_ATTRS = {
    "allowfullscreen",
    "async",
    "autofocus",
    "autoplay",
    "checked",
    "controls",
    "default",
    "defer",
    "disabled",
    "formnovalidate",
    "hidden",
    "loop",
    "multiple",
    "muted",
    "novalidate",
    "open",
    "playsinline",
    "readonly",
    "required",
    "reversed",
    "selected",
    "allowFullScreen",
    "autoFocus",
    "formNoValidate",
    "noValidate",
    "playsInline",
    "readOnly",
}


def html_to_jsx(markup: str) -> str:
    """Convert HTML markup into React-compatible JSX."""
    if not markup or not markup.strip():
        return ""

    soup = BeautifulSoup(markup, "html.parser")
    rendered_nodes: list[str] = []
    for node in soup.contents:
        converted = _render_node(node, level=0)
        if converted:
            rendered_nodes.append(converted)

    if not rendered_nodes:
        return ""

    if len(rendered_nodes) == 1:
        return rendered_nodes[0].strip()

    return "<>\n" + "\n".join(rendered_nodes) + "\n</>"


def _render_node(node, level: int) -> str:
    indent = "  " * level

    if isinstance(node, (Comment, Doctype)):
        return ""

    if isinstance(node, NavigableString):
        text = str(node)
        if not text.strip():
            return ""
        return f"{indent}{text.strip()}"

    if not isinstance(node, Tag):
        return ""

    tag_name = node.name
    attrs = _render_attrs(node)

    if tag_name in _VOID_TAGS:
        return f"{indent}<{tag_name}{attrs} />"

    children = []
    for child in node.contents:
        rendered_child = _render_node(child, level + 1)
        if rendered_child:
            children.append(rendered_child)

    if not children:
        return f"{indent}<{tag_name}{attrs}></{tag_name}>"

    if len(children) == 1:
        child = children[0].strip()
        if not child.startswith("<"):
            return f"{indent}<{tag_name}{attrs}>{child}</{tag_name}>"

    return (
        f"{indent}<{tag_name}{attrs}>\n"
        + "\n".join(children)
        + f"\n{indent}</{tag_name}>"
    )


def _render_attrs(tag: Tag) -> str:
    rendered = []
    for raw_name, raw_value in tag.attrs.items():
        jsx_name = _to_jsx_attr_name(raw_name)

        if isinstance(raw_value, list):
            value = " ".join(str(v) for v in raw_value if v is not None).strip()
        else:
            value = raw_value

        if jsx_name == "style":
            style_expr = _style_to_jsx_expr(str(value or ""))
            if style_expr:
                rendered.append(f"style={style_expr}")
            continue

        if _is_boolean_attr(raw_name, jsx_name):
            rendered.append(_render_boolean_attr(jsx_name, value))
            continue

        if value is None:
            rendered.append(f'{jsx_name}=""')
            continue

        rendered.append(f'{jsx_name}="{_escape_attr_value(str(value))}"')

    if not rendered:
        return ""
    return " " + " ".join(rendered)


def _to_jsx_attr_name(attr_name: str) -> str:
    lower = attr_name.lower()
    if lower.startswith("data-") or lower.startswith("aria-"):
        return lower
    return _ATTR_ALIASES.get(lower, attr_name)


def _is_boolean_attr(raw_name: str, jsx_name: str) -> bool:
    return raw_name.lower() in _BOOLEAN_ATTRS or jsx_name in _BOOLEAN_ATTRS


def _render_boolean_attr(jsx_name: str, value) -> str:
    if value is False:
        return f"{jsx_name}={{false}}"
    if isinstance(value, str) and value.strip().lower() == "false":
        return f"{jsx_name}={{false}}"
    # Truthy/empty boolean attrs use JSX shorthand
    return jsx_name


def _escape_attr_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _style_to_jsx_expr(style: str) -> str:
    declarations = []
    for part in style.split(";"):
        if ":" not in part:
            continue
        prop, raw_value = part.split(":", 1)
        prop = prop.strip()
        raw_value = raw_value.strip()
        if not prop or not raw_value:
            continue

        if prop.startswith("--"):
            jsx_prop = f'"{prop}"'
        else:
            jsx_prop = _css_prop_to_camel(prop)

        declarations.append(f'{jsx_prop}: "{_escape_attr_value(raw_value)}"')

    if not declarations:
        return ""

    return "{{ " + ", ".join(declarations) + " }}"


def _css_prop_to_camel(prop: str) -> str:
    parts = [p for p in prop.split("-") if p]
    if not parts:
        return prop
    return parts[0] + "".join(part.capitalize() for part in parts[1:])

"""CSS parser for extracting UX4G classes and design tokens."""

import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import tinycss2


class CSSParser:
    """Parse CSS files to extract component classes and design tokens."""

    def __init__(self, css_file: Path):
        self.css_file = css_file
        self.classes: Dict[str, List[str]] = {}  # component -> list of classes
        self.tokens: Dict[str, Dict[str, str]] = {}  # token_type -> {name: value}
        self.css_variables: Dict[str, str] = {}  # var_name -> value

    def parse(
        self,
    ) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, str]], Dict[str, str]]:
        """Parse CSS file and return classes, tokens, and CSS variables."""
        if not self.css_file.exists():
            return {}, {}, {}

        content = self.css_file.read_text(encoding="utf-8")
        stylesheet = tinycss2.parse_stylesheet(
            content, skip_comments=True, skip_whitespace=True
        )

        # Extract CSS variables from all :root blocks in the stylesheet.
        self._extract_css_variables(stylesheet)

        # Extract component classes
        self._extract_component_classes(content)

        # Extract design tokens
        self._extract_tokens(stylesheet)

        return self.classes, self.tokens, self.css_variables

    def _iter_qualified_rules(self, rules: Iterable) -> Iterable:
        """Yield all qualified rules, recursively traversing nested at-rules."""
        for rule in rules:
            if rule.type == "qualified-rule":
                yield rule
            elif rule.type == "at-rule" and rule.content is not None:
                nested = tinycss2.parse_rule_list(
                    rule.content, skip_comments=True, skip_whitespace=True
                )
                yield from self._iter_qualified_rules(nested)

    def _rule_declarations(self, rule) -> list:
        """Return parsed declaration nodes for a qualified rule."""
        return [
            declaration
            for declaration in tinycss2.parse_declaration_list(
                rule.content, skip_comments=True, skip_whitespace=True
            )
            if declaration.type == "declaration"
        ]

    def _extract_css_variables(self, stylesheet) -> None:
        """Extract CSS custom properties from all :root selectors."""
        for rule in self._iter_qualified_rules(stylesheet):
            selector = tinycss2.serialize(rule.prelude).strip()
            if not selector:
                continue
            selectors = [s.strip() for s in selector.split(",")]
            if not any(":root" in s for s in selectors):
                continue
            for declaration in self._rule_declarations(rule):
                if not declaration.name.startswith("--"):
                    continue
                var_name = declaration.name[2:]
                var_value = tinycss2.serialize(declaration.value).strip()
                self.css_variables[var_name] = var_value

    def _extract_component_classes(self, content: str):
        """Extract component-related classes."""
        # Common UX4G component prefixes
        component_patterns = {
            "button": r"\.(btn|button)(?:-[-\w]+)?",
            "alert": r"\.alert(?:-[-\w]+)?",
            "badge": r"\.badge(?:-[-\w]+)?",
            "card": r"\.card(?:-[-\w]+)?",
            "modal": r"\.modal(?:-[-\w]+)?",
            "nav": r"\.nav(?:-[-\w]+)?",
            "navbar": r"\.navbar(?:-[-\w]+)?",
            "dropdown": r"\.dropdown(?:-[-\w]+)?",
            "form": r"\.(form|form-control|form-label|form-select|form-check)(?:-[-\w]+)?",
            "input": r"\.(input-group|form-control)(?:-[-\w]+)?",
            "table": r"\.table(?:-[-\w]+)?",
            "list": r"\.(list-group|list-group-item)(?:-[-\w]+)?",
            "breadcrumb": r"\.breadcrumb(?:-[-\w]+)?",
            "pagination": r"\.pagination(?:-[-\w]+)?",
            "progress": r"\.progress(?:-[-\w]+)?",
            "spinner": r"\.spinner(?:-[-\w]+)?",
            "toast": r"\.toast(?:-[-\w]+)?",
            "tooltip": r"\.tooltip(?:-[-\w]+)?",
            "popover": r"\.popover(?:-[-\w]+)?",
            "carousel": r"\.carousel(?:-[-\w]+)?",
            "collapse": r"\.collapse(?:-[-\w]+)?",
            "accordion": r"\.accordion(?:-[-\w]+)?",
            "offcanvas": r"\.offcanvas(?:-[-\w]+)?",
            "tab": r"\.(tab|nav-tabs)(?:-[-\w]+)?",
        }

        for component, pattern in component_patterns.items():
            classes = set()
            for match in re.finditer(pattern, content):
                class_name = match.group(0).lstrip(".")
                classes.add(class_name)
            if classes:
                self.classes[component] = sorted(list(classes))

        # Extract utility classes
        self._extract_utility_classes(content)

    def _extract_utility_classes(self, content: str):
        """Extract utility classes (spacing, colors, display, etc.)."""
        utilities = {
            "spacing": r"\.(m|p|mx|my|mt|mb|ml|mr|ms|me|px|py|pt|pb|pl|pr|ps|pe|g|gap)(?:-[-\w]+)?",
            "display": r"\.(d|display)(?:-[-\w]+)?",
            "position": r"\.(position|top|bottom|start|end)(?:-[-\w]+)?",
            "color": r"\.(text|bg|border)(?:-[-\w]+)?",
            "flex": r"\.(flex|justify|align|order)(?:-[-\w]+)?",
            "grid": r"\.(container|row|col)(?:-[-\w]+)?",
        }

        for util_type, pattern in utilities.items():
            classes = set()
            for match in re.finditer(pattern, content):
                class_name = match.group(0).lstrip(".")
                classes.add(class_name)
            if classes:
                if util_type not in self.classes:
                    self.classes[util_type] = []
                self.classes[util_type].extend(sorted(list(classes)))

    def _extract_spacing_tokens_from_utilities(self, stylesheet) -> Dict[str, str]:
        """Extract spacing token values from utility class rules."""
        spacing_selector_pattern = re.compile(
            r"\.(?:m|p|mx|my|mt|mb|ml|mr|ms|me|px|py|pt|pb|pl|pr|ps|pe|g|gap)-[A-Za-z0-9_-]+"
        )
        spacing_properties = {
            "margin",
            "margin-top",
            "margin-right",
            "margin-bottom",
            "margin-left",
            "padding",
            "padding-top",
            "padding-right",
            "padding-bottom",
            "padding-left",
            "gap",
            "row-gap",
            "column-gap",
        }

        spacing_tokens: Dict[str, str] = {}
        for rule in self._iter_qualified_rules(stylesheet):
            selector = tinycss2.serialize(rule.prelude).strip()
            if not selector or not spacing_selector_pattern.search(selector):
                continue

            class_names = {
                match.lstrip(".")
                for match in spacing_selector_pattern.findall(selector)
            }
            if not class_names:
                continue

            values: list[str] = []
            for declaration in self._rule_declarations(rule):
                if declaration.name not in spacing_properties:
                    continue
                value = tinycss2.serialize(declaration.value).strip()
                if value:
                    values.append(f"{declaration.name}: {value}")

            if not values:
                continue

            compact_value = "; ".join(values)
            for class_name in class_names:
                spacing_tokens[class_name] = compact_value

        return spacing_tokens

    def _extract_typography_tokens_from_utilities(self, stylesheet) -> Dict[str, str]:
        """Extract typography token values from utility class rules."""
        typography_selector_pattern = re.compile(r"\.(?:fs|fw|lh)-[A-Za-z0-9_-]+")
        typography_properties = {
            "font-family",
            "font-size",
            "font-weight",
            "line-height",
            "letter-spacing",
        }

        typography_tokens: Dict[str, str] = {}
        for rule in self._iter_qualified_rules(stylesheet):
            selector = tinycss2.serialize(rule.prelude).strip()
            if not selector or not typography_selector_pattern.search(selector):
                continue

            class_names = {
                match.lstrip(".")
                for match in typography_selector_pattern.findall(selector)
            }
            if not class_names:
                continue

            values: list[str] = []
            for declaration in self._rule_declarations(rule):
                if declaration.name not in typography_properties:
                    continue
                value = tinycss2.serialize(declaration.value).strip()
                if value:
                    values.append(f"{declaration.name}: {value}")

            if not values:
                continue

            compact_value = "; ".join(values)
            for class_name in class_names:
                typography_tokens[class_name] = compact_value

        return typography_tokens

    def _extract_tokens(self, stylesheet) -> None:
        """Extract design tokens from CSS variables."""
        # Colors
        color_vars = {
            k: v
            for k, v in self.css_variables.items()
            if any(
                x in k.lower()
                for x in [
                    "color",
                    "primary",
                    "secondary",
                    "success",
                    "danger",
                    "warning",
                    "info",
                    "blue",
                    "red",
                    "green",
                    "yellow",
                    "black",
                    "white",
                    "gray",
                    "grey",
                ]
            )
        }
        if color_vars:
            self.tokens["color"] = color_vars

        def is_spacing_variable(var_name: str) -> bool:
            name = var_name.lower()
            if any(
                key in name for key in ["spacing", "spacer", "gap", "margin", "padding"]
            ):
                return True
            return re.search(r"(^|[-_])space([-_]|$)", name) is not None

        # Spacing tokens from variables plus utility classes.
        spacing_vars = {
            k: v for k, v in self.css_variables.items() if is_spacing_variable(k)
        }
        spacing_vars.update(self._extract_spacing_tokens_from_utilities(stylesheet))
        if spacing_vars:
            self.tokens["spacing"] = spacing_vars

        # Typography tokens from variables plus typography utility classes.
        typo_vars = {
            k: v
            for k, v in self.css_variables.items()
            if any(
                x in k.lower()
                for x in [
                    "font",
                    "line-height",
                    "letter-spacing",
                    "typography",
                    "weight",
                    "size",
                ]
            )
        }
        typo_vars.update(self._extract_typography_tokens_from_utilities(stylesheet))
        if typo_vars:
            self.tokens["typography"] = typo_vars

        # Border radius
        radius_vars = {
            k: v
            for k, v in self.css_variables.items()
            if "radius" in k.lower() or "border-radius" in k.lower()
        }
        if radius_vars:
            self.tokens["radius"] = radius_vars

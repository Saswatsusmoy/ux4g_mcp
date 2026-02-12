"""CSS parser for extracting UX4G classes and design tokens."""
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import tinycss2


class CSSParser:
    """Parse CSS files to extract component classes and design tokens."""

    def __init__(self, css_file: Path):
        self.css_file = css_file
        self.classes: Dict[str, List[str]] = {}  # component -> list of classes
        self.tokens: Dict[str, Dict[str, str]] = {}  # token_type -> {name: value}
        self.css_variables: Dict[str, str] = {}  # var_name -> value

    def parse(self) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, str]], Dict[str, str]]:
        """Parse CSS file and return classes, tokens, and CSS variables."""
        if not self.css_file.exists():
            return {}, {}, {}

        content = self.css_file.read_text(encoding="utf-8")

        # Extract CSS variables from :root
        self._extract_css_variables(content)

        # Extract component classes
        self._extract_component_classes(content)

        # Extract design tokens
        self._extract_tokens(content)

        return self.classes, self.tokens, self.css_variables

    def _extract_css_variables(self, content: str):
        """Extract CSS custom properties from :root."""
        # Match :root { --var-name: value; }
        root_pattern = r":root\s*\{([^}]+)\}"
        root_match = re.search(root_pattern, content, re.DOTALL)
        if root_match:
            root_content = root_match.group(1)
            var_pattern = r"--([\w-]+):\s*([^;]+);"
            for match in re.finditer(var_pattern, root_content):
                var_name = match.group(1)
                var_value = match.group(2).strip()
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

    def _extract_tokens(self, content: str):
        """Extract design tokens from CSS variables."""
        # Colors
        color_vars = {
            k: v for k, v in self.css_variables.items()
            if any(x in k.lower() for x in ["color", "primary", "secondary", "success", "danger", "warning", "info", "blue", "red", "green", "yellow"])
        }
        if color_vars:
            self.tokens["color"] = color_vars

        # Spacing (from variables or utility classes)
        spacing_vars = {
            k: v for k, v in self.css_variables.items()
            if "spacing" in k.lower() or "gap" in k.lower()
        }
        if spacing_vars:
            self.tokens["spacing"] = spacing_vars

        # Typography
        typo_vars = {
            k: v for k, v in self.css_variables.items()
            if any(x in k.lower() for x in ["font", "line-height", "size", "weight"])
        }
        if typo_vars:
            self.tokens["typography"] = typo_vars

        # Border radius
        radius_vars = {
            k: v for k, v in self.css_variables.items()
            if "radius" in k.lower() or "border-radius" in k.lower()
        }
        if radius_vars:
            self.tokens["radius"] = radius_vars

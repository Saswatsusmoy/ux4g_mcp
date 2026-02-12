"""JavaScript parser for extracting UX4G component initialization patterns."""
import re
from pathlib import Path
from typing import Dict, List, Set, Optional


class JSParser:
    """Parse JS files to identify components requiring initialization."""

    def __init__(self, js_file: Path):
        self.js_file = js_file
        self.components: Dict[str, Dict] = {}  # component_name -> {selectors, data_attrs, init_pattern}

    def parse(self) -> Dict[str, Dict]:
        """Parse JS file and return component initialization info."""
        if not self.js_file.exists():
            return {}

        content = self.js_file.read_text(encoding="utf-8")

        # Known UX4G components from the codebase
        component_classes = [
            "Alert", "Button", "Carousel", "Collapse", "Dropdown",
            "Modal", "Offcanvas", "Popover", "ScrollSpy", "Tab", "Toast", "Tooltip"
        ]

        for comp_name in component_classes:
            info = self._extract_component_info(content, comp_name)
            if info:
                self.components[comp_name.lower()] = info

        return self.components

    def _extract_component_info(self, content: str, component_name: str) -> Optional[Dict]:
        """Extract initialization info for a component."""
        info = {
            "selectors": [],
            "data_attributes": [],
            "init_pattern": None,
            "requires_js": True,
        }

        # Look for class definition
        class_pattern = rf"class\s+{component_name}\s+extends"
        if not re.search(class_pattern, content):
            return None

        # Extract data attribute patterns (data-bs-*, data-ux4g-*)
        data_pattern = rf"data-(?:bs|ux4g)-[\w-]+"
        data_attrs = set(re.findall(data_pattern, content))
        info["data_attributes"] = sorted(list(data_attrs))

        # Extract common selectors (class-based)
        selector_patterns = {
            "modal": r"\.modal",
            "carousel": r"\.carousel",
            "dropdown": r"\.dropdown",
            "collapse": r"\.collapse",
            "alert": r"\.alert",
            "toast": r"\.toast",
            "tooltip": r"\.tooltip",
            "popover": r"\.popover",
            "tab": r"\.nav-tabs?|\.tab",
        }

        comp_key = component_name.lower()
        if comp_key in selector_patterns:
            selectors = re.findall(selector_patterns[comp_key], content)
            info["selectors"] = list(set(selectors))

        # Determine initialization pattern
        if "getOrCreateInstance" in content or "new " + component_name in content:
            info["init_pattern"] = f"new {component_name}(element)"

        return info

"""JavaScript parser for extracting UX4G component initialization patterns."""

import re
from pathlib import Path
from typing import Dict, Optional


class JSParser:
    """Parse JS files to identify components requiring initialization."""

    _CLASS_PATTERN = re.compile(r"class\s+(?P<name>[A-Za-z0-9_]+)\s+extends")
    _CONSTANTS_MARKER_PATTERN = re.compile(r"/\*\*[\s\S]*?\bConstants\b[\s\S]*?\*/")
    _NAME_CONST_PATTERN = re.compile(r"const\s+NAME[\w$]*\s*=\s*['\"][^'\"]+['\"]\s*;")

    def __init__(self, js_file: Path):
        self.js_file = js_file
        self.components: Dict[
            str, Dict
        ] = {}  # component_name -> {selectors, data_attrs, init_pattern}

    def parse(self) -> Dict[str, Dict]:
        """Parse JS file and return component initialization info."""
        if not self.js_file.exists():
            return {}

        content = self.js_file.read_text(encoding="utf-8")

        # Known UX4G components from the codebase
        component_classes = [
            "Alert",
            "Button",
            "Carousel",
            "Collapse",
            "Dropdown",
            "Modal",
            "Offcanvas",
            "Popover",
            "ScrollSpy",
            "Tab",
            "Toast",
            "Tooltip",
        ]
        component_set = set(component_classes)
        class_matches = list(self._CLASS_PATTERN.finditer(content))

        for index, class_match in enumerate(class_matches):
            class_name = class_match.group("name")
            if class_name not in component_set:
                continue

            next_class_start = (
                class_matches[index + 1].start()
                if index + 1 < len(class_matches)
                else None
            )
            section = self._component_section(
                content=content,
                component_name=class_name,
                class_start=class_match.start(),
                next_class_start=next_class_start,
            )
            info = self._extract_component_info(section, class_name)
            if info:
                self.components[class_name.lower()] = info

        return self.components

    def _component_section(
        self,
        content: str,
        component_name: str,
        class_start: int,
        next_class_start: Optional[int],
    ) -> str:
        """
        Extract a component-scoped source slice.

        Prefer bounded constants sections when available to avoid whole-file
        data-attribute contamination. If constants markers are unavailable,
        bound by nearby NAME constants instead of next-component constants.
        """
        section_start = class_start
        previous_marker = None
        for marker in self._CONSTANTS_MARKER_PATTERN.finditer(content, 0, class_start):
            previous_marker = marker
        if previous_marker:
            section_start = previous_marker.start()
        else:
            name_const_start = self._find_component_name_const_start(
                content=content,
                component_name=component_name,
                class_start=class_start,
            )
            if name_const_start is not None:
                section_start = name_const_start

        section_end = next_class_start if next_class_start is not None else len(content)
        next_marker = self._CONSTANTS_MARKER_PATTERN.search(content, class_start + 1)
        if next_marker and next_marker.start() < section_end:
            section_end = next_marker.start()
        else:
            next_name_const = self._NAME_CONST_PATTERN.search(content, class_start + 1)
            if next_name_const and next_name_const.start() < section_end:
                section_end = next_name_const.start()

        return content[section_start:section_end]

    def _find_component_name_const_start(
        self,
        content: str,
        component_name: str,
        class_start: int,
    ) -> Optional[int]:
        component_name_pattern = re.compile(
            rf"const\s+NAME[\w$]*\s*=\s*['\"]{re.escape(component_name.lower())}['\"]\s*;"
        )
        name_const_start = None
        for match in component_name_pattern.finditer(content, 0, class_start):
            name_const_start = match.start()
        return name_const_start

    def _extract_component_info(
        self, content: str, component_name: str
    ) -> Optional[Dict]:
        """Extract initialization info for a component."""
        info = {
            "selectors": [],
            "data_attributes": [],
            "init_pattern": None,
            "requires_js": True,
        }

        class_pattern = rf"class\s+{component_name}\s+extends"
        if not re.search(class_pattern, content):
            return None

        # Extract data attribute patterns scoped to this component section.
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

        # Determine initialization pattern from component-scoped code.
        if f"{component_name}.getOrCreateInstance" in content or re.search(
            rf"new\s+{re.escape(component_name)}\b", content
        ):
            info["init_pattern"] = f"new {component_name}(element)"

        return info

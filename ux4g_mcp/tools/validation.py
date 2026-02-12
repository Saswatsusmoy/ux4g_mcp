"""Validation tool implementation."""
import json
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..registry import get_registry


class ValidationIssue:
    """Represents a validation issue."""
    def __init__(self, code: str, severity: str, message: str, location: Optional[str] = None, fix_hint: Optional[str] = None):
        self.code = code
        self.severity = severity
        self.message = message
        self.location = location
        self.fix_hint = fix_hint

    def to_dict(self):
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "location": self.location,
            "fix_hint": self.fix_hint,
        }


def detect_framework(code: str) -> str:
    """Detect if code is HTML or React JSX."""
    # Check for JSX patterns
    if "className=" in code or "htmlFor=" in code or "{/*" in code:
        return "react"
    return "html"


async def validate_snippet_tool(arguments: dict) -> str:
    """Validate code against UX4G design system rules."""
    code = arguments.get("code", "")
    framework = arguments.get("framework")

    if not code:
        return json.dumps({
            "is_valid": False,
            "issues": [{
                "code": "EMPTY_CODE",
                "severity": "error",
                "message": "No code provided for validation",
            }],
        }, indent=2)

    # Auto-detect framework if not provided
    if not framework:
        framework = detect_framework(code)

    registry = get_registry()
    issues: List[ValidationIssue] = []
    normalized_components = []

    # Parse HTML/JSX
    try:
        # Convert JSX className back to class for parsing
        parse_code = code
        if framework == "react":
            parse_code = code.replace("className=", "class=")
            parse_code = parse_code.replace("htmlFor=", "for=")

        soup = BeautifulSoup(parse_code, "html.parser")

        # Check for common UX4G components
        _validate_components(soup, registry, issues, normalized_components)
        _validate_accessibility(soup, issues)
        _validate_structure(soup, registry, issues)

    except Exception as e:
        issues.append(ValidationIssue(
            code="PARSE_ERROR",
            severity="error",
            message=f"Failed to parse code: {str(e)}",
        ))

    is_valid = len([i for i in issues if i.severity == "error"]) == 0

    result = {
        "is_valid": is_valid,
        "issues": [issue.to_dict() for issue in issues],
        "normalized_components": normalized_components,
        "framework": framework,
    }

    return json.dumps(result, indent=2)


def _validate_components(soup: BeautifulSoup, registry, issues: List[ValidationIssue], normalized_components: List[Dict]):
    """Validate component usage."""
    # Check for buttons
    buttons = soup.find_all("button")
    for btn in buttons:
        classes = btn.get("class", [])
        if isinstance(classes, str):
            classes = classes.split()
        if "btn" in classes:
            normalized_components.append({"type": "button", "classes": classes})
            # Check if btn is used without variant
            has_variant = any(c.startswith("btn-") and c != "btn" for c in classes)
            if not has_variant:
                issues.append(ValidationIssue(
                    code="MISSING_BUTTON_VARIANT",
                    severity="warning",
                    message="Button should have a variant class (e.g., btn-primary, btn-secondary)",
                    location=f"button element",
                    fix_hint="Add a variant class like 'btn-primary' or 'btn-outline-primary'",
                ))

    # Check for modals
    modals = soup.find_all(class_=re.compile(r"modal"))
    for modal in modals:
        normalized_components.append({"type": "modal", "classes": modal.get("class", [])})
        if not modal.get("id"):
            issues.append(ValidationIssue(
                code="MISSING_MODAL_ID",
                severity="error",
                message="Modal should have an id attribute",
                location="modal element",
                fix_hint="Add an id attribute to the modal element",
            ))

    # Check for forms
    form_controls = soup.find_all(["input", "select", "textarea"])
    for control in form_controls:
        classes = control.get("class", [])
        if isinstance(classes, str):
            classes = classes.split()
        if control.name in ["input", "select", "textarea"]:
            if not any(c.startswith("form-") for c in classes):
                issues.append(ValidationIssue(
                    code="MISSING_FORM_CLASS",
                    severity="warning",
                    message=f"{control.name} should have form-control or form-select class",
                    location=f"{control.name} element",
                    fix_hint=f"Add 'form-control' class to {control.name}",
                ))


def _validate_accessibility(soup: BeautifulSoup, issues: List[ValidationIssue]):
    """Validate accessibility requirements."""
    # Check for images without alt text
    images = soup.find_all("img")
    for img in images:
        if not img.get("alt"):
            issues.append(ValidationIssue(
                code="MISSING_ALT_TEXT",
                severity="warning",
                message="Image should have alt attribute for accessibility",
                location="img element",
                fix_hint="Add alt attribute describing the image",
            ))

    # Check for form labels
    inputs = soup.find_all(["input", "select", "textarea"])
    for inp in inputs:
        inp_id = inp.get("id")
        if inp_id:
            # Check if label exists with matching for attribute
            label = soup.find("label", {"for": inp_id})
            if not label:
                issues.append(ValidationIssue(
                    code="MISSING_LABEL",
                    severity="warning",
                    message=f"Form control with id '{inp_id}' should have an associated label",
                    location=f"{inp.name} element",
                    fix_hint="Add a <label> element with 'for' attribute matching the input id",
                ))


def _validate_structure(soup: BeautifulSoup, registry, issues: List[ValidationIssue]):
    """Validate structural requirements."""
    # Check for container/row/col structure
    rows = soup.find_all(class_=re.compile(r"row"))
    for row in rows:
        parent = row.parent
        if parent:
            parent_classes = parent.get("class", [])
            if isinstance(parent_classes, str):
                parent_classes = parent_classes.split()
            if not any(c in ["container", "container-fluid"] for c in parent_classes):
                issues.append(ValidationIssue(
                    code="ROW_WITHOUT_CONTAINER",
                    severity="warning",
                    message="Row should be inside a container or container-fluid",
                    location="row element",
                    fix_hint="Wrap the row in a <div class='container'> or <div class='container-fluid'>",
                ))

"""Code generation tool implementations."""
import json
from ..generator import SnippetGenerator


async def generate_snippet_tool(arguments: dict) -> str:
    """Generate UX4G-compliant code from natural language description."""
    description = arguments.get("description", "")
    framework = arguments.get("framework", "html")
    page_context = arguments.get("page_context")
    validation_level = arguments.get("validation_level", "relaxed")

    if not description:
        return json.dumps({"error": "description is required"}, indent=2)

    generator = SnippetGenerator()
    result = generator.generate(
        description=description,
        framework=framework,
        page_context=page_context,
        validation_level=validation_level,
    )

    return json.dumps(result, indent=2)


async def refine_snippet_tool(arguments: dict) -> str:
    """Refine existing UX4G code based on natural language change request."""
    existing_code = arguments.get("existing_code", "")
    change_request = arguments.get("change_request", "")
    framework = arguments.get("framework")

    if not existing_code or not change_request:
        return json.dumps({
            "error": "existing_code and change_request are required"
        }, indent=2)

    generator = SnippetGenerator()
    result = generator.refine(
        existing_code=existing_code,
        change_request=change_request,
        framework=framework,
    )

    return json.dumps(result, indent=2)

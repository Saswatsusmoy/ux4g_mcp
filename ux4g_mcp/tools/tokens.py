"""Token-related tool implementations."""
import json
from ..registry import get_registry


async def list_tokens_tool(arguments: dict) -> str:
    """List design tokens (colors, spacing, typography, breakpoints)."""
    registry = get_registry()
    token_type = arguments.get("token_type", "all")

    tokens = registry.get_tokens(token_type=token_type if token_type != "all" else None)

    result = []
    for token in tokens:
        token_data = {
            "name": token.name,
            "type": token.token_type,
            "value": token.value,
            "css_variable": token.css_variable,
            "css_class": token.css_class,
        }
        if token.description:
            token_data["description"] = token.description
        if token.usage_examples:
            token_data["usage_examples"] = token.usage_examples

        result.append(token_data)

    return json.dumps({"tokens": result}, indent=2)

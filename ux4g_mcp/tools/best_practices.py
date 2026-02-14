"""Best-practices tool backed by UX4G handbook knowledge base."""
import json

from ..services import BestPracticesService


async def get_bestpractices_tool(arguments: dict) -> str:
    """Get UX4G best practices matched to an optional query."""
    service = BestPracticesService()
    result = service.query(
        user_query=arguments.get("query"),
        limit=arguments.get("limit", 10),
    )
    return json.dumps(result, indent=2)

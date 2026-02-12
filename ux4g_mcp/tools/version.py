"""Version tool implementation."""
import json
from ..config import UX4G_VERSION, UX4G_ASSET_ROOT


async def get_version_tool(arguments: dict) -> str:
    """Get UX4G version and asset information."""
    info = {
        "version": UX4G_VERSION,
        "asset_root": str(UX4G_ASSET_ROOT),
        "mcp_version": "1.0.0",
    }
    return json.dumps(info, indent=2)

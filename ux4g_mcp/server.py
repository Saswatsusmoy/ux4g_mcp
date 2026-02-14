"""Main MCP server entrypoint for UX4G design system."""
import asyncio
from typing import Any

import mcp.server.stdio
from mcp import types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .tools import (
    list_components_tool,
    use_component_tool,
    get_bestpractices_tool,
    get_version_tool,
)

# Initialize MCP server
server = Server("ux4g-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available UX4G MCP tools."""
    return [
        types.Tool(
            name="get_version",
            description="Get UX4G version and asset information",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="get_bestpractices",
            description="Get UX4G best practices from UX4G Handbook knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Optional query to filter best practices (e.g., 'accessibility forms mobile')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of practices to return",
                        "default": 10,
                    },
                },
            },
        ),
        types.Tool(
            name="list_components",
            description="List all UX4G components in structured JSON with metadata and IDs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category (e.g., 'layout', 'form', 'navigation')",
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag",
                    },
                    "requires_js": {
                        "type": "boolean",
                        "description": "Filter components that require JavaScript initialization",
                    },
                    "layout_vs_component": {
                        "type": "string",
                        "enum": ["layout", "component", "both"],
                        "description": "Filter by layout vs component type",
                    },
                },
            },
        ),
        types.Tool(
            name="use_component",
            description="Get selected UX4G components with structured metadata and code payload (HTML/React/CSS/JS).",
            inputSchema={
                "type": "object",
                "properties": {
                    "component_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of selected component IDs from list_components.",
                    },
                    "framework": {
                        "type": "string",
                        "enum": ["html", "react"],
                        "description": "Preferred framework for `code.preferred`.",
                        "default": "html",
                    },
                    "include_css": {
                        "type": "boolean",
                        "description": "Include extracted component CSS rules.",
                        "default": True,
                    },
                    "include_js": {
                        "type": "boolean",
                        "description": "Include component JS init/constructor code when available.",
                        "default": True,
                    }
                },
                "required": ["component_ids"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_version":
            result = await get_version_tool(arguments)
        elif name == "get_bestpractices":
            result = await get_bestpractices_tool(arguments)
        elif name == "list_components":
            result = await list_components_tool(arguments)
        elif name == "use_component":
            result = await use_component_tool(arguments)
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"Unknown tool: {name}",
                )
            ]

        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}",
            )
        ]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ux4g-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

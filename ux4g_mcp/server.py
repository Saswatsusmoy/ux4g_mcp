"""Main MCP server entrypoint for UX4G design system."""
import asyncio
from typing import Any

import mcp.server.stdio
from mcp import types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .config import UX4G_VERSION
from .tools import (
    list_components_tool,
    get_component_tool,
    generate_snippet_tool,
    refine_snippet_tool,
    validate_snippet_tool,
    list_tokens_tool,
    get_version_tool,
)

# Initialize MCP server
server = Server("ux4g-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available UX4G MCP tools."""
    return [
        types.Tool(
            name="ux4g_get_version",
            description="Get UX4G version and asset information",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="ux4g_list_components",
            description="List UX4G components with direct code snippets inline. Each component includes its default snippet (HTML/JSX) — use the code as-is, no paths or external fetch.",
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
                    "framework": {
                        "type": "string",
                        "enum": ["html", "react"],
                        "description": "Snippet format: html or react (default: html)",
                        "default": "html",
                    },
                },
            },
        ),
        types.Tool(
            name="ux4g_get_component",
            description="Get one UX4G component with full snippet code inline. Returns the primary snippet plus all variants with their snippet and snippet_react — use the returned code directly, no paths.",
            inputSchema={
                "type": "object",
                "properties": {
                    "component_id": {
                        "type": "string",
                        "description": "Component identifier (e.g., 'button', 'modal', 'card')",
                    },
                    "variant": {
                        "type": "string",
                        "description": "Optional variant name (e.g., 'primary', 'outline', 'ghost')",
                    },
                    "framework": {
                        "type": "string",
                        "enum": ["html", "react"],
                        "description": "Output framework",
                        "default": "html",
                    },
                },
                "required": ["component_id"],
            },
        ),
        types.Tool(
            name="ux4g_generate_snippet",
            description="Generate UX4G-compliant code from natural language description",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Natural language description of the UI to generate",
                    },
                    "framework": {
                        "type": "string",
                        "enum": ["html", "react"],
                        "description": "Output framework",
                        "default": "html",
                    },
                    "page_context": {
                        "type": "object",
                        "description": "Optional page context (container, grid, theme, RTL)",
                        "properties": {
                            "container": {"type": "boolean"},
                            "grid": {"type": "boolean"},
                            "theme": {"type": "string", "enum": ["light", "dark"]},
                            "rtl": {"type": "boolean"},
                        },
                    },
                    "validation_level": {
                        "type": "string",
                        "enum": ["strict", "relaxed"],
                        "description": "Validation strictness",
                        "default": "relaxed",
                    },
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="ux4g_refine_snippet",
            description="Refine existing UX4G code based on natural language change request",
            inputSchema={
                "type": "object",
                "properties": {
                    "existing_code": {
                        "type": "string",
                        "description": "Existing HTML or JSX code",
                    },
                    "change_request": {
                        "type": "string",
                        "description": "Natural language description of changes to apply",
                    },
                    "framework": {
                        "type": "string",
                        "enum": ["html", "react"],
                        "description": "Framework of the code (auto-detected if not provided)",
                    },
                },
                "required": ["existing_code", "change_request"],
            },
        ),
        types.Tool(
            name="ux4g_validate_snippet",
            description="Validate code against UX4G design system rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "HTML or JSX code to validate",
                    },
                    "framework": {
                        "type": "string",
                        "enum": ["html", "react"],
                        "description": "Framework of the code (auto-detected if not provided)",
                    },
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="ux4g_list_tokens",
            description="List design tokens (colors, spacing, typography, breakpoints)",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_type": {
                        "type": "string",
                        "enum": ["color", "spacing", "typography", "breakpoint", "all"],
                        "description": "Filter by token type",
                        "default": "all",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle tool calls."""
    try:
        if name == "ux4g_get_version":
            result = await get_version_tool(arguments)
        elif name == "ux4g_list_components":
            result = await list_components_tool(arguments)
        elif name == "ux4g_get_component":
            result = await get_component_tool(arguments)
        elif name == "ux4g_generate_snippet":
            result = await generate_snippet_tool(arguments)
        elif name == "ux4g_refine_snippet":
            result = await refine_snippet_tool(arguments)
        elif name == "ux4g_validate_snippet":
            result = await validate_snippet_tool(arguments)
        elif name == "ux4g_list_tokens":
            result = await list_tokens_tool(arguments)
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

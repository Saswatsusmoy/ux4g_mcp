"""Entry point for running the MCP server as a module."""

import asyncio

from .server import main as server_main


def main() -> None:
    """Sync console entrypoint that runs the async MCP server main."""
    asyncio.run(server_main())


if __name__ == "__main__":
    main()

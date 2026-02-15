# UX4G MCP Server

A Model Context Protocol (MCP) server that exposes UX4G design-system knowledge and component metadata to MCP-compatible clients (for example, Cursor and Claude Desktop).

## Overview

This project enables AI-assisted UI development against UX4G conventions by providing tools for:

- Discovering available components and their metadata
- Retrieving implementation payloads for selected components (HTML/React/CSS/JS)
- Looking up UX4G handbook-aligned best practices
- Verifying installed UX4G asset/version information

## Repository Layout

```text
ux4g_mcp/
|-- ux4g_mcp/
|   |-- __main__.py         # Module entrypoint (`python -m ux4g_mcp`)
|   |-- server.py           # MCP server implementation
|   |-- config.py           # Runtime configuration
|   |-- tools/              # MCP tool handlers
|   |-- registry/           # Component registry + extraction logic
|   |-- metadata/           # Curated component metadata
|   `-- services/           # Supporting service layer
|-- ux4g_2.0.8/             # UX4G assets (default asset root)
|-- requirements.txt
|-- setup.py
`-- SETUP.md                # Client integration and troubleshooting
```

## Requirements

- Python 3.8+
- UX4G assets available locally (default: `ux4g_2.0.8/`)
- Dependencies from `requirements.txt`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

Use module execution (required for correct package-relative imports):

```bash
python -m ux4g_mcp
```

Equivalent alternatives:

```bash
python -m ux4g_mcp.server
ux4g-mcp
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

### MCP Tools
## Exposed MCP Tools

The server currently advertises the following tools:

- `get_version`: Returns UX4G version and asset-root information
- `get_bestpractices`: Returns UX4G handbook-backed best practices, optionally filtered by query
- `list_components`: Returns component catalog entries with filters (category, tag, JS requirement, type)
- `use_component`: Returns structured component payloads for selected `component_ids`

## Configuration

Environment variables:

- `UX4G_ASSET_ROOT`: Path to UX4G assets (default: `ux4g_2.0.8/`)
- `UX4G_DEFAULT_FRAMEWORK`: Preferred framework for generated payloads (`html` or `react`, default: `html`)

Example:

```bash
export UX4G_ASSET_ROOT="/absolute/path/to/ux4g_2.0.8"
export UX4G_DEFAULT_FRAMEWORK="react"
python -m ux4g_mcp
```

## Development

Install editable package mode:

```bash
pip install -e .
```

Run quick import health check:

```bash
python -c "from ux4g_mcp.server import main; print('Server import OK')"
```

## Troubleshooting

For client wiring and MCP configuration details, see `SETUP.md`.

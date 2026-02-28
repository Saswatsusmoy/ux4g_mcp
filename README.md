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

- Python 3.10+
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

### Test Types

- Tool contract tests: validate MCP tool payload shapes and default behavior (`tests/test_tools_components.py`, `tests/test_tools_additional.py`)
- Service-layer tests: validate component service behavior, including CSS/JS asset extraction (`tests/test_component_service.py`)
- Parser tests: validate CSS and JS parsing logic for classes/tokens/component metadata (`tests/test_css_parser.py`, `tests/test_js_parser.py`)
- Validation-rule tests: verify snippet validation outcomes and issue reporting (`tests/test_validation.py`)
- Conversion tests: verify HTML-to-JSX conversion behavior for generated/component snippets (`tests/test_react_conversion.py`)
- Cache/regression tests: verify registry cache fingerprint invalidation and force rebuild behavior (`tests/test_registry_cache.py`)
- Entrypoint smoke tests: verify module entrypoint wiring (`tests/test_entrypoint.py`)

## Exposed MCP Tools

The server currently advertises the following tools:

- `get_version`: Returns UX4G version and asset-root information
- `get_bestpractices`: Returns UX4G handbook-backed best practices, optionally filtered by query
- `list_components`: Returns component catalog entries with filters (category, tag, JS requirement, type)
- `use_component`: Returns structured component payloads for selected `component_ids`
- `list_tokens`: Returns design tokens (colors, spacing, typography, breakpoints), optionally filtered by type
- `validate_snippet`: Validates HTML/React snippets against UX4G component and accessibility rules
- `generate_snippet`: Generates UX4G-compliant snippets from natural language descriptions
- `refine_snippet`: Refines existing UX4G snippets based on a change request

## Configuration

Environment variables:

- `UX4G_ASSET_ROOT`: Path to UX4G assets (default: `ux4g_2.0.8/`)
- `UX4G_DEFAULT_FRAMEWORK`: Preferred framework for generated payloads (`html` or `react`, default: `html`)
- `UX4G_FORCE_REBUILD`: Force registry rebuild and ignore cached registry (`true/false`, default: `false`)

Example:

```bash
export UX4G_ASSET_ROOT="/absolute/path/to/ux4g_2.0.8"
export UX4G_DEFAULT_FRAMEWORK="react"
export UX4G_FORCE_REBUILD="true"
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

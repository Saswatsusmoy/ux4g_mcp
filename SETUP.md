# UX4G MCP Server Setup Guide

This guide covers local setup and MCP client configuration for the UX4G MCP server.

## 1. Install Dependencies

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional verification:

```bash
python -c "from ux4g_mcp.server import main; print('Server ready')"
```

## 2. Verify Local Server Startup

Run the server with module execution:

```bash
python -m ux4g_mcp
```

Important:

- Use `python -m ux4g_mcp` (or `python -m ux4g_mcp.server`)
- Do not run `ux4g_mcp/server.py` directly; relative imports can fail in that mode

## 3. Configure MCP Client (Cursor Example)

Cursor reads MCP configuration from:

- Global config: `~/.cursor/mcp.json`
- Workspace config: `.cursor/mcp.json` (when this repo is opened as the workspace)

Example configuration:

```json
{
  "mcpServers": {
    "ux4g": {
      "command": "/absolute/path/to/python",
      "args": ["-m", "ux4g_mcp"],
      "cwd": "/absolute/path/to/ux4g_mcp"
    }
  }
}
```

Configuration requirements:

- `command` must point to the Python interpreter with installed dependencies
- `args` must be `["-m", "ux4g_mcp"]`
- `cwd` must be the repository root containing `requirements.txt` and `ux4g_mcp/`

## 4. Restart Client and Confirm Tools

After saving MCP config:

1. Fully restart the client (quit and reopen)
2. Confirm the following tools are available:
   - `ux4g_get_version`
   - `ux4g_get_bestpractices`
   - `ux4g_list_components`
   - `ux4g_use_component`
   - `ux4g_list_tokens`
   - `ux4g_validate_snippet`
   - `ux4g_generate_snippet`
   - `ux4g_refine_snippet`

## 5. Run Tests (Optional)

```bash
pip install -r requirements-dev.txt
pytest
```

Note: Tests import the local package directly from the repo root; an editable install is not required.

## Troubleshooting

### `ModuleNotFoundError` or MCP connection failure

- Confirm module mode: `args` must use `-m ux4g_mcp`
- Confirm dependencies are installed in the interpreter used by `command`
- Confirm `cwd` points to repository root

### Pydantic-related import/runtime errors

```bash
pip install "pydantic>=2,<3"
pip install --upgrade mcp
```

### Assets not found

- Confirm UX4G assets exist at `ux4g_2.0.8/`
- Or set `UX4G_ASSET_ROOT` to the correct absolute path

## Diagnostic Commands

```bash
# Confirm interpreter path
which python

# Confirm package versions
python -c "import mcp, pydantic; print('mcp OK, pydantic', pydantic.__version__)"

# Smoke test module import
python -c "import ux4g_mcp; print('ux4g_mcp import OK')"
```

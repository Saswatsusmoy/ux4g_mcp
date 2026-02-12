#!/bin/bash
# Fix Pydantic version mismatch for UX4G MCP Server

echo "🔧 Fixing Pydantic version mismatch..."
echo ""

# Use the pyenv Python
PYTHON="/Users/saswatsusmoy/.pyenv/versions/3.12.9/bin/python3"
PIP="${PYTHON} -m pip"

echo "1. Checking current Pydantic version..."
$PIP show pydantic 2>/dev/null | grep Version || echo "   Pydantic not found"

echo ""
echo "2. Upgrading Pydantic to v2..."
$PIP install --upgrade "pydantic>=2.0.0,<3.0.0"

echo ""
echo "3. Installing/upgrading MCP SDK..."
$PIP install --upgrade "mcp>=1.0.0"

echo ""
echo "4. Installing all other dependencies..."
$PIP install -r requirements.txt

echo ""
echo "5. Verifying installation..."
$PYTHON -c "
import pydantic
import mcp
print(f'✅ Pydantic version: {pydantic.__version__}')
print(f'✅ MCP SDK imported successfully')
print(f'✅ All dependencies ready!')
"

echo ""
echo "✅ Setup complete! Restart Cursor to use the UX4G MCP server."

"""Setup script for UX4G MCP Server."""

from setuptools import find_packages, setup

setup(
    name="ux4g-mcp",
    version="1.0.0",
    description="MCP server for UX4G design system",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "tinycss2>=1.2.0",
        "beautifulsoup4>=4.12.0",
        "jinja2>=3.1.0",
        "pyyaml>=6.0",
        "html5lib>=1.1",
        "lxml>=5.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ux4g-mcp=ux4g_mcp.__main__:main",
        ],
    },
)

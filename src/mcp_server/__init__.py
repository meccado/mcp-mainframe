"""
MCP COBOL Server - Mainframe source code retrieval via MCP protocol.

This package provides an MCP server that exposes tools to retrieve
COBOL program source and copybooks from z/OS mainframe datasets.
"""

__version__ = "1.0.0"
__author__ = "MCP Mainframe Team"

from .server import main

__all__ = ["main"]

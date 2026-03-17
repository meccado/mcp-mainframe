"""
MCP COBOL Server - Main entry point.

Implements the MCP protocol server with stdio transport.
Exposes:
- Tools: get_cobol_source, get_copybook
- Resources: Frequently accessed programs and copybooks

Supports two backends:
- SSH: Direct SSH connection to mainframe USS filesystem
- Endevor: CA Endevor API web services
"""

import asyncio
import logging
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

from .config import load_config, Config
from .ssh_client import SSHConnectionPool, MainframeSSH
from .endevor_client import EndevorClient
from .tools import validate_member_name, create_tool_handlers
from .resources import create_resource_manager, ResourceManager

# Configure logging to stderr
def setup_logging(log_level: str) -> logging.Logger:
    """
    Configure logging to stderr with specified level.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        '%(levelname)s: %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('mcp_cobol')
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    return logger


async def run_server(config: Config, logger: logging.Logger) -> None:
    """
    Run the MCP server with stdio transport.
    
    Args:
        config: Server configuration
        logger: Configured logger
    """
    backend = config.backend.upper()
    logger.info(f"Starting MCP COBOL Server (backend: {backend})...")
    
    # Initialize backend-specific clients
    pool = None
    endevor_client = None
    
    try:
        if backend == "SSH":
            # SSH backend - initialize connection pool
            pool = SSHConnectionPool(config)
            ssh_client = MainframeSSH(pool, config)
            logger.info("SSH connection pool initialized")

        elif backend == "ENDEVOR":
            # Endevor backend - initialize HTTP client
            endevor_client = EndevorClient(config)
            logger.info("Endevor client initialized")

        # Create tool handlers based on backend
        tool_handlers = create_tool_handlers(
            config=config,
            pool=pool,
            endevor=endevor_client
        )
        
        # Create resource manager
        resource_manager = create_resource_manager(config)
        logger.info("Resource manager initialized")

        # Create MCP server
        server = Server("mcp-cobol-server")

        @server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available MCP resources."""
            logger.debug("Handling list_resources request")
            return resource_manager.list_resources()

        @server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource by URI."""
            logger.debug(f"Handling read_resource request: {uri}")
            return await resource_manager.read_resource(uri)

        @server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available MCP tools."""
            logger.debug("Handling list_tools request")

            return [
                Tool(
                    name="get_cobol_source",
                    description=(
                        "Retrieve the latest COBOL source code for a given program from the mainframe. "
                        "Returns the complete source code as plain text."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "program": {
                                "type": "string",
                                "description": "The COBOL program name (1-8 alphanumeric characters)",
                                "minLength": 1,
                                "maxLength": 8,
                                "pattern": "^[A-Za-z0-9@#$]+$"
                            }
                        },
                        "required": ["program"],
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="get_copybook",
                    description=(
                        "Retrieve a COBOL copybook (data structure definition) from the mainframe. "
                        "Returns the complete copybook source as plain text."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "copybook": {
                                "type": "string",
                                "description": "The copybook name (1-8 alphanumeric characters)",
                                "minLength": 1,
                                "maxLength": 8,
                                "pattern": "^[A-Za-z0-9@#$]+$"
                            }
                        },
                        "required": ["copybook"],
                        "additionalProperties": False
                    }
                )
            ]
        
        @server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """
            Handle tool call requests.
            
            Args:
                name: Tool name (get_cobol_source or get_copybook)
                arguments: Tool arguments
                
            Returns:
                Tool result as text content
            """
            logger.info(f"Handling call_tool request: {name}")
            
            try:
                if name == "get_cobol_source":
                    # Validate program name
                    program = validate_member_name(arguments.get('program', ''), "program")
                    
                    # Retrieve source
                    source = await ssh_client.read_member(
                        config.cobol_source_dsn,
                        program
                    )
                    
                    logger.info(f"Successfully retrieved program '{program}'")
                    
                    return [TextContent(
                        type="text",
                        text=source
                    )]
                    
                elif name == "get_copybook":
                    # Validate copybook name
                    copybook = validate_member_name(arguments.get('copybook', ''), "copybook")
                    
                    # Retrieve source
                    source = await ssh_client.read_member(
                        config.copybook_dsn,
                        copybook
                    )
                    
                    logger.info(f"Successfully retrieved copybook '{copybook}'")
                    
                    return [TextContent(
                        type="text",
                        text=source
                    )]
                    
                else:
                    logger.warning(f"Unknown tool requested: {name}")
                    raise ValueError(f"Unknown tool: {name}")
                    
            except FileNotFoundError as e:
                logger.info(f"Tool error (not found): {e}")
                return [TextContent(
                    type="text",
                    text=str(e)
                )]
                
            except PermissionError as e:
                logger.warning(f"Tool error (permission): {e}")
                return [TextContent(
                    type="text",
                    text=str(e)
                )]
                
            except ConnectionError as e:
                logger.warning(f"Tool error (connection): {e}")
                return [TextContent(
                    type="text",
                    text=str(e)
                )]
                
            except ValueError as e:
                logger.info(f"Tool error (validation): {e}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
                
            except Exception as e:
                logger.error(f"Tool error (unexpected): {e}")
                return [TextContent(
                    type="text",
                    text=f"Error: An unexpected error occurred: {str(e)}"
                )]
        
        # Run server with stdio transport
        logger.info("Server initialized, waiting for MCP connection...")
        
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    finally:
        # Cleanup: close backend-specific resources
        if pool:
            await pool.close()
            logger.info("SSH connection pool closed")
        
        if endevor_client:
            await endevor_client.close()
            logger.info("Endevor client closed")
        
        logger.info("Server shutdown complete")


def main() -> None:
    """
    Main entry point for the MCP COBOL Server.
    
    Loads configuration, sets up logging, and runs the async server.
    Exits with clear error messages on configuration failures.
    """
    try:
        # Load and validate configuration
        config = load_config()
        
        # Setup logging
        logger = setup_logging(config.log_level)
        
        logger.info("Configuration validated successfully")
        
        # Run async server
        asyncio.run(run_server(config, logger))
        
    except KeyboardInterrupt:
        print("INFO: Server interrupted by user", file=sys.stderr)
        sys.exit(0)
        
    except SystemExit:
        raise
        
    except Exception as e:
        print(f"ERROR: Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

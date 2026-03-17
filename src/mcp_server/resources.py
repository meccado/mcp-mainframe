"""
MCP Resources for frequently accessed COBOL programs and copybooks.

Resources allow MCP clients to discover and read data directly from the server
without invoking tools. This is useful for:
- Listing available programs/copybooks
- Providing metadata about elements
- Exposing configuration information
"""

import logging
from typing import Any, Optional
from dataclasses import dataclass

from mcp.types import Resource

from .config import Config

logger = logging.getLogger(__name__)


@dataclass
class ResourceInfo:
    """Information about a resource."""
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


class ResourceManager:
    """
    Manages MCP resources for frequently accessed data.
    
    Resources provide a way to expose data without tool invocation.
    Use cases:
    - List of frequently accessed programs
    - List of commonly used copybooks
    - System metadata and status
    - Configuration information
    
    Usage:
        manager = ResourceManager(config)
        resources = await manager.list_resources()
        content = await manager.read_resource(uri)
    """
    
    def __init__(self, config: Config):
        """
        Initialize resource manager.
        
        Args:
            config: Server configuration
        """
        self._config = config
        self._backend = config.backend.upper()
        
        # Define static resources
        self._static_resources = [
            ResourceInfo(
                uri="cobol://metadata",
                name="Server Metadata",
                description="MCP COBOL Server metadata and configuration",
                mime_type="application/json"
            ),
            ResourceInfo(
                uri="cobol://status",
                name="Server Status",
                description="Current server status and backend information",
                mime_type="application/json"
            ),
        ]
        
        # Frequently accessed programs (can be populated from config or file)
        self._frequent_programs = self._load_frequent_programs()
        
        # Frequently accessed copybooks
        self._frequent_copybooks = self._load_frequent_copybooks()
        
        logger.info(f"ResourceManager initialized with {len(self._static_resources)} static resources")
    
    def _load_frequent_programs(self) -> list[str]:
        """
        Load list of frequently accessed programs.
        
        In a production environment, this could:
        - Read from a configuration file
        - Query a database of commonly used programs
        - Track usage statistics and auto-populate
        
        For now, returns an empty list (can be extended via config).
        """
        # Example: Could load from FREQUENT_PROGRAMS env var
        # Format: comma-separated list of program names
        # Example: "PAYROLL,BILLING,CUSTUPD"
        import os
        frequent = os.environ.get("FREQUENT_PROGRAMS", "")
        if frequent:
            programs = [p.strip().upper() for p in frequent.split(",") if p.strip()]
            logger.info(f"Loaded {len(programs)} frequent programs")
            return programs
        return []
    
    def _load_frequent_copybooks(self) -> list[str]:
        """
        Load list of frequently accessed copybooks.
        
        Similar to _load_frequent_programs but for copybooks.
        """
        import os
        frequent = os.environ.get("FREQUENT_COPYBOOKS", "")
        if frequent:
            copybooks = [c.strip().upper() for c in frequent.split(",") if c.strip()]
            logger.info(f"Loaded {len(copybooks)} frequent copybooks")
            return copybooks
        return []
    
    def list_resources(self) -> list[Resource]:
        """
        List all available resources.
        
        Returns:
            List of Resource objects for MCP protocol
        """
        resources = []
        
        # Add static resources
        for info in self._static_resources:
            resources.append(Resource(
                uri=info.uri,
                name=info.name,
                description=info.description,
                mimeType=info.mime_type
            ))
        
        # Add frequent programs as resources
        for program in self._frequent_programs:
            resources.append(Resource(
                uri=f"cobol://program/{program}",
                name=f"Program: {program}",
                description=f"Frequently accessed COBOL program: {program}",
                mimeType="text/plain"
            ))
        
        # Add frequent copybooks as resources
        for copybook in self._frequent_copybooks:
            resources.append(Resource(
                uri=f"cobol://copybook/{copybook}",
                name=f"Copybook: {copybook}",
                description=f"Frequently accessed copybook: {copybook}",
                mimeType="text/plain"
            ))
        
        logger.debug(f"Listing {len(resources)} resources")
        return resources
    
    async def read_resource(self, uri: str) -> str:
        """
        Read a resource by URI.
        
        Args:
            uri: Resource URI (e.g., "cobol://metadata", "cobol://program/PAYROLL")
            
        Returns:
            Resource content as string
            
        Raises:
            ValueError: If URI is unknown
        """
        logger.debug(f"Reading resource: {uri}")
        
        # Handle static resources
        if uri == "cobol://metadata":
            return self._read_metadata()
        
        elif uri == "cobol://status":
            return self._read_status()
        
        # Handle frequent program resources
        elif uri.startswith("cobol://program/"):
            program_name = uri.replace("cobol://program/", "")
            return self._read_program_resource(program_name)
        
        # Handle frequent copybook resources
        elif uri.startswith("cobol://copybook/"):
            copybook_name = uri.replace("cobol://copybook/", "")
            return self._read_copybook_resource(copybook_name)
        
        else:
            raise ValueError(f"Unknown resource URI: {uri}")
    
    def _read_metadata(self) -> str:
        """Read server metadata resource."""
        import json
        
        metadata = {
            "server": "MCP COBOL Server",
            "version": "1.0.0",
            "backend": self._backend,
            "description": "Provides access to COBOL programs and copybooks on z/OS mainframe",
            "features": [
                "get_cobol_source - Retrieve COBOL program source",
                "get_copybook - Retrieve copybook source",
                "resources - Frequently accessed programs and copybooks"
            ]
        }
        
        if self._backend == "SSH":
            metadata["ssh_config"] = {
                "host": self._config.host,
                "username": self._config.username,
                "cobol_dsn": self._config.cobol_source_dsn,
                "copybook_dsn": self._config.copybook_dsn
            }
        elif self._backend == "ENDEVOR":
            metadata["endevor_config"] = {
                "url": self._config.endevor_base_url,
                "user": self._config.endevor_user,
                "stage": self._config.endevor_stage
            }
        
        return json.dumps(metadata, indent=2)
    
    def _read_status(self) -> str:
        """Read server status resource."""
        import json
        from datetime import datetime
        
        status = {
            "status": "running",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "backend": self._backend,
            "frequent_programs_count": len(self._frequent_programs),
            "frequent_copybooks_count": len(self._frequent_copybooks)
        }
        
        return json.dumps(status, indent=2)
    
    def _read_program_resource(self, program_name: str) -> str:
        """
        Read a frequent program resource.
        
        Note: This returns metadata about the program, not the source code.
        To get source code, use the get_cobol_source tool.
        """
        import json
        
        # This is a placeholder - in production, could query metadata
        program_info = {
            "name": program_name,
            "type": "COBOL",
            "category": "frequent",
            "note": "Use get_cobol_source tool to retrieve actual source code"
        }
        
        return json.dumps(program_info, indent=2)
    
    def _read_copybook_resource(self, copybook_name: str) -> str:
        """
        Read a frequent copybook resource.
        
        Note: This returns metadata about the copybook, not the source code.
        To get source code, use the get_copybook tool.
        """
        import json
        
        copybook_info = {
            "name": copybook_name,
            "type": "COPYBOOK",
            "category": "frequent",
            "note": "Use get_copybook tool to retrieve actual source code"
        }
        
        return json.dumps(copybook_info, indent=2)
    
    def get_resource_templates(self) -> list[dict[str, Any]]:
        """
        Get resource templates for dynamic resource discovery.
        
        Templates allow clients to discover resource patterns.
        
        Returns:
            List of resource template definitions
        """
        return [
            {
                "uriTemplate": "cobol://program/{name}",
                "name": "COBOL Program",
                "description": "Frequently accessed COBOL program"
            },
            {
                "uriTemplate": "cobol://copybook/{name}",
                "name": "COBOL Copybook",
                "description": "Frequently accessed copybook"
            }
        ]


def create_resource_manager(config: Config) -> ResourceManager:
    """
    Factory function to create resource manager.
    
    Args:
        config: Server configuration
        
    Returns:
        Initialized ResourceManager
    """
    manager = ResourceManager(config)
    logger.info("Created ResourceManager")
    return manager


__all__ = ["ResourceManager", "ResourceInfo", "create_resource_manager"]

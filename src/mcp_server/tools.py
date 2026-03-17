"""
MCP tool implementations for COBOL source retrieval.

Provides tool handlers for:
- get_cobol_source: Retrieve COBOL program source
- get_copybook: Retrieve copybook source

Supports four backends:
- SSH: Direct SSH connection to mainframe USS filesystem
- Endevor: CA Endevor API web services
- z/OSMF: IBM z/OS Management Facility REST API
- Zowe: Open Mainframe Project API ML

All tools validate input, execute mainframe commands, and handle errors gracefully.
"""

import logging
import re
from typing import Any, Optional

from .config import Config
from .ssh_client import MainframeSSH, SSHConnectionPool
from .endevor_client import EndevorClient
from .zosmf_client import ZosmfClient
from .zowe_client import ZoweClient

logger = logging.getLogger(__name__)


# Program/copybook name validation pattern (z/OS member naming)
# Allows: A-Z, 0-9, @, #, $ (1-8 characters)
MEMBER_NAME_PATTERN = re.compile(r'^[A-Z0-9@#$]{1,8}$', re.IGNORECASE)


def validate_member_name(name: str, member_type: str = "program") -> str:
    """
    Validate a program or copybook name.
    
    Args:
        name: The member name to validate
        member_type: 'program' or 'copybook' for error messages
        
    Returns:
        Uppercase member name if valid
        
    Raises:
        ValueError: If name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValueError(
            f"Invalid {member_type} name: must be a non-empty string"
        )
    
    # Normalize to uppercase
    normalized = name.strip().upper()
    
    if not MEMBER_NAME_PATTERN.match(normalized):
        raise ValueError(
            f"Invalid {member_type} name '{name}'. "
            f"Names must be 1-8 alphanumeric characters (A-Z, 0-9, @, #, $)."
        )
    
    return normalized


class ToolHandlers:
    """
    MCP tool handlers for COBOL source retrieval.
    
    Supports two backends:
    - SSH: Direct SSH connection to mainframe USS filesystem
    - Endevor: CA Endevor API web services
    
    Provides methods that can be registered with the MCP server
    to handle tool calls.
    """
    
    def __init__(
        self,
        config: Config,
        ssh: Optional[MainframeSSH] = None,
        endevor: Optional[EndevorClient] = None
    ):
        """
        Initialize tool handlers.
        
        Args:
            config: Configuration with backend selection
            ssh: Mainframe SSH client (required if backend == "SSH")
            endevor: Endevor client (required if backend == "ENDEVOR")
        """
        self._config = config
        self._ssh = ssh
        self._endevor = endevor
        self._backend = config.backend.upper()
        
        logger.info(f"ToolHandlers initialized with backend: {self._backend}")

    async def get_cobol_source(self, arguments: dict[str, Any]) -> str:
        """
        Retrieve COBOL program source from mainframe.
        
        Supports four backends:
        - SSH: Retrieves from PDS dataset via USS filesystem
        - Endevor: Retrieves from Endevor library via REST API
        - z/OSMF: Retrieves via IBM z/OSMF REST API
        - Zowe: Retrieves via Zowe API ML
        
        Args:
            arguments: Tool call arguments with 'program' key
            
        Returns:
            COBOL source code as plain text
            
        Raises:
            ValueError: If program name is invalid
            FileNotFoundError: If program not found
            PermissionError: If access denied
            ConnectionError: If connection fails
        """
        # Extract and validate program name
        program_arg = arguments.get('program')
        if not program_arg:
            raise ValueError("Missing required argument: 'program'")
        
        program = validate_member_name(program_arg, "program")
        
        logger.info(f"get_cobol_source: Requesting program '{program}' (backend: {self._backend})")
        
        try:
            if self._backend == "SSH":
                # SSH backend - retrieve from PDS
                if not self._ssh:
                    raise RuntimeError("SSH client not initialized")
                
                source = await self._ssh.read_member(
                    self._config.cobol_source_dsn,
                    program
                )
                
                logger.info(f"get_cobol_source: Successfully retrieved '{program}' via SSH")
                
            elif self._backend == "ENDEVOR":
                # Endevor backend - retrieve from Endevor library
                if not self._endevor:
                    raise RuntimeError("Endevor client not initialized")
                
                element = await self._endevor.retrieve_element(program, "COBOL")
                source = element.source_code
                
                logger.info(f"get_cobol_source: Successfully retrieved '{program}' via Endevor")
            
            elif self._backend == "ZOSMF":
                # z/OSMF backend - retrieve via z/OSMF REST API
                if not self._zosmf:
                    raise RuntimeError("z/OSMF client not initialized")
                
                element = await self._zosmf.retrieve_member(
                    self._config.cobol_source_dsn,
                    program
                )
                source = element.source_code
                
                logger.info(f"get_cobol_source: Successfully retrieved '{program}' via z/OSMF")
            
            elif self._backend == "ZOWE":
                # Zowe backend - retrieve via Zowe API ML
                if not self._zowe:
                    raise RuntimeError("Zowe client not initialized")
                
                element = await self._zowe.retrieve_member(
                    self._config.cobol_source_dsn,
                    program
                )
                source = element.source_code
                
                logger.info(f"get_cobol_source: Successfully retrieved '{program}' via Zowe")
            
            else:
                raise RuntimeError(f"Unknown backend: {self._backend}")
            
            return source
            
        except FileNotFoundError as e:
            logger.info(f"get_cobol_source: Program '{program}' not found")
            raise FileNotFoundError(str(e)) from e
            
        except PermissionError as e:
            logger.warning(f"get_cobol_source: Permission denied for '{program}'")
            raise PermissionError(str(e)) from e
            
        except ConnectionError as e:
            logger.warning(f"get_cobol_source: Connection error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"get_cobol_source: Unexpected error: {e}")
            raise ConnectionError(
                f"Error retrieving program '{program}': {str(e)}"
            ) from e
    
    async def get_copybook(self, arguments: dict[str, Any]) -> str:
        """
        Retrieve copybook source from mainframe.
        
        Supports four backends:
        - SSH: Retrieves from PDS dataset via USS filesystem
        - Endevor: Retrieves from Endevor library via REST API
        - z/OSMF: Retrieves via IBM z/OSMF REST API
        - Zowe: Retrieves via Zowe API ML
        
        Args:
            arguments: Tool call arguments with 'copybook' key
            
        Returns:
            Copybook source code as plain text
            
        Raises:
            ValueError: If copybook name is invalid
            FileNotFoundError: If copybook not found
            PermissionError: If access denied
            ConnectionError: If connection fails
        """
        # Extract and validate copybook name
        copybook_arg = arguments.get('copybook')
        if not copybook_arg:
            raise ValueError("Missing required argument: 'copybook'")
        
        copybook = validate_member_name(copybook_arg, "copybook")
        
        logger.info(f"get_copybook: Requesting copybook '{copybook}' (backend: {self._backend})")
        
        try:
            if self._backend == "SSH":
                # SSH backend - retrieve from PDS
                if not self._ssh:
                    raise RuntimeError("SSH client not initialized")
                
                source = await self._ssh.read_member(
                    self._config.copybook_dsn,
                    copybook
                )
                
                logger.info(f"get_copybook: Successfully retrieved '{copybook}' via SSH")
                
            elif self._backend == "ENDEVOR":
                # Endevor backend - retrieve from Endevor library
                if not self._endevor:
                    raise RuntimeError("Endevor client not initialized")
                
                element = await self._endevor.retrieve_element(copybook, "COPY")
                source = element.source_code
                
                logger.info(f"get_copybook: Successfully retrieved '{copybook}' via Endevor")
            
            elif self._backend == "ZOSMF":
                # z/OSMF backend - retrieve via z/OSMF REST API
                if not self._zosmf:
                    raise RuntimeError("z/OSMF client not initialized")
                
                element = await self._zosmf.retrieve_member(
                    self._config.copybook_dsn,
                    copybook
                )
                source = element.source_code
                
                logger.info(f"get_copybook: Successfully retrieved '{copybook}' via z/OSMF")
            
            elif self._backend == "ZOWE":
                # Zowe backend - retrieve via Zowe API ML
                if not self._zowe:
                    raise RuntimeError("Zowe client not initialized")
                
                element = await self._zowe.retrieve_member(
                    self._config.copybook_dsn,
                    copybook
                )
                source = element.source_code
                
                logger.info(f"get_copybook: Successfully retrieved '{copybook}' via Zowe")
            
            else:
                raise RuntimeError(f"Unknown backend: {self._backend}")
            
            return source
            
        except FileNotFoundError as e:
            logger.info(f"get_copybook: Copybook '{copybook}' not found")
            raise FileNotFoundError(str(e)) from e
            
        except PermissionError as e:
            logger.warning(f"get_copybook: Permission denied for '{copybook}'")
            raise PermissionError(str(e)) from e
            
        except ConnectionError as e:
            logger.warning(f"get_copybook: Connection error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"get_copybook: Unexpected error: {e}")
            raise ConnectionError(
                f"Error retrieving copybook '{copybook}': {str(e)}"
            ) from e


def create_tool_handlers(
    config: Config,
    pool: Optional[SSHConnectionPool] = None,
    endevor: Optional[EndevorClient] = None,
    zosmf: Optional[ZosmfClient] = None,
    zowe: Optional[ZoweClient] = None
) -> ToolHandlers:
    """
    Factory function to create tool handlers.
    
    Args:
        config: Configuration with backend selection
        pool: SSH connection pool (required if backend == "SSH")
        endevor: Endevor client (required if backend == "ENDEVOR")
        zosmf: z/OSMF client (required if backend == "ZOSMF")
        zowe: Zowe client (required if backend == "ZOWE")
        
    Returns:
        Initialized ToolHandlers instance
    """
    backend = config.backend.upper()
    
    if backend == "SSH":
        if not pool:
            raise ValueError("SSH connection pool required for SSH backend")
        ssh = MainframeSSH(pool, config)
        return ToolHandlers(config=config, ssh=ssh, endevor=None, zosmf=None, zowe=None)
    
    elif backend == "ENDEVOR":
        if not endevor:
            raise ValueError("Endevor client required for Endevor backend")
        return ToolHandlers(config=config, ssh=None, endevor=endevor, zosmf=None, zowe=None)
    
    elif backend == "ZOSMF":
        if not zosmf:
            raise ValueError("z/OSMF client required for z/OSMF backend")
        return ToolHandlers(config=config, ssh=None, endevor=None, zosmf=zosmf, zowe=None)
    
    elif backend == "ZOWE":
        if not zowe:
            raise ValueError("Zowe client required for Zowe backend")
        return ToolHandlers(config=config, ssh=None, endevor=None, zosmf=None, zowe=zowe)
    
    else:
        raise ValueError(f"Unknown backend: {backend}")


__all__ = ["ToolHandlers", "create_tool_handlers", "validate_member_name"]

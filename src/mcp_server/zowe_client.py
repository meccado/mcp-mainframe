"""
Zowe API client for mainframe source code retrieval.

Provides integration with Zowe API ML (API Mediation Layer) for modern,
vendor-neutral mainframe access.

Requires: Zowe installed on mainframe (open source from Open Mainframe Project)
"""

import logging
import asyncio
from typing import Optional
from dataclasses import dataclass

import httpx

from .config import Config

logger = logging.getLogger(__name__)


@dataclass
class ZoweElement:
    """Represents a Zowe dataset element (program or copybook)."""
    name: str
    dsname: str
    member: str
    source_code: str
    volume: str = ""


class ZoweClient:
    """
    Client for Zowe API ML (API Mediation Layer).
    
    Supports:
    - Dataset member retrieval via Zowe z/OS Files service
    - Authentication via JWT token or basic auth
    - Modern REST API with OpenAPI specification
    
    Usage:
        client = ZoweClient(config)
        element = await client.retrieve_member("USER.COBOL.SRC", "PAYROLL")
        print(element.source_code)
    
    References:
    - Zowe Docs: https://docs.zowe.org/
    - z/OS Files API: https://docs.zowe.org/v2.11.x/web-help/index.html?path=/api/v1/zos-files
    - Zowe Python SDK: https://github.com/zowe/zowe-client-python
    """
    
    def __init__(self, config: Config):
        """
        Initialize Zowe client.
        
        Args:
            config: Configuration with Zowe connection parameters
        """
        self._config = config
        self._base_url = config.zowe_base_url.rstrip('/')
        self._user = config.zowe_user
        self._password = config.zowe_password
        self._verify_cert = config.zowe_verify_cert
        self._timeout = config.connection_timeout
        
        # JWT token (if using token-based auth)
        self._jwt_token: Optional[str] = None
        
        # HTTP client (reused across requests)
        self._client: Optional[httpx.AsyncClient] = None
        
        logger.info(
            f"ZoweClient initialized: URL={self._base_url}, "
            f"User={self._user}, VerifyCert={self._verify_cert}"
        )
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with authentication."""
        if self._client is None:
            # Configure headers
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Add JWT token if available
            if self._jwt_token:
                headers["Authorization"] = f"Bearer {self._jwt_token}"
            
            # Configure SSL verification
            if self._verify_cert:
                self._client = httpx.AsyncClient(
                    auth=(self._user, self._password),
                    timeout=httpx.Timeout(self._timeout),
                    headers=headers
                )
            else:
                # Development: skip certificate verification
                import ssl
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                self._client = httpx.AsyncClient(
                    auth=(self._user, self._password),
                    timeout=httpx.Timeout(self._timeout),
                    headers=headers,
                    verify=ssl_context
                )
                
        return self._client
    
    async def authenticate(self) -> bool:
        """
        Authenticate with Zowe API ML and obtain JWT token.
        
        Returns:
            True if authentication successful
            
        Raises:
            PermissionError: If authentication fails
        """
        client = await self._get_client()
        
        # Zowe authentication endpoint
        auth_url = f"{self._base_url}/api/v1/auth/login"
        
        try:
            response = await client.post(auth_url)
            
            if response.status_code == 200:
                data = response.json()
                # Extract JWT token from response
                self._jwt_token = data.get('token', {}).get('value', '')
                if self._jwt_token:
                    logger.info("Successfully authenticated with Zowe API ML")
                    return True
            
            logger.warning(f"Zowe authentication failed: {response.status_code}")
            raise PermissionError(
                f"Zowe authentication failed. Check credentials."
            )
            
        except Exception as e:
            logger.error(f"Zowe authentication error: {e}")
            raise PermissionError(f"Zowe authentication error: {str(e)}")
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("Zowe HTTP client closed")
    
    async def retrieve_member(self, dsname: str, member: str) -> ZoweElement:
        """
        Retrieve a dataset member via Zowe z/OS Files API.
        
        Args:
            dsname: Dataset name (e.g., 'USER.COBOL.SRC')
            member: Member name (e.g., 'PAYROLL')
            
        Returns:
            ZoweElement with source code
            
        Raises:
            FileNotFoundError: If member not found
            PermissionError: If access denied
            ConnectionError: If connection fails
        """
        client = await self._get_client()
        
        # Build Zowe REST API URL
        # Format: {base_url}/api/v1/zos-files/dataset/{dsname}/member/{member}
        import urllib.parse
        encoded_dsname = urllib.parse.quote(dsname, safe='')
        encoded_member = urllib.parse.quote(member, safe='')
        url = f"{self._base_url}/api/v1/zos-files/dataset/{encoded_dsname}/member/{encoded_member}"
        
        logger.debug(f"Retrieving Zowe member: {url}")
        
        try:
            response = await client.get(url)
            
            logger.debug(f"Zowe response status: {response.status_code}")
            
            # Handle common error cases
            if response.status_code == 404:
                raise FileNotFoundError(
                    f"Member '{member}' not found in dataset {dsname}"
                )
            
            if response.status_code == 401:
                # Try to re-authenticate
                await self.authenticate()
                # Retry request
                response = await client.get(url)
                if response.status_code == 401:
                    raise PermissionError(
                        f"Authentication failed for Zowe. Check credentials."
                    )
            
            if response.status_code == 403:
                raise PermissionError(
                    f"Access denied to {dsname}({member}). Check RACF permissions."
                )
            
            if response.status_code >= 500:
                error_msg = response.text[:200] if response.text else str(response.status_code)
                raise ConnectionError(
                    f"Zowe server error: {error_msg}"
                )
            
            response.raise_for_status()
            
            # Zowe returns raw content for dataset members
            source_code = response.text
            
            if not source_code:
                raise FileNotFoundError(
                    f"Member '{member}' not found or empty in dataset {dsname}"
                )
            
            logger.info(f"Successfully retrieved '{dsname}({member})' via Zowe")
            
            return ZoweElement(
                name=member,
                dsname=dsname,
                member=member,
                source_code=source_code
            )
            
        except httpx.TimeoutException:
            logger.warning(f"Zowe request timeout after {self._timeout}s")
            raise ConnectionError(
                f"Zowe request timeout after {self._timeout}s"
            )
        except httpx.RequestError as e:
            logger.error(f"Zowe request error: {e}")
            raise ConnectionError(
                f"Error connecting to Zowe: {str(e)}"
            )
        except (FileNotFoundError, PermissionError, ConnectionError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving Zowe member: {e}")
            raise ConnectionError(
                f"Error retrieving member '{dsname}({member})': {str(e)}"
            )
    
    async def list_members(self, dsname: str) -> list[str]:
        """
        List all members in a PDS/PDSE dataset via Zowe.
        
        Args:
            dsname: Dataset name
            
        Returns:
            List of member names
            
        Raises:
            FileNotFoundError: If dataset not found
            PermissionError: If access denied
        """
        client = await self._get_client()
        
        import urllib.parse
        encoded_dsname = urllib.parse.quote(dsname, safe='')
        url = f"{self._base_url}/api/v1/zos-files/dataset/{encoded_dsname}/member-list"
        
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            # Zowe returns member list in 'items' or 'apiResponse'
            items = data.get('items', []) or data.get('apiResponse', {}).get('items', [])
            return [m.get('member', '') for m in items if m.get('member')]
            
        except Exception as e:
            logger.error(f"Error listing members: {e}")
            raise ConnectionError(f"Error listing members in {dsname}: {str(e)}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
        return False


async def create_zowe_client(config: Config) -> ZoweClient:
    """
    Factory function to create Zowe client.
    
    Args:
        config: Configuration with Zowe parameters
        
    Returns:
        Initialized ZoweClient
    """
    client = ZoweClient(config)
    # Authenticate on creation
    await client.authenticate()
    logger.info(f"Created Zowe client for {config.zowe_base_url}")
    return client


__all__ = ["ZoweClient", "ZoweElement", "create_zowe_client"]

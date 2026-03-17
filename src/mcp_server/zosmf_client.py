"""
z/OSMF REST API client for mainframe source code retrieval.

Provides integration with IBM z/OS Management Facility (z/OSMF) REST APIs
for direct dataset and member access without SSH.

Requires: z/OSMF installed on mainframe (standard on modern z/OS)
"""

import logging
import asyncio
from typing import Optional
from dataclasses import dataclass

import httpx

from .config import Config

logger = logging.getLogger(__name__)


@dataclass
class ZosmfElement:
    """Represents a z/OSMF dataset element (program or copybook)."""
    name: str
    dsname: str
    member: str
    source_code: str
    recfm: str = ""
    lrecl: int = 0


class ZosmfClient:
    """
    Client for IBM z/OSMF REST APIs.
    
    Supports:
    - Dataset member retrieval via z/OSMF REST API
    - Authentication via basic auth or certificate
    - Direct dataset access without USS/SSH
    
    Usage:
        client = ZosmfClient(config)
        element = await client.retrieve_member("USER.COBOL.SRC", "PAYROLL")
        print(element.source_code)
    
    References:
    - z/OSMF REST API Guide: https://www.ibm.com/docs/en/zos/2.5.0?topic=services-zosmf-rest-apis
    - Dataset API: https://www.ibm.com/docs/en/zos/2.5.0?topic=interfaces-data-set-file-rest-interface
    """
    
    def __init__(self, config: Config):
        """
        Initialize z/OSMF client.
        
        Args:
            config: Configuration with z/OSMF connection parameters
        """
        self._config = config
        self._base_url = config.zosmf_base_url.rstrip('/')
        self._user = config.zosmf_user
        self._password = config.zosmf_password
        self._verify_cert = config.zosmf_verify_cert  # True for prod, False for dev
        self._timeout = config.connection_timeout
        
        # HTTP client (reused across requests)
        self._client: Optional[httpx.AsyncClient] = None
        
        logger.info(
            f"ZosmfClient initialized: URL={self._base_url}, "
            f"User={self._user}, VerifyCert={self._verify_cert}"
        )
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with authentication."""
        if self._client is None:
            # Configure SSL verification
            if self._verify_cert:
                # Production: verify certificates
                self._client = httpx.AsyncClient(
                    auth=(self._user, self._password),
                    timeout=httpx.Timeout(self._timeout),
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "X-IBM-Attributes": "base"  # z/OSMF specific header
                    }
                )
            else:
                # Development: skip certificate verification (not recommended for prod)
                import ssl
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                self._client = httpx.AsyncClient(
                    auth=(self._user, self._password),
                    timeout=httpx.Timeout(self._timeout),
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "X-IBM-Attributes": "base"
                    },
                    verify=ssl_context
                )
                
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("z/OSMF HTTP client closed")
    
    async def retrieve_member(self, dsname: str, member: str) -> ZosmfElement:
        """
        Retrieve a dataset member via z/OSMF REST API.
        
        Args:
            dsname: Dataset name (e.g., 'USER.COBOL.SRC')
            member: Member name (e.g., 'PAYROLL')
            
        Returns:
            ZosmfElement with source code
            
        Raises:
            FileNotFoundError: If member not found
            PermissionError: If access denied
            ConnectionError: If connection fails
        """
        client = await self._get_client()
        
        # Build z/OSMF REST API URL
        # Format: {base_url}/zosmf/restfiles/ds/{dsname}({member})
        # URL encode special characters
        import urllib.parse
        encoded_dsname = urllib.parse.quote(dsname, safe='')
        url = f"{self._base_url}/zosmf/restfiles/ds/{encoded_dsname}({member})"
        
        # Request content with maximum record length
        params = {
            "record": "Y",  # Return record content
            "maxrecs": "10000"  # Maximum records to return
        }
        
        logger.debug(f"Retrieving z/OSMF member: {url}")
        
        try:
            response = await client.get(url, params=params)
            
            logger.debug(f"z/OSMF response status: {response.status_code}")
            
            # Handle common error cases
            if response.status_code == 404:
                raise FileNotFoundError(
                    f"Member '{member}' not found in dataset {dsname}"
                )
            
            if response.status_code == 401:
                raise PermissionError(
                    f"Authentication failed for z/OSMF. Check credentials."
                )
            
            if response.status_code == 403:
                raise PermissionError(
                    f"Access denied to {dsname}({member}). Check RACF permissions."
                )
            
            if response.status_code >= 500:
                # z/OSMF internal error
                error_msg = response.json().get('reason', {}).get('message', str(response.status_code))
                raise ConnectionError(
                    f"z/OSMF server error: {error_msg}"
                )
            
            response.raise_for_status()
            
            # Parse z/OSMF response
            # z/OSMF returns records in 'items' array with 'data' field (base64 encoded)
            data = response.json()
            source_code = self._parse_zosmf_response(data)
            
            if not source_code:
                raise FileNotFoundError(
                    f"Member '{member}' not found or empty in dataset {dsname}"
                )
            
            logger.info(f"Successfully retrieved '{dsname}({member})' via z/OSMF")
            
            return ZosmfElement(
                name=member,
                dsname=dsname,
                member=member,
                source_code=source_code,
                recfm=data.get('recfm', ''),
                lrecl=data.get('lrecl', 0)
            )
            
        except httpx.TimeoutException:
            logger.warning(f"z/OSMF request timeout after {self._timeout}s")
            raise ConnectionError(
                f"z/OSMF request timeout after {self._timeout}s"
            )
        except httpx.RequestError as e:
            logger.error(f"z/OSMF request error: {e}")
            raise ConnectionError(
                f"Error connecting to z/OSMF: {str(e)}"
            )
        except (FileNotFoundError, PermissionError, ConnectionError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving z/OSMF member: {e}")
            raise ConnectionError(
                f"Error retrieving member '{dsname}({member})': {str(e)}"
            )
    
    def _parse_zosmf_response(self, data: dict) -> str:
        """
        Parse z/OSMF REST API response.
        
        z/OSMF returns records in this format:
        {
          "items": [
            {
              "data": "base64-encoded-record-content",
              "length": 80
            },
            ...
          ],
          "recfm": "FB",
          "lrecl": 80
        }
        
        Args:
            data: Parsed JSON response from z/OSMF
            
        Returns:
            Source code as string (decoded from base64)
        """
        import base64
        
        items = data.get('items', [])
        if not items:
            return ""
        
        lines = []
        for item in items:
            # z/OSMF returns data as base64-encoded strings
            encoded_data = item.get('data', '')
            if encoded_data:
                try:
                    # Decode base64
                    decoded = base64.b64decode(encoded_data).decode('utf-8', errors='replace')
                    lines.append(decoded)
                except Exception as e:
                    logger.warning(f"Failed to decode record: {e}")
                    # Fallback: try to use data as-is
                    lines.append(encoded_data)
        
        return '\n'.join(lines)
    
    async def list_members(self, dsname: str) -> list[str]:
        """
        List all members in a PDS/PDSE dataset.
        
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
        url = f"{self._base_url}/zosmf/restfiles/ds/{encoded_dsname}/member"
        
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            members = data.get('items', [])
            return [m.get('member', '') for m in members if m.get('member')]
            
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


async def create_zosmf_client(config: Config) -> ZosmfClient:
    """
    Factory function to create z/OSMF client.
    
    Args:
        config: Configuration with z/OSMF parameters
        
    Returns:
        Initialized ZosmfClient
    """
    client = ZosmfClient(config)
    logger.info(f"Created z/OSMF client for {config.zosmf_base_url}")
    return client


__all__ = ["ZosmfClient", "ZosmfElement", "create_zosmf_client"]

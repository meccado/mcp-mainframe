"""
Endevor API client for mainframe source code retrieval.

Provides integration with CA Endevor Software Change Manager via REST API.
More robust than SSH for environments with Endevor installed.
"""

import logging
import asyncio
from typing import Optional
from dataclasses import dataclass

import httpx

from .config import Config

logger = logging.getLogger(__name__)


@dataclass
class EndevorElement:
    """Represents an Endevor element (program or copybook)."""
    name: str
    system: str
    subsystem: str
    stage: str
    type: str
    source_code: str


class EndevorClient:
    """
    Client for CA Endevor API web services.
    
    Supports:
    - Element retrieval (source code)
    - Authentication via basic auth or token
    - Configurable stage (PROD, TEST, DEV, etc.)
    
    Usage:
        client = EndevorClient(config)
        element = await client.retrieve_element("PAYROLL", "COBOL")
        print(element.source_code)
    """
    
    def __init__(self, config: Config):
        """
        Initialize Endevor client.
        
        Args:
            config: Configuration with Endevor connection parameters
        """
        self._config = config
        self._base_url = config.endevor_base_url.rstrip('/')
        self._user = config.endevor_user
        self._password = config.endevor_password
        self._stage = config.endevor_stage
        self._timeout = config.connection_timeout
        
        # HTTP client (reused across requests)
        self._client: Optional[httpx.AsyncClient] = None
        
        logger.info(
            f"EndevorClient initialized: URL={self._base_url}, "
            f"User={self._user}, Stage={self._stage}"
        )
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with authentication."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                auth=(self._user, self._password),
                timeout=httpx.Timeout(self._timeout),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("Endevor HTTP client closed")
    
    async def retrieve_element(
        self,
        element_name: str,
        element_type: str = "COBOL"
    ) -> EndevorElement:
        """
        Retrieve an element from Endevor.
        
        Args:
            element_name: Name of the element (program or copybook)
            element_type: Endevor element type (e.g., "COBOL", "COPY")
            
        Returns:
            EndevorElement with source code
            
        Raises:
            FileNotFoundError: If element not found
            PermissionError: If access denied
            ConnectionError: If connection fails
        """
        client = await self._get_client()
        
        # Build Endevor API URL
        # Standard Endevor REST API pattern:
        # /api/v1/systems/{system}/subsystems/{subsystem}/stages/{stage}/types/{type}/elements/{element}
        # Adjust based on your Endevor configuration
        
        url = f"{self._base_url}/elements/{element_name}"
        params = {
            "stage": self._stage,
            "type": element_type,
            "view": "source"  # Request source code view
        }
        
        logger.debug(f"Retrieving Endevor element: {url} with params {params}")
        
        try:
            response = await client.get(url, params=params)
            
            logger.debug(f"Endevor response status: {response.status_code}")
            
            # Handle common error cases
            if response.status_code == 404:
                raise FileNotFoundError(
                    f"Element '{element_name}' not found in Endevor stage {self._stage}"
                )
            
            if response.status_code == 401:
                raise PermissionError(
                    f"Authentication failed for Endevor. Check ENDEVOR_USER and ENDEVOR_PASSWORD"
                )
            
            if response.status_code == 403:
                raise PermissionError(
                    f"Access denied to element '{element_name}'. Check Endevor security settings"
                )
            
            if response.status_code >= 500:
                raise ConnectionError(
                    f"Endevor server error: {response.status_code}"
                )
            
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Extract source code from response
            # Endevor API response format varies by configuration
            # Common patterns:
            source_code = self._extract_source_code(data, element_name)
            
            if not source_code:
                raise FileNotFoundError(
                    f"Element '{element_name}' not found or has no source in stage {self._stage}"
                )
            
            logger.info(f"Successfully retrieved '{element_name}' from Endevor")
            
            return EndevorElement(
                name=element_name,
                system=data.get("system", "UNKNOWN"),
                subsystem=data.get("subsystem", "UNKNOWN"),
                stage=self._stage,
                type=element_type,
                source_code=source_code
            )
            
        except httpx.TimeoutException:
            logger.warning(f"Endevor request timeout after {self._timeout}s")
            raise ConnectionError(
                f"Endevor request timeout after {self._timeout}s. Try again or check mainframe availability"
            )
        except httpx.RequestError as e:
            logger.error(f"Endevor request error: {e}")
            raise ConnectionError(
                f"Error connecting to Endevor: {str(e)}"
            )
        except (FileNotFoundError, PermissionError, ConnectionError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving Endevor element: {e}")
            raise ConnectionError(
                f"Error retrieving element '{element_name}': {str(e)}"
            )
    
    def _extract_source_code(self, data: dict, element_name: str) -> str:
        """
        Extract source code from Endevor API response.
        
        Endevor API response format varies by configuration.
        Common patterns:
        - {"element": {"source": "..."}}
        - {"data": {"content": "..."}}
        - {"sourceCode": "..."}
        - Direct string response
        
        Args:
            data: Parsed JSON response
            element_name: Element name (for error messages)
            
        Returns:
            Source code as string
        """
        # Try common response patterns
        if "source" in data:
            return data["source"]
        
        if "sourceCode" in data:
            return data["sourceCode"]
        
        if "content" in data:
            return data["content"]
        
        if "element" in data and isinstance(data["element"], dict):
            element_data = data["element"]
            if "source" in element_data:
                return element_data["source"]
            if "contents" in element_data:
                return element_data["contents"]
        
        if "data" in data and isinstance(data["data"], dict):
            data_content = data["data"]
            if "source" in data_content:
                return data_content["source"]
            if "content" in data_content:
                return data_content["content"]
        
        # Check if response is already a string
        if isinstance(data, str):
            return data
        
        logger.warning(
            f"Unknown Endevor response format for '{element_name}': {list(data.keys()) if isinstance(data, dict) else type(data)}"
        )
        return ""
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
        return False


async def create_endevor_client(config: Config) -> EndevorClient:
    """
    Factory function to create Endevor client.
    
    Args:
        config: Configuration with Endevor parameters
        
    Returns:
        Initialized EndevorClient
    """
    client = EndevorClient(config)
    logger.info(f"Created Endevor client for {config.endevor_base_url}")
    return client


__all__ = ["EndevorClient", "EndevorElement", "create_endevor_client"]

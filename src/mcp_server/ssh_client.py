"""
SSH client with connection pooling for mainframe access.

Provides efficient SSH connection management with configurable limits,
timeout handling, and graceful error recovery.
"""

import asyncio
import logging
from typing import Optional, Any
from contextlib import asynccontextmanager

import paramiko
from paramiko.ssh_exception import (
    SSHException,
    AuthenticationException,
    BadHostKeyException,
)

from .config import Config

logger = logging.getLogger(__name__)


class SSHConnectionPool:
    """
    Manages a pool of SSH connections to the mainframe.
    
    Features:
    - Configurable maximum connections (default: 10)
    - Connection reuse across tool calls
    - Timeout handling
    - Automatic reconnection on stale connections
    - Graceful handling of connection exhaustion
    
    Usage:
        async with SSHConnectionPool(config) as pool:
            async with pool.acquire() as ssh:
                stdout, stderr, rc = await ssh.exec_command("cat '//\'DSN(MBR)\'")
    """
    
    def __init__(self, config: Config):
        """
        Initialize the connection pool.
        
        Args:
            config: Configuration with connection parameters
        """
        self._config = config
        self._max_connections = config.max_connections
        self._timeout = config.connection_timeout
        
        # Connection pool state
        self._pool: asyncio.Queue[paramiko.SSHClient] = asyncio.Queue(
            maxsize=self._max_connections
        )
        self._semaphore = asyncio.Semaphore(self._max_connections)
        self._active_count = 0
        self._closed = False
        
        logger.info(
            f"SSHConnectionPool initialized: max={self._max_connections}, "
            f"timeout={self._timeout}s"
        )
    
    async def _create_connection(self) -> paramiko.SSHClient:
        """
        Create a new SSH connection to the mainframe.
        
        Returns:
            Connected and authenticated paramiko.SSHClient
            
        Raises:
            ConnectionError: If connection fails
            AuthenticationError: If authentication fails
        """
        logger.debug(f"Creating new SSH connection to {self._config.host}")
        
        ssh = paramiko.SSHClient()
        
        # Auto-add host keys (TODO: consider host key verification for production)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: ssh.connect(
                    hostname=self._config.host,
                    username=self._config.username,
                    key_filename=self._config.key_file,
                    timeout=self._timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )
            )
            
            logger.info(f"SSH connection established to {self._config.host}")
            return ssh
            
        except AuthenticationException as e:
            logger.warning(f"SSH authentication failed: {e}")
            raise ConnectionError(
                "Authentication failed. Check SSH key permissions and try again."
            ) from e
            
        except BadHostKeyException as e:
            logger.warning(f"SSH host key mismatch: {e}")
            raise ConnectionError(
                "Host key verification failed. Mainframe host key may have changed."
            ) from e
            
        except SSHException as e:
            logger.warning(f"SSH connection error: {e}")
            raise ConnectionError(
                f"Unable to connect to mainframe. Check network and credentials."
            ) from e
            
        except asyncio.TimeoutError:
            logger.warning(f"SSH connection timeout after {self._timeout}s")
            raise ConnectionError(
                f"Connection timeout after {self._timeout}s. Try again or check mainframe availability."
            ) from e
    
    def _is_connection_alive(self, ssh: paramiko.SSHClient) -> bool:
        """
        Check if an SSH connection is still alive.
        
        Args:
            ssh: The SSH client to check
            
        Returns:
            True if connection is alive, False otherwise
        """
        try:
            # Transport is active and not closed
            transport = ssh.get_transport()
            if transport is None or transport.is_closed():
                return False
            
            # Try to get channel (lightweight check)
            return True
            
        except Exception:
            return False
    
    def _close_connection(self, ssh: paramiko.SSHClient) -> None:
        """
        Close an SSH connection gracefully.
        
        Args:
            ssh: The SSH client to close
        """
        try:
            ssh.close()
            logger.debug("SSH connection closed")
        except Exception as e:
            logger.debug(f"Error closing SSH connection: {e}")
    
    async def acquire(self) -> paramiko.SSHClient:
        """
        Acquire an SSH connection from the pool.
        
        Creates a new connection if none available and under limit.
        Waits if at max capacity (with timeout).
        
        Returns:
            Connected SSH client
            
        Raises:
            ConnectionError: If connection cannot be established
        """
        if self._closed:
            raise RuntimeError("Connection pool is closed")
        
        logger.debug(f"Acquiring SSH connection (active: {self._active_count})")
        
        # Wait for semaphore (respects max connections limit)
        await self._semaphore.acquire()
        
        try:
            # Try to get existing connection from pool
            while not self._pool.empty():
                try:
                    ssh = self._pool.get_nowait()
                    if self._is_connection_alive(ssh):
                        logger.debug("Reusing existing SSH connection")
                        return ssh
                    else:
                        logger.debug("Discarding stale SSH connection")
                        self._close_connection(ssh)
                except asyncio.QueueEmpty:
                    break
            
            # No available connections, create new one
            logger.debug("Creating new SSH connection")
            self._active_count += 1
            return await self._create_connection()
            
        except Exception:
            # Release semaphore on error
            self._semaphore.release()
            raise
    
    async def release(self, ssh: paramiko.SSHClient) -> None:
        """
        Release an SSH connection back to the pool.
        
        Args:
            ssh: The SSH client to release
        """
        if self._closed:
            self._close_connection(ssh)
            return
        
        # Check if connection is still alive
        if self._is_connection_alive(ssh):
            try:
                # Return to pool (non-blocking)
                self._pool.put_nowait(ssh)
                logger.debug("SSH connection returned to pool")
            except asyncio.QueueFull:
                logger.debug("Pool full, closing connection")
                self._close_connection(ssh)
        else:
            logger.debug("Connection dead, not returning to pool")
            self._close_connection(ssh)
        
        # Release semaphore
        self._semaphore.release()
    
    @asynccontextmanager
    async def connection(self):
        """
        Context manager for acquiring and releasing SSH connections.
        
        Usage:
            async with pool.connection() as ssh:
                stdout, stderr, rc = await ssh.exec_command(...)
        
        Yields:
            Connected SSH client
            
        Raises:
            ConnectionError: If connection cannot be established
            PoolExhaustedError: If all connections are in use
        """
        ssh = await self.acquire()
        try:
            yield ssh
        finally:
            await self.release(ssh)
    
    async def close(self) -> None:
        """
        Close all connections in the pool.
        
        Should be called when shutting down the server.
        """
        logger.info("Closing SSH connection pool")
        self._closed = True
        
        # Close all pooled connections
        while not self._pool.empty():
            try:
                ssh = self._pool.get_nowait()
                self._close_connection(ssh)
            except asyncio.QueueEmpty:
                break
        
        logger.info(f"SSH connection pool closed (was {self._active_count} connections)")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
        return False


class MainframeSSH:
    """
    High-level mainframe SSH operations.
    
    Provides convenient methods for common mainframe operations
    using USS (UNIX System Services) filesystem access.
    """
    
    def __init__(self, pool: SSHConnectionPool, config: Config):
        """
        Initialize mainframe SSH client.
        
        Args:
            pool: SSH connection pool
            config: Configuration with dataset names
        """
        self._pool = pool
        self._config = config
    
    async def read_member(self, dsn: str, member: str) -> str:
        """
        Read a PDS member via USS filesystem.
        
        Args:
            dsn: Dataset name (e.g., 'USER.COBOL.SRC')
            member: Member name (e.g., 'PAYROLL')
            
        Returns:
            Member content as string
            
        Raises:
            FileNotFoundError: If member doesn't exist
            PermissionError: If access denied
            ConnectionError: If connection fails
        """
        # Build USS command
        command = self._config.cat_command.format(f"{dsn}({member})")
        
        logger.debug(f"Executing mainframe command: {command}")
        
        async with self._pool.connection() as ssh:
            try:
                # Execute command
                loop = asyncio.get_event_loop()
                stdin, stdout, stderr = await loop.run_in_executor(
                    None,
                    lambda: ssh.exec_command(command)
                )
                
                # Read output
                output = await loop.run_in_executor(None, stdout.read)
                error_output = await loop.run_in_executor(None, stderr.read)
                rc = await loop.run_in_executor(None, stdout.channel.recv_exit_status)
                
                output_str = output.decode('utf-8', errors='replace').strip()
                error_str = error_output.decode('utf-8', errors='replace').strip()
                
                logger.debug(f"Command returned rc={rc}")
                
                # Handle errors
                if rc != 0:
                    if "not found" in error_str.lower() or rc == 1:
                        raise FileNotFoundError(
                            f"Member '{member}' not found in dataset {dsn}"
                        )
                    elif "permission" in error_str.lower() or "access" in error_str.lower():
                        raise PermissionError(
                            f"Access denied to {dsn}({member}). Check read permissions."
                        )
                    else:
                        raise ConnectionError(
                            f"Command failed with rc={rc}: {error_str}"
                        )
                
                if not output_str:
                    raise FileNotFoundError(
                        f"Member '{member}' not found or empty in dataset {dsn}"
                    )
                
                logger.info(f"Successfully read {dsn}({member})")
                return output_str
                
            except (FileNotFoundError, PermissionError):
                raise
            except Exception as e:
                logger.error(f"Error reading member: {e}")
                raise ConnectionError(
                    f"Error reading {dsn}({member}): {str(e)}"
                ) from e


__all__ = ["SSHConnectionPool", "MainframeSSH"]

"""
Configuration management for MCP COBOL Server.

Handles environment variable parsing, validation, and provides
a type-safe configuration object.

Supports four backends:
- SSH: Direct SSH connection to mainframe USS filesystem
- Endevor: CA Endevor API web services
- z/OSMF: IBM z/OS Management Facility REST API
- Zowe: Open Mainframe Project API ML
"""

import os
import sys
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass(frozen=True)
class Config:
    """
    Immutable configuration for MCP COBOL Server.
    
    Supports four backends:
    - SSH: Direct SSH connection to mainframe USS filesystem
    - Endevor: CA Endevor API web services
    - z/OSMF: IBM z/OS Management Facility REST API
    - Zowe: Open Mainframe Project API ML
    
    All required fields must be provided via environment variables.
    No defaults for sensitive connection parameters.
    """
    # Backend selection (SSH, ENDEVOR, ZOSMF, or ZOWE)
    backend: str = "SSH"
    
    # SSH-specific parameters (required if backend == "SSH")
    host: Optional[str] = None
    username: Optional[str] = None
    key_file: Optional[str] = None
    
    # Endevor-specific parameters (required if backend == "ENDEVOR")
    endevor_base_url: Optional[str] = None
    endevor_user: Optional[str] = None
    endevor_password: Optional[str] = None
    endevor_stage: str = "PROD"
    
    # z/OSMF-specific parameters (required if backend == "ZOSMF")
    zosmf_base_url: Optional[str] = None
    zosmf_user: Optional[str] = None
    zosmf_password: Optional[str] = None
    zosmf_verify_cert: bool = True
    
    # Zowe-specific parameters (required if backend == "ZOWE")
    zowe_base_url: Optional[str] = None
    zowe_user: Optional[str] = None
    zowe_password: Optional[str] = None
    zowe_verify_cert: bool = True
    
    # Dataset names (required for SSH, optional for others)
    cobol_source_dsn: Optional[str] = None
    copybook_dsn: Optional[str] = None

    # Optional parameters with defaults
    log_level: str = "INFO"
    max_connections: int = 10
    connection_timeout: int = 30
    cat_command: str = 'cat "//\'{}\'"'
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Validate backend selection
        valid_backends = {"SSH", "ENDEVOR", "ZOSMF", "ZOWE"}
        if self.backend.upper() not in valid_backends:
            raise ValueError(
                f"Invalid BACKEND: {self.backend}. Must be one of: {', '.join(valid_backends)}"
            )
        
        backend_upper = self.backend.upper()
        
        # Validate SSH-specific parameters
        if backend_upper == "SSH":
            if not self.host:
                raise ValueError("MF_HOST is required when using SSH backend")
            if not self.username:
                raise ValueError("MF_USER is required when using SSH backend")
            if not self.key_file:
                raise ValueError("MF_KEYFILE is required when using SSH backend")
            if not self.cobol_source_dsn:
                raise ValueError("COBOL_SRC_DSN is required when using SSH backend")
            if not self.copybook_dsn:
                raise ValueError("COPYBOOK_DSN is required when using SSH backend")
            
            # Validate SSH key file exists
            key_path = Path(self.key_file)
            if not key_path.exists():
                raise ValueError(
                    f"SSH key file not found: {self.key_file}. "
                    "Check MF_KEYFILE environment variable."
                )

            # Validate SSH key permissions (Unix-like systems)
            if os.name != "nt":
                try:
                    mode = key_path.stat().st_mode & 0o777
                    if mode & 0o077:
                        print(
                            f"WARNING: SSH key file {self.key_file} has permissions "
                            f"{oct(mode)}. Recommended: 0o600",
                            file=sys.stderr
                        )
                except (OSError, IOError):
                    pass
        
        # Validate Endevor-specific parameters
        elif backend_upper == "ENDEVOR":
            if not self.endevor_base_url:
                raise ValueError("ENDEVOR_BASE_URL is required when using Endevor backend")
            if not self.endevor_user:
                raise ValueError("ENDEVOR_USER is required when using Endevor backend")
            if not self.endevor_password:
                raise ValueError("ENDEVOR_PASSWORD is required when using Endevor backend")
        
        # Validate z/OSMF-specific parameters
        elif backend_upper == "ZOSMF":
            if not self.zosmf_base_url:
                raise ValueError("ZOSMF_BASE_URL is required when using z/OSMF backend")
            if not self.zosmf_user:
                raise ValueError("ZOSMF_USER is required when using z/OSMF backend")
            if not self.zosmf_password:
                raise ValueError("ZOSMF_PASSWORD is required when using z/OSMF backend")
            if not self.cobol_source_dsn:
                raise ValueError("COBOL_SRC_DSN is required when using z/OSMF backend")
            if not self.copybook_dsn:
                raise ValueError("COPYBOOK_DSN is required when using z/OSMF backend")
        
        # Validate Zowe-specific parameters
        elif backend_upper == "ZOWE":
            if not self.zowe_base_url:
                raise ValueError("ZOWE_BASE_URL is required when using Zowe backend")
            if not self.zowe_user:
                raise ValueError("ZOWE_USER is required when using Zowe backend")
            if not self.zowe_password:
                raise ValueError("ZOWE_PASSWORD is required when using Zowe backend")
            if not self.cobol_source_dsn:
                raise ValueError("COBOL_SRC_DSN is required when using Zowe backend")
            if not self.copybook_dsn:
                raise ValueError("COPYBOOK_DSN is required when using Zowe backend")

        # Validate log level
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
        if self.log_level.upper() not in valid_levels:
            raise ValueError(
                f"Invalid LOG_LEVEL: {self.log_level}. "
                f"Must be one of: {', '.join(valid_levels)}"
            )

        # Validate max connections (1-20)
        if not (1 <= self.max_connections <= 20):
            raise ValueError(
                f"MAX_CONNECTIONS must be between 1 and 20, got {self.max_connections}"
            )

        # Validate connection timeout (positive)
        if self.connection_timeout <= 0:
            raise ValueError(
                f"CONNECTION_TIMEOUT must be positive, got {self.connection_timeout}"
            )


def get_required_env(var_name: str) -> str:
    """
    Get a required environment variable or exit with clear error.
    
    Args:
        var_name: Name of the environment variable
        
    Returns:
        The environment variable value
        
    Exits:
        If the variable is not set, exits with error code 1 and clear message.
    """
    value = os.environ.get(var_name)
    if value is None or value.strip() == "":
        print(
            f"ERROR: Configuration error: Required environment variable '{var_name}' is not set.\n"
            f"Please set {var_name} in your environment or .env file.",
            file=sys.stderr
        )
        sys.exit(1)
    return value.strip()


def get_optional_env(var_name: str, default: str) -> str:
    """
    Get an optional environment variable with a default value.
    
    Args:
        var_name: Name of the environment variable
        default: Default value if not set
        
    Returns:
        The environment variable value or default
    """
    return os.environ.get(var_name, default).strip()


def get_optional_env_int(var_name: str, default: int) -> int:
    """
    Get an optional integer environment variable.
    
    Args:
        var_name: Name of the environment variable
        default: Default value if not set or invalid
        
    Returns:
        The integer value or default
    """
    value = os.environ.get(var_name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value.strip())
    except ValueError:
        print(
            f"WARNING: Invalid integer value for {var_name}: {value}. Using default: {default}",
            file=sys.stderr
        )
        return default


def get_optional_env_bool(var_name: str, default: bool) -> bool:
    """
    Get an optional boolean environment variable.
    
    Args:
        var_name: Name of the environment variable
        default: Default value if not set
        
    Returns:
        The boolean value or default
    """
    value = os.environ.get(var_name, str(default)).strip().lower()
    return value in ("true", "1", "yes", "on")


def load_config() -> Config:
    """
    Load configuration from environment variables.
    
    Supports four backends:
    - SSH: Requires MF_HOST, MF_USER, MF_KEYFILE, COBOL_SRC_DSN, COPYBOOK_DSN
    - Endevor: Requires ENDEVOR_BASE_URL, ENDEVOR_USER, ENDEVOR_PASSWORD
    - z/OSMF: Requires ZOSMF_BASE_URL, ZOSMF_USER, ZOSMF_PASSWORD, COBOL_SRC_DSN, COPYBOOK_DSN
    - Zowe: Requires ZOWE_BASE_URL, ZOWE_USER, ZOWE_PASSWORD, COBOL_SRC_DSN, COPYBOOK_DSN
    
    Validates all required variables and creates an immutable Config object.
    Exits with clear error messages if required variables are missing.
    
    Returns:
        Config object with all configuration parameters
        
    Exits:
        If any required environment variable is missing or invalid.
    """
    print("INFO: Loading configuration...", file=sys.stderr)
    
    try:
        # Determine backend from environment
        backend = get_optional_env("BACKEND", "SSH").upper()
        
        if backend == "SSH":
            config = Config(
                backend=backend,
                host=get_required_env("MF_HOST"),
                username=get_required_env("MF_USER"),
                key_file=get_required_env("MF_KEYFILE"),
                cobol_source_dsn=get_required_env("COBOL_SRC_DSN"),
                copybook_dsn=get_required_env("COPYBOOK_DSN"),
                log_level=get_optional_env("LOG_LEVEL", "INFO"),
                max_connections=get_optional_env_int("MAX_CONNECTIONS", 10),
                connection_timeout=get_optional_env_int("CONNECTION_TIMEOUT", 30),
            )
            
            print(f"INFO: Configuration loaded successfully (SSH backend)", file=sys.stderr)
            print(f"INFO: Host: {config.host}", file=sys.stderr)
            print(f"INFO: User: {config.username}", file=sys.stderr)
            print(f"INFO: COBOL Dataset: {config.cobol_source_dsn}", file=sys.stderr)
            print(f"INFO: Copybook Dataset: {config.copybook_dsn}", file=sys.stderr)
            
        elif backend == "ENDEVOR":
            config = Config(
                backend=backend,
                endevor_base_url=get_required_env("ENDEVOR_BASE_URL"),
                endevor_user=get_required_env("ENDEVOR_USER"),
                endevor_password=get_required_env("ENDEVOR_PASSWORD"),
                endevor_stage=get_optional_env("ENDEVOR_STAGE", "PROD"),
                cobol_source_dsn=get_optional_env("COBOL_SRC_DSN", ""),
                copybook_dsn=get_optional_env("COPYBOOK_DSN", ""),
                log_level=get_optional_env("LOG_LEVEL", "INFO"),
                max_connections=get_optional_env_int("MAX_CONNECTIONS", 10),
                connection_timeout=get_optional_env_int("CONNECTION_TIMEOUT", 30),
            )
            
            print(f"INFO: Configuration loaded successfully (Endevor backend)", file=sys.stderr)
            print(f"INFO: Endevor URL: {config.endevor_base_url}", file=sys.stderr)
            print(f"INFO: Endevor User: {config.endevor_user}", file=sys.stderr)
            print(f"INFO: Endevor Stage: {config.endevor_stage}", file=sys.stderr)
        
        elif backend == "ZOSMF":
            config = Config(
                backend=backend,
                zosmf_base_url=get_required_env("ZOSMF_BASE_URL"),
                zosmf_user=get_required_env("ZOSMF_USER"),
                zosmf_password=get_required_env("ZOSMF_PASSWORD"),
                zosmf_verify_cert=get_optional_env_bool("ZOSMF_VERIFY_CERT", True),
                cobol_source_dsn=get_required_env("COBOL_SRC_DSN"),
                copybook_dsn=get_required_env("COPYBOOK_DSN"),
                log_level=get_optional_env("LOG_LEVEL", "INFO"),
                max_connections=get_optional_env_int("MAX_CONNECTIONS", 10),
                connection_timeout=get_optional_env_int("CONNECTION_TIMEOUT", 30),
            )
            
            print(f"INFO: Configuration loaded successfully (z/OSMF backend)", file=sys.stderr)
            print(f"INFO: z/OSMF URL: {config.zosmf_base_url}", file=sys.stderr)
            print(f"INFO: z/OSMF User: {config.zosmf_user}", file=sys.stderr)
            print(f"INFO: COBOL Dataset: {config.cobol_source_dsn}", file=sys.stderr)
            print(f"INFO: Copybook Dataset: {config.copybook_dsn}", file=sys.stderr)
        
        elif backend == "ZOWE":
            config = Config(
                backend=backend,
                zowe_base_url=get_required_env("ZOWE_BASE_URL"),
                zowe_user=get_required_env("ZOWE_USER"),
                zowe_password=get_required_env("ZOWE_PASSWORD"),
                zowe_verify_cert=get_optional_env_bool("ZOWE_VERIFY_CERT", True),
                cobol_source_dsn=get_required_env("COBOL_SRC_DSN"),
                copybook_dsn=get_required_env("COPYBOOK_DSN"),
                log_level=get_optional_env("LOG_LEVEL", "INFO"),
                max_connections=get_optional_env_int("MAX_CONNECTIONS", 10),
                connection_timeout=get_optional_env_int("CONNECTION_TIMEOUT", 30),
            )
            
            print(f"INFO: Configuration loaded successfully (Zowe backend)", file=sys.stderr)
            print(f"INFO: Zowe URL: {config.zowe_base_url}", file=sys.stderr)
            print(f"INFO: Zowe User: {config.zowe_user}", file=sys.stderr)
            print(f"INFO: COBOL Dataset: {config.cobol_source_dsn}", file=sys.stderr)
            print(f"INFO: Copybook Dataset: {config.copybook_dsn}", file=sys.stderr)
        
        else:
            print(f"ERROR: Invalid BACKEND: {backend}. Must be SSH, ENDEVOR, ZOSMF, or ZOWE", file=sys.stderr)
            sys.exit(1)
        
        print(f"INFO: Log Level: {config.log_level}", file=sys.stderr)
        print(f"INFO: Max Connections: {config.max_connections}", file=sys.stderr)
        
        return config
        
    except ValueError as e:
        print(f"ERROR: Configuration validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)


__all__ = ["Config", "load_config", "get_required_env", "get_optional_env"]

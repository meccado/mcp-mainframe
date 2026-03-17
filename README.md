# MCP COBOL Server

Retrieve COBOL source code and copybooks from z/OS mainframe datasets via the Model Context Protocol (MCP).

## Overview

This MCP server provides AI assistants (via Continue.dev) with direct access to COBOL programs and copybooks stored on IBM z/OS mainframes. It supports two backends:

- **SSH**: Direct SSH connection to mainframe USS filesystem
- **Endevor**: CA Endevor API web services (more robust, recommended if available)

Both backends provide secure, read-only source retrieval with configurable connection pooling and comprehensive error handling.

## Features

- **Dual Backend Support**: Choose between SSH or Endevor based on your environment
- **`get_cobol_source`**: Retrieve COBOL program source by name
- **`get_copybook`**: Retrieve copybook (data structure) source by name
- **MCP Resources**: Expose frequently accessed programs and copybooks
- **VS Code Native Integration**: Works with built-in MCP support (no extensions required)
- **SSH Connection Pooling**: Efficient connection reuse (configurable limit: 5-10)
- **Endevor HTTP Client**: Reusable HTTP client with authentication
- **Secure Configuration**: All credentials via environment variables
- **Error Handling**: User-friendly error messages, no credential exposure
- **Configurable Logging**: DEBUG, INFO, WARNING, ERROR levels

## Prerequisites

- **Python 3.10+**
- **For SSH backend**:
  - SSH access to z/OS mainframe with USS (UNIX System Services)
  - Read permissions on COBOL source and copybook datasets
- **For Endevor backend**:
  - CA Endevor Software Change Manager installed
  - Endevor web services API access
  - Endevor user credentials
- **VS Code** with **GitHub Copilot** extension (for AI integration)
- **VS Code MCP support**: Built-in (VS Code 1.95+ or Insiders)

## Installation

You can install and run the MCP COBOL Server in two ways:

### Option A: Local Installation (Traditional)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp-mainframe
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv

   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Enable MCP in VS Code** (VS Code 1.95+ or Insiders):
   - Open Settings (`Ctrl+,` or `Cmd+,`)
   - Search for `chat.mcp.enabled`
   - Check the box to enable MCP
   - The repository includes `.vscode/mcp.json` which VS Code will auto-detect

### Option B: Docker Deployment (Recommended for Teams)

**Prerequisites**: Docker and Docker Compose installed on your system.

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp-mainframe
   ```

2. **Configure environment**:
   ```bash
   # Copy Docker environment template
   cp .env.docker .env
   
   # Edit .env with your mainframe credentials
   # For SSH backend: Ensure SSH key is accessible
   ```

3. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Verify container is running**:
   ```bash
   docker-compose ps
   ```

5. **View logs**:
   ```bash
   docker-compose logs -f mcp-cobol-server
   ```

**For SSH Backend**: Mount your SSH key as a volume:
```yaml
# In docker-compose.yml, uncomment and configure:
volumes:
  - ~/.ssh/id_rsa:/app/ssh_keys/id_rsa:ro
```

**For Endevor Backend**: No special volume configuration needed.

**Stop the server**:
```bash
docker-compose down
```

## Configuration

Copy `.env.example` to `.env` and fill in your connection details:

### Option 1: SSH Backend

```bash
# Backend selection
BACKEND=SSH

# Mainframe connection (Required for SSH)
MF_HOST=zos.yourcompany.com
MF_USER=YOURUSERID
MF_KEYFILE=/path/to/your/private/ssh/key

# Dataset names (Required for SSH)
COBOL_SRC_DSN=YOUR.COBOL.SRC
COPYBOOK_DSN=YOUR.COPYBOOK

# Optional configuration
LOG_LEVEL=INFO
MAX_CONNECTIONS=10
CONNECTION_TIMEOUT=30
```

### Option 2: Endevor Backend (Recommended if available)

```bash
# Backend selection
BACKEND=ENDEVOR

# Endevor API configuration (Required for Endevor)
ENDEVOR_BASE_URL=https://endevor.yourcompany.com/api/v1
ENDEVOR_USER=YOURUSERID
ENDEVOR_PASSWORD=your_password_or_access_token

# Endevor stage (Optional, default: PROD)
ENDEVOR_STAGE=PROD

# Dataset names are optional with Endevor (used for logging only)
# COBOL_SRC_DSN=YOUR.COBOL.SRC
# COPYBOOK_DSN=YOUR.COPYBOOK
```

**Security Notes**:
- Never commit `.env` file to version control (it's in `.gitignore`)
- SSH key file should have permissions `600` (read/write for owner only)
- Use SSH key authentication (passwords not supported)
- For Endevor, consider using access tokens instead of passwords
- Rotate credentials regularly according to your organization's policy

### Backend Comparison

| Feature | SSH Backend | Endevor Backend |
|---------|-------------|-----------------|
| **Setup Complexity** | Simple | Moderate |
| **Robustness** | Good | Excellent |
| **Error Recovery** | Manual | Automatic |
| **Performance** | Fast | Fast |
| **Security** | SSH keys | API authentication |
| **Recommended For** | Direct mainframe access | Enterprise environments with Endevor |

**Note**: If your organization uses CA Endevor for change management, the Endevor backend is recommended as it integrates with your existing change control processes and provides better error recovery.

## MCP Resources

The server exposes **MCP Resources** for frequently accessed programs and copybooks. Resources allow MCP clients to discover and read data directly without invoking tools.

### Available Resources

- **`cobol://metadata`**: Server metadata and configuration (JSON)
- **`cobol://status`**: Current server status (JSON)
- **`cobol://program/{name}`**: Frequently accessed program metadata
- **`cobol://copybook/{name}`**: Frequently accessed copybook metadata

### Configuration

Add frequently accessed programs and copybooks to your `.env` file:

```bash
# Frequently accessed programs (comma-separated)
FREQUENT_PROGRAMS=PAYROLL,BILLING,CUSTUPD,INVOICE

# Frequently accessed copybooks (comma-separated)
FREQUENT_COPYBOOKS=CUST-REC,ORDER-REC,COMMON1,DATEFLDS
```

### Usage

MCP clients can discover resources via `list_resources()` and read them via `read_resource(uri)`.

**Example**: Read server metadata
```
Resource URI: cobol://metadata
Response: { "server": "MCP COBOL Server", "version": "1.0.0", "backend": "SSH", ... }
```

**Note**: Resources provide metadata only. To retrieve actual source code, use the `get_cobol_source` or `get_copybook` tools.

## Usage with VS Code and GitHub Copilot

This MCP server integrates natively with **VS Code** and **GitHub Copilot** using the built-in MCP support (no Continue.dev extension required).

### Quick Setup

1. **Enable MCP in VS Code**:
   - Open VS Code settings (`Ctrl+,` or `Cmd+,`)
   - Search for `chat.mcp.enabled`
   - Check the box to enable MCP

2. **Use the provided configuration**:
   - The repository includes `.vscode/mcp.json` with pre-configured settings
   - VS Code will automatically detect and load MCP servers from this file

3. **Configure your credentials**:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your mainframe connection details
   - Or update `.vscode/mcp.json` directly with your credentials

### Alternative: Endevor Backend

If using the Endevor backend, use the provided template:

```bash
# Copy the Endevor configuration
cp .vscode/mcp.endevor.json .vscode/mcp.json
```

Then edit `.vscode/mcp.json` with your Endevor credentials.

### Using MCP Tools in Copilot

Once configured:

1. **Open Copilot Chat** (`Ctrl+Alt+I` or `Cmd+Alt+I`)
2. **Select Agent Mode** from the dropdown at the top
3. **Click the Tools button** (🔧 icon) – your MCP tools should appear:
   - `get_cobol_source` - Retrieve COBOL program source
   - `get_copybook` - Retrieve copybook source
4. **Ask questions** like:
   - "Show me the source for program PAYROLL"
   - "Get the CUST-REC copybook and explain the fields"
   - "Using get_cobol_source, retrieve the BILLING program"
   - "What fields are in the CUSTOMER copybook?"
   - "List available resources" (to see MCP resources)

### Manual Testing

Test the server manually before integrating with VS Code:

```bash
# Set environment variables (or use .env file)
export MF_HOST=zos.yourcompany.com
export MF_USER=YOURUSERID
export MF_KEYFILE=/path/to/key
export COBOL_SRC_DSN=YOUR.COBOL.SRC
export COPYBOOK_DSN=YOUR.COPYBOOK

# Run the server (waits for MCP connection)
python -m src.mcp_server.server
```

Expected output:
```
INFO: Loading configuration...
INFO: Configuration loaded successfully (SSH backend)
INFO: Host: zos.yourcompany.com
INFO: User: YOURUSERID
INFO: Starting MCP COBOL Server (backend: SSH)...
INFO: SSH connection pool initialized
INFO: Resource manager initialized
INFO: Server initialized, waiting for MCP connection...
```

## Troubleshooting

### MCP Tools Don't Appear in Copilot

- Ensure MCP is enabled: `"chat.mcp.enabled": true` in VS Code settings
- Check the Output panel for MCP-related errors
- Verify `.vscode/mcp.json` syntax is valid JSON
- Reload VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window")

## Docker Deployment Guide

### Why Docker?

- **Consistency**: Same environment across all team members
- **Isolation**: No Python version conflicts or dependency issues
- **Security**: Run with minimal privileges, isolated from host
- **Easy Updates**: Pull latest image and restart
- **Production Ready**: Use the same container in dev and prod

### Quick Start

```bash
# 1. Copy environment template
cp .env.docker .env

# 2. Edit .env with your credentials
# For SSH: Set MF_KEYFILE=/app/ssh_keys/id_rsa
# For Endevor: Set ENDEVOR_* variables

# 3. Start the server
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f
```

### Configuration Examples

**SSH Backend** (docker-compose.yml):
```yaml
services:
  mcp-cobol-server:
    environment:
      - BACKEND=SSH
      - MF_HOST=zos.company.com
      - MF_USER=USERID
      - MF_KEYFILE=/app/ssh_keys/id_rsa
      - COBOL_SRC_DSN=USER.COBOL.SRC
      - COPYBOOK_DSN=USER.COPYBOOK
    volumes:
      - ~/.ssh/id_rsa:/app/ssh_keys/id_rsa:ro
```

**Endevor Backend** (docker-compose.yml):
```yaml
services:
  mcp-cobol-server:
    environment:
      - BACKEND=ENDEVOR
      - ENDEVOR_BASE_URL=https://endevor.company.com/api/v1
      - ENDEVOR_USER=USERID
      - ENDEVOR_PASSWORD=${ENDEVOR_PASSWORD}
      - ENDEVOR_STAGE=PROD
```

### Connecting VS Code to Docker Server

**Option 1: Stdio Transport (Local)**
Run the server locally (not in Docker) and use `.vscode/mcp.json`.

**Option 2: SSE Transport (Remote)**
For Docker deployment with remote access, use SSE transport:

1. **Expose the server** (uncomment in docker-compose.yml):
```yaml
mcp-cobol-server-sse:
  ports:
    - "8080:8080"
  command: ["python", "-m", "uvicorn", "src.mcp_server.server:app", "--host", "0.0.0.0", "--port", "8080"]
```

2. **Configure VS Code** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "mainframe-cobol": {
      "type": "sse",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

### Docker Commands Reference

```bash
# Start server
docker-compose up -d

# Stop server
docker-compose down

# View logs
docker-compose logs -f mcp-cobol-server

# Restart server
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Access container shell
docker-compose exec mcp-cobol-server bash

# Check container status
docker-compose ps

# View resource usage
docker stats mcp-cobol-server
```

### Security Best Practices

1. **Use non-root user**: The Dockerfile creates an `appuser` with limited privileges
2. **Mount SSH keys as read-only**: Use `:ro` flag for SSH key volumes
3. **Use Docker secrets**: For production, use Docker secrets instead of `.env` files
4. **Keep images updated**: Regularly rebuild with latest security patches
5. **Limit network exposure**: Only expose ports when using SSE transport

### Troubleshooting Docker

**Container won't start**:
```bash
# Check logs
docker-compose logs mcp-cobol-server

# Verify .env file
docker-compose config
```

**SSH connection fails**:
```bash
# Verify SSH key is mounted
docker-compose exec mcp-cobol-server ls -la /app/ssh_keys/

# Test SSH from container
docker-compose exec mcp-cobol-server ssh -i /app/ssh_keys/id_rsa USER@HOST
```

**Permission denied**:
```bash
# Fix SSH key permissions on host
chmod 600 ~/.ssh/id_rsa

# Rebuild container
docker-compose up -d --force-recreate
```

### Production Deployment

For production use:

1. **Use Docker Swarm or Kubernetes** for orchestration
2. **Store secrets in Docker Swarm secrets or Kubernetes Secrets**
3. **Enable health checks** (already configured in docker-compose.yml)
4. **Set up log aggregation** (forward logs to ELK, Splunk, etc.)
5. **Monitor with Prometheus/Grafana** (export metrics from server)
6. **Use TLS for SSE transport** (terminate SSL at reverse proxy)

### "Authentication failed"

- Check SSH key file path is correct
- Verify key permissions: `chmod 600 ~/.ssh/id_rsa` (Unix-like systems)
- Test SSH manually: `ssh -i ~/.ssh/id_rsa YOURUSERID@zos.yourcompany.com`

### "Program not found"

- Verify program name (1-8 alphanumeric characters)
- Check `COBOL_SRC_DSN` is correct
- Try a different known program name

### "Unable to connect to mainframe"

- Test network: `ping zos.yourcompany.com`
- Test SSH port: `telnet zos.yourcompany.com 22`
- Check firewall settings

### Tools don't appear in Continue.dev

- Check Continue.dev console for errors
- Verify `config.json` syntax is valid JSON
- Ensure absolute path to `server.py` is correct
- Restart VS Code completely

## Project Structure

```
mcp-mainframe/
├── .github/                    # GitHub configuration
│   ├── ISSUE_TEMPLATE/         # Issue templates (bug, feature, docs)
│   ├── DISCUSSION_TEMPLATE/    # Discussion templates (Q&A, general)
│   ├── workflows/              # GitHub Actions workflows
│   │   ├── ci-cd.yml          # CI/CD pipeline
│   │   ├── docker.yml         # Docker build workflow
│   │   └── code-quality.yml   # Code quality checks
│   ├── copilot-instructions.md # GitHub Copilot agent config
│   ├── CODEOWNERS             # Code ownership
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── SECURITY.md            # Security policy
│   └── dependabot.yml         # Auto-dependency updates
├── .vscode/                    # VS Code configuration
│   ├── mcp.json               # MCP server config (SSH)
│   ├── mcp.endevor.json       # MCP server config (Endevor)
│   └── README.md              # VS Code setup guide
├── src/mcp_server/             # MCP server source code
│   ├── server.py              # Main entry point
│   ├── config.py              # Configuration management
│   ├── tools.py               # Tool implementations
│   ├── ssh_client.py          # SSH connection pooling
│   ├── endevor_client.py      # Endevor REST API client
│   └── resources.py           # MCP Resources manager
├── Dockerfile                  # Docker build configuration
├── docker-compose.yml          # Docker Compose orchestration
├── .dockerignore               # Docker build exclusions
├── .env.docker                 # Docker environment template
├── .env.example                # Local environment template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Development

### Running Tests

```bash
# Unit tests
pytest tests/unit/

# Contract tests
pytest tests/contract/

# Integration tests (requires mainframe connection)
pytest tests/integration/
```

### Code Style

- 4-space indentation
- Max 100 character line length
- Type hints for all public functions
- Docstrings for all public modules, classes, and functions

## Architecture

The server follows a modular architecture:

- **`server.py`**: MCP protocol handling, tool registration
- **`tools.py`**: Business logic (get_cobol_source, get_copybook)
- **`ssh_client.py`**: SSH connection pool, mainframe communication
- **`config.py`**: Environment variable parsing, validation

This separation allows:
- Adding new tools without modifying core MCP logic
- Independent testing of each module
- Easy SSH implementation swaps

## License

[Your License Here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the [quickstart.md](specs/001-mcp-cobol-server/quickstart.md) guide
- Contact your mainframe team for dataset access issues

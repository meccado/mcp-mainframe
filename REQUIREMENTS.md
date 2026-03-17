# MCP Mainframe COBOL Context Server – Requirements Specification

## 1. Overview
### 1.1 Purpose
This document specifies the requirements for a custom **Model Context Protocol (MCP) server** that provides live mainframe COBOL context to GitHub Copilot (via the Continue.dev extension). The server enables developers to query the latest source code, copybooks, and related artifacts directly from a z/OS mainframe environment without manual copying.

### 1.2 Scope
The solution will:
- Implement an MCP server in Python using the official MCP SDK.
- Provide tools to retrieve COBOL program source and copybooks from mainframe datasets.
- Integrate with the Continue.dev VS Code extension.
- Use SSH (with key authentication) to execute mainframe commands.
- Be configurable via environment variables for security.
- Include error handling and logging.

### 1.3 Definitions
- **MCP**: Model Context Protocol – an open standard for connecting AI assistants to data sources and tools.
- **Continue.dev**: A VS Code extension that supports MCP and can use GitHub Copilot as the language model.
- **z/OS**: IBM mainframe operating system.
- **PDS**: Partitioned Data Set – mainframe dataset storing source members.

## 2. Functional Requirements

### 2.1 MCP Server Core
- **FR1**: The server shall implement the MCP protocol using the `mcp` Python SDK.
- **FR2**: The server shall communicate via standard input/output (stdio) as required by MCP.
- **FR3**: The server shall support listing available tools via the `list_tools` method.
- **FR4**: The server shall execute tool calls via the `call_tool` method.

### 2.2 Tools

#### 2.2.1 `get_cobol_source`
- **FR5**: The server shall provide a tool named `get_cobol_source`.
- **FR6**: The tool shall accept a single string parameter `program` (the COBOL program name).
- **FR7**: The tool shall connect to the mainframe via SSH using credentials from environment variables.
- **FR8**: The tool shall construct a mainframe command to retrieve the source of the specified program from a predefined dataset (e.g., `cat 'USER.COBOL.SRC(PROGRAM)'`).
- **FR9**: The tool shall return the source code as plain text.
- **FR10**: If the program does not exist or cannot be retrieved, the tool shall return an error message.

#### 2.2.2 `get_copybook`
- **FR11**: The server shall provide a tool named `get_copybook`.
- **FR12**: The tool shall accept a single string parameter `copybook` (the copybook name).
- **FR13**: The tool shall retrieve the copybook source from a predefined copybook dataset.
- **FR14**: The tool shall return the copybook source as plain text, or an error if not found.

#### 2.2.3 (Optional) Future tools
- **FR15**: The architecture shall allow easy addition of new tools (e.g., `get_jcl`, `list_programs_in_module`) without modifying core MCP logic.

### 2.3 Configuration
- **FR16**: All sensitive mainframe connection parameters shall be provided via environment variables, not hardcoded:
  - `MF_HOST`: mainframe hostname or IP
  - `MF_USER`: SSH username
  - `MF_KEYFILE`: path to private SSH key file
  - (Optional) `MF_PASSWORD`: if password authentication is required – **not recommended**.
- **FR17**: Dataset names for source and copybooks shall be configurable via environment variables (e.g., `COBOL_SRC_DSN`, `COPYBOOK_DSN`).
- **FR18**: The server shall validate that required environment variables are set on startup; if missing, it shall log an error and exit.

### 2.4 Logging
- **FR19**: The server shall log significant events (startup, tool invocation, errors) to stderr.
- **FR20**: Log levels shall be configurable via environment variable `LOG_LEVEL` (default: INFO).

## 3. Non-Functional Requirements

### 3.1 Performance
- **NFR1**: Tool invocation shall complete within a reasonable time (target <5 seconds for a typical source retrieval).
- **NFR2**: SSH connections shall be reused for multiple tool calls within the same session to reduce overhead (optional, but recommended).

### 3.2 Security
- **NFR3**: No credentials shall be exposed in logs or tool outputs.
- **NFR4**: SSH key authentication is preferred over passwords.
- **NFR5**: The server shall run with the least privilege necessary on the mainframe (read-only access to source datasets).

### 3.3 Reliability
- **NFR6**: The server shall handle network timeouts gracefully and return a user‑friendly error.
- **NFR7**: The server shall recover from transient SSH failures (e.g., by retrying once).

### 3.4 Maintainability
- **NFR8**: Code shall be modular, with clear separation between MCP handling, SSH communication, and mainframe command generation.
- **NFR9**: Inline comments and docstrings shall explain non‑obvious logic.

## 4. Technical Specifications

### 4.1 Technology Stack
- **Language**: Python 3.10+
- **MCP Library**: `mcp` (official SDK)
- **SSH Library**: `paramiko`
- **Configuration**: `python-dotenv` for local development (optional)
- **Testing**: `pytest`, `pytest-asyncio`

### 4.2 Project Structure
```
mcp-mainframe/
├── src/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py          # Main MCP server entry point
│   │   ├── tools.py           # Tool implementations
│   │   ├── ssh_client.py      # SSH connection handling
│   │   └── config.py          # Environment variable parsing
├── tests/
│   ├── test_tools.py
│   └── test_ssh_client.py
├── .env.example                # Example environment variables
├── requirements.txt
├── README.md
└── pyproject.toml              # Optional, for packaging
```

### 4.3 Interface Definitions

#### 4.3.1 Environment Variables
| Variable        | Required | Description                                    | Example                     |
|-----------------|----------|------------------------------------------------|-----------------------------|
| MF_HOST         | Yes      | Mainframe hostname or IP                       | `zos.company.com`           |
| MF_USER         | Yes      | SSH username                                   | `myuserid`                  |
| MF_KEYFILE      | Yes      | Path to private SSH key                        | `/home/user/.ssh/id_rsa`    |
| COBOL_SRC_DSN   | Yes      | Dataset name for COBOL source                   | `USER.COBOL.SRC`            |
| COPYBOOK_DSN    | Yes      | Dataset name for copybooks                      | `USER.COPYBOOK`             |
| LOG_LEVEL       | No       | Logging level (DEBUG, INFO, WARNING, ERROR)    | `INFO`                      |

#### 4.3.2 MCP Tool Definitions

**Tool: `get_cobol_source`**
- **Description**: Retrieve the latest COBOL source code for a given program.
- **Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "program": { "type": "string" }
  },
  "required": ["program"]
}
```
- **Output**: TextContent containing the source code or an error message.

**Tool: `get_copybook`**
- **Description**: Retrieve a COBOL copybook.
- **Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "copybook": { "type": "string" }
  },
  "required": ["copybook"]
}
```
- **Output**: TextContent containing the copybook source or an error message.

### 4.4 Mainframe Command Details
The server will construct commands to read a dataset member. On z/OS UNIX System Services (USS), a common command is:
```bash
cat "//'USER.COBOL.SRC(PROGRAM)'"
```
If using TSO, the command might be:
```bash
tsocmd "listds 'USER.COBOL.SRC' members"
```
But for simplicity, we assume USS is available and the dataset is accessible via the filesystem at `/z/path/to/dataset`. The exact command template shall be configurable via environment variable `CAT_COMMAND` (default: `cat "//'{}'"`).

### 4.5 Error Handling
- **SSH connection errors**: Return `"Error: Unable to connect to mainframe. Check network and credentials."`
- **Missing dataset/member**: Return `"Error: Program {program} not found."`
- **Permission denied**: Return `"Error: Permission denied. Check SSH user permissions."`
- **Timeout**: Return `"Error: Connection timeout."`

## 5. Integration with Continue.dev

### 5.1 Configuration
The user must add the following to their `~/.continue/config.json`:
```json
{
  "experimental": {
    "mcpServers": {
      "mainframe": {
        "command": "python",
        "args": ["/absolute/path/to/mcp-mainframe/src/mcp_server/server.py"],
        "env": {
          "MF_HOST": "zos.company.com",
          "MF_USER": "myuserid",
          "MF_KEYFILE": "/home/user/.ssh/id_rsa",
          "COBOL_SRC_DSN": "USER.COBOL.SRC",
          "COPYBOOK_DSN": "USER.COPYBOOK"
        }
      }
    }
  }
}
```

### 5.2 Usage
After restarting VS Code, the user can open Continue chat and ask:
- "Using get_cobol_source, show me the source for program PAYROLL."
- "What are the fields in copybook CUST-REC?"
- "Explain the logic of PAYROLL."

## 6. Testing Requirements

### 6.1 Unit Tests
- **T1**: Test environment variable parsing with valid/invalid values.
- **T2**: Test SSH command execution mocking (using `unittest.mock`).
- **T3**: Test tool handlers return expected output for valid inputs.
- **T4**: Test error responses for missing programs.

### 6.2 Integration Tests
- **T5**: (Optional) Run against a test mainframe dataset to verify connectivity.
- **T6**: Verify that the MCP server registers tools correctly with a test client.

### 6.3 Manual Testing
- **T7**: Install Continue extension and confirm tools appear.
- **T8**: Execute a real query and verify source retrieval.

## 7. Deployment

### 7.1 Prerequisites for End Users
- Python 3.10+
- SSH access to mainframe with key-based authentication.
- Continue.dev extension installed in VS Code.

### 7.2 Installation Steps
1. Clone repository.
2. Create virtual environment and install dependencies.
3. Set environment variables (or provide them in Continue config).
4. Test server manually: `python src/mcp_server/server.py`
5. Add MCP server configuration to Continue.
6. Restart VS Code.

## 8. Future Enhancements
- Add caching to avoid repeated SSH calls.
- Support for Endevor or other source management APIs.
- Provide a “resources” endpoint for frequently accessed data.
- Add more tools: `get_jcl`, `list_programs`, `search_code`.

---

This document serves as the complete specification for the MCP Mainframe COBOL Context Server. It is intended to be used with GitHub Speckit and Qwen Coder CLI to generate the implementation. All requirements are traceable and can be used as a basis for test case creation.
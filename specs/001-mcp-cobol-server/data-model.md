# Data Model: MCP COBOL Server

**Created**: 2026-03-16
**Branch**: `001-mcp-cobol-server`

## Overview

This MCP server is **read-only** and **stateless**—it retrieves data from mainframe datasets but does not persist any data locally. The "data model" consists of the entities representing mainframe artifacts and the configuration context.

---

## Core Entities

### 1. COBOL Program

**Definition**: A source code member stored in a mainframe PDS (Partitioned Data Set) containing executable COBOL logic.

**Attributes**:
| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `name` | string | Program name (member name) | 1-8 alphanumeric characters, uppercase |
| `source_code` | string | Complete COBOL source code | Plain text, may contain special characters |
| `dataset` | string | Source PDS dataset name | Format: `USER.COBOL.SRC` or similar |
| `member_path` | string | Full USS path to member | Derived: `//'{dataset}({name})'` |
| `retrieved_at` | datetime | Timestamp of retrieval | ISO 8601 format, for logging only |

**Relationships**:
- Belongs to: COBOL Source Dataset
- May reference: Multiple Copybooks (via COPY statement)

**Validation Rules**:
- Program name MUST match pattern: `^[A-Z0-9@#$]{1,8}$` (z/OS member naming)
- Source code MUST NOT be modified before returning to user
- Dataset MUST be configured via `COBOL_SRC_DSN` environment variable

---

### 2. Copybook

**Definition**: A reusable COBOL source member containing data structure definitions (record layouts, field definitions, constants).

**Attributes**:
| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `name` | string | Copybook name (member name) | 1-8 alphanumeric characters, uppercase |
| `source_code` | string | Complete copybook source | Plain text, contains level numbers (01, 05, 10, etc.) |
| `dataset` | string | Copybook PDS dataset name | Format: `USER.COPYBOOK` or similar |
| `member_path` | string | Full USS path to member | Derived: `//'{dataset}({name})'` |
| `retrieved_at` | datetime | Timestamp of retrieval | ISO 8601 format, for logging only |

**Relationships**:
- Belongs to: Copybook Dataset
- Referenced by: Multiple COBOL Programs (via COPY statement)

**Validation Rules**:
- Copybook name MUST match pattern: `^[A-Z0-9@#$]{1,8}$`
- Source code typically contains level numbers (01-49, 77, 88)
- Dataset MUST be configured via `COPYBOOK_DSN` environment variable

---

### 3. Mainframe Dataset (PDS)

**Definition**: A z/OS Partitioned Data Set—a library containing named members (programs or copybooks).

**Attributes**:
| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `dsn` | string | Dataset name | Format: `USER.NAME.TYPE` (3-44 characters) |
| `type` | enum | Dataset purpose | Values: `COBOL_SOURCE`, `COPYBOOK` |
| `uss_path` | string | USS filesystem path | `/u/...` or `//'{dsn}'` format |
| `accessible` | boolean | Whether dataset is reachable | Determined at runtime |

**Relationships**:
- Contains: Multiple COBOL Programs OR Copybooks (not both)

**Validation Rules**:
- Dataset name MUST follow z/OS naming conventions
- Dataset MUST be accessible via USS filesystem
- User MUST have read-only permissions

---

### 4. MCP Tool

**Definition**: A function exposed by the MCP server that can be invoked by AI assistants.

**Attributes**:
| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `name` | string | Tool identifier | Values: `get_cobol_source`, `get_copybook` |
| `description` | string | Human-readable description | Shown in AI assistant UI |
| `input_schema` | JSON Schema | Parameter validation schema | Defines required/optional params |
| `handler` | function | Implementation function | Async, returns TextContent |

**Tool Definitions**:

#### Tool: `get_cobol_source`
```json
{
  "name": "get_cobol_source",
  "description": "Retrieve the latest COBOL source code for a given program from the mainframe.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "program": {
        "type": "string",
        "description": "The COBOL program name (1-8 alphanumeric characters)"
      }
    },
    "required": ["program"]
  }
}
```

#### Tool: `get_copybook`
```json
{
  "name": "get_copybook",
  "description": "Retrieve a COBOL copybook (data structure definition) from the mainframe.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "copybook": {
        "type": "string",
        "description": "The copybook name (1-8 alphanumeric characters)"
      }
    },
    "required": ["copybook"]
  }
}
```

---

### 5. Server Configuration

**Definition**: Runtime configuration loaded from environment variables.

**Attributes**:
| Attribute | Env Var | Type | Required | Default |
|-----------|---------|------|----------|---------|
| `host` | `MF_HOST` | string | Yes | — |
| `username` | `MF_USER` | string | Yes | — |
| `key_file` | `MF_KEYFILE` | string | Yes | — |
| `cobol_source_dsn` | `COBOL_SRC_DSN` | string | Yes | — |
| `copybook_dsn` | `COPYBOOK_DSN` | string | Yes | — |
| `log_level` | `LOG_LEVEL` | enum | No | `INFO` |
| `max_connections` | `MAX_CONNECTIONS` | integer | No | `10` |
| `connection_timeout` | `CONNECTION_TIMEOUT` | integer | No | `30` |
| `command_template` | `CAT_COMMAND` | string | No | `cat "//'{}'"` |

**Validation Rules**:
- All required variables MUST be set before server starts
- `LOG_LEVEL` MUST be one of: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `MAX_CONNECTIONS` MUST be between 1 and 20
- `MF_KEYFILE` MUST point to an existing file with correct permissions (600)

---

## State Transitions

This server is **stateless**—no state transitions occur. Each tool invocation:
1. Receives request with program/copybook name
2. Validates input
3. Acquires SSH connection from pool
4. Executes mainframe command
5. Returns source code
6. Releases SSH connection back to pool

No persistent state is maintained between invocations.

---

## Data Flow Diagram

```
┌─────────────────┐
│  AI Assistant   │
│  (via Continue) │
└────────┬────────┘
         │ MCP Tool Call
         ▼
┌─────────────────────────┐
│   MCP Server (stdio)    │
│  ┌───────────────────┐  │
│  │   server.py       │  │
│  │  (MCP Protocol)   │  │
│  └─────────┬─────────┘  │
│            │            │
│  ┌─────────▼─────────┐  │
│  │   tools.py        │  │
│  │  (Business Logic) │  │
│  └─────────┬─────────┘  │
│            │            │
│  ┌─────────▼─────────┐  │
│  │  ssh_client.py    │  │
│  │ (Connection Pool) │  │
│  └─────────┬─────────┘  │
└────────────┼────────────┘
             │ SSH (port 22)
             ▼
┌─────────────────────────┐
│   z/OS Mainframe        │
│  ┌───────────────────┐  │
│  │  USS Filesystem   │  │
│  │  cat "//'DSN(MBR)'"│ │
│  └───────────────────┘  │
└─────────────────────────┘
```

---

## Error States

| Error Type | Trigger | Response |
|------------|---------|----------|
| `ValidationError` | Invalid program/copybook name | Return MCP error with validation message |
| `ConfigurationError` | Missing required env var | Log error, exit server |
| `ConnectionError` | SSH connection fails | Return user-friendly error, log at WARNING |
| `AuthenticationError` | SSH key rejected | Return auth error, log at WARNING |
| `NotFoundError` | Program/copybook not in dataset | Return not found error, log at INFO |
| `PermissionError` | User lacks read access | Return permission error, log at WARNING |
| `TimeoutError` | SSH operation exceeds timeout | Return timeout error, log at WARNING |
| `PoolExhaustedError` | All connections in use | Queue request or return "server busy" |

---

## Design Principles

1. **Immutability**: Retrieved source code is never modified
2. **Statelessness**: No persistent state between tool calls
3. **Read-Only**: No write operations to mainframe
4. **Explicit Configuration**: All parameters via environment variables
5. **Fail-Fast**: Validate configuration on startup, fail immediately if invalid

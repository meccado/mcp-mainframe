# MCP Tool Contracts

**Created**: 2026-03-16
**Branch**: `001-mcp-cobol-server`

This document defines the interface contracts for the MCP tools exposed by this server. These contracts are the formal agreement between the MCP server and AI assistants (via Continue.dev).

---

## Contract 1: `get_cobol_source`

### Purpose
Retrieve COBOL program source code from the mainframe.

### Input Contract

**Method**: MCP `call_tool` with name `get_cobol_source`

**Input Schema** (JSON Schema):
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "program": {
      "type": "string",
      "description": "The COBOL program name (1-8 alphanumeric characters)",
      "minLength": 1,
      "maxLength": 8,
      "pattern": "^[A-Za-z0-9@#$]+$"
    }
  },
  "required": ["program"],
  "additionalProperties": false
}
```

**Valid Input Examples**:
```json
{"program": "PAYROLL"}
{"program": "CUSTUPD"}
{"program": "RPT001"}
```

**Invalid Input Examples**:
```json
{"program": ""}                    // Empty string
{"program": "VERYLONGNAME"}        // >8 characters
{"program": "PROG-1"}              // Hyphen not allowed
{"program": "PROG 1"}              // Space not allowed
```

### Output Contract

**Success Response**:
- **Content Type**: `text`
- **Format**: Plain text COBOL source code
- **Encoding**: UTF-8 (or EBCDIC converted to ASCII)
- **Structure**: Complete COBOL program including identification, environment, data, and procedure divisions

**Example Success Output**:
```
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAYROLL.
       AUTHOR. SYSTEM PROGRAMMER.
       
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-EMPLOYEE-TOTAL      PIC 9(5) VALUE ZEROS.
       
       PROCEDURE DIVISION.
       MAIN-LOGIC.
           PERFORM 1000-INITIALIZE
           PERFORM 2000-PROCESS-RECORDS
           PERFORM 9000-FINALIZE
           STOP RUN.
```

**Error Responses**:

| Error Condition | MCP Error Message | Log Level |
|-----------------|-------------------|-----------|
| Program not found | `Error: Program '{program}' not found in dataset {dataset}.` | INFO |
| Invalid program name | `Error: Invalid program name. Must be 1-8 alphanumeric characters.` | INFO |
| SSH connection failed | `Error: Unable to connect to mainframe. Check network and credentials.` | WARNING |
| Authentication failed | `Error: Authentication failed. Check SSH key permissions.` | WARNING |
| Permission denied | `Error: Access denied. Check read permissions for dataset.` | WARNING |
| Timeout | `Error: Connection timeout. Try again or check mainframe availability.` | WARNING |
| Server busy | `Error: Server is busy. Please try again in a few seconds.` | INFO |

### Performance Contract

- **Latency**: <5 seconds for programs under 10KB (p95)
- **Throughput**: Up to 10 concurrent requests (configurable)
- **Availability**: Best-effort (depends on mainframe availability)

### Side Effects

- **None**: This is a read-only operation
- **Logging**: Request and response logged at INFO level (no source code content)
- **Connection**: Acquires SSH connection from pool, releases after completion

---

## Contract 2: `get_copybook`

### Purpose
Retrieve COBOL copybook (data structure definition) from the mainframe.

### Input Contract

**Method**: MCP `call_tool` with name `get_copybook`

**Input Schema** (JSON Schema):
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "copybook": {
      "type": "string",
      "description": "The copybook name (1-8 alphanumeric characters)",
      "minLength": 1,
      "maxLength": 8,
      "pattern": "^[A-Za-z0-9@#$]+$"
    }
  },
  "required": ["copybook"],
  "additionalProperties": false
}
```

**Valid Input Examples**:
```json
{"copybook": "CUST-REC"}
{"copybook": "ADDRBOOK"}
{"copybook": "COMMON1"}
```

**Invalid Input Examples**:
```json
{"copybook": ""}                    // Empty string
{"copybook": "VERYLONGNAME"}        // >8 characters
{"copybook": "COPY-1"}              // Hyphen not allowed
```

### Output Contract

**Success Response**:
- **Content Type**: `text`
- **Format**: Plain text copybook source code
- **Encoding**: UTF-8 (or EBCDIC converted to ASCII)
- **Structure**: COBOL copybook with level numbers (01, 05, 10, 77, 88)

**Example Success Output**:
```
       01  CUSTOMER-RECORD.
           05  CUST-ID              PIC X(10).
           05  CUST-NAME            PIC X(30).
           05  CUST-ADDR.
               10  STREET           PIC X(25).
               10  CITY             PIC X(20).
               10  STATE            PIC X(2).
               10  ZIP-CODE         PIC X(10).
           05  CUST-PHONE           PIC X(15).
```

**Error Responses**:

| Error Condition | MCP Error Message | Log Level |
|-----------------|-------------------|-----------|
| Copybook not found | `Error: Copybook '{copybook}' not found in dataset {dataset}.` | INFO |
| Invalid copybook name | `Error: Invalid copybook name. Must be 1-8 alphanumeric characters.` | INFO |
| SSH connection failed | `Error: Unable to connect to mainframe. Check network and credentials.` | WARNING |
| Authentication failed | `Error: Authentication failed. Check SSH key permissions.` | WARNING |
| Permission denied | `Error: Access denied. Check read permissions for dataset.` | WARNING |
| Timeout | `Error: Connection timeout. Try again or check mainframe availability.` | WARNING |
| Server busy | `Error: Server is busy. Please try again in a few seconds.` | INFO |

### Performance Contract

- **Latency**: <5 seconds for copybooks under 10KB (p95)
- **Throughput**: Up to 10 concurrent requests (configurable)
- **Availability**: Best-effort (depends on mainframe availability)

### Side Effects

- **None**: This is a read-only operation
- **Logging**: Request and response logged at INFO level (no source code content)
- **Connection**: Acquires SSH connection from pool, releases after completion

---

## MCP Protocol Contract

### Server Capabilities

**Tools Supported**:
```json
{
  "tools": [
    {
      "name": "get_cobol_source",
      "description": "Retrieve the latest COBOL source code for a given program from the mainframe.",
      "inputSchema": { ... }
    },
    {
      "name": "get_copybook",
      "description": "Retrieve a COBOL copybook (data structure definition) from the mainframe.",
      "inputSchema": { ... }
    }
  ]
}
```

### Transport Protocol

- **Method**: stdio (standard input/output)
- **Encoding**: JSON-RPC 2.0 over newline-delimited JSON
- **Initialization**: MCP `initialize` handshake on startup

### Error Handling Contract

All errors follow MCP error response format:
```json
{
  "jsonrpc": "2.0",
  "id": "<request-id>",
  "error": {
    "code": <integer>,
    "message": "<human-readable message>",
    "data": {
      "details": "<optional additional context>"
    }
  }
}
```

**Error Codes**:
- `-32602`: Invalid params (validation error)
- `-32000`: Server error (connection, timeout, etc.)
- `-32001`: Tool not found (should not occur with proper registration)

---

## Versioning Policy

**Contract Version**: 1.0.0

**Breaking Changes** (require MAJOR version bump):
- Changing input schema (removing/rename parameters)
- Changing output format (non-backward-compatible)
- Removing tools
- Changing error message format

**Non-Breaking Changes** (MINOR or PATCH):
- Adding new tools
- Adding optional input parameters
- Improving error message clarity
- Performance improvements

---

## Testing Requirements

### Contract Tests (Required)

1. **Tool Registration**:
   - Verify `list_tools()` returns both `get_cobol_source` and `get_copybook`
   - Verify tool schemas match this contract

2. **Input Validation**:
   - Valid program/copybook names are accepted
   - Invalid names (empty, too long, invalid chars) return validation errors
   - Missing required parameters return appropriate errors

3. **Success Path**:
   - Valid program name returns COBOL source as text
   - Valid copybook name returns copybook source as text

4. **Error Paths**:
   - Not found returns appropriate error message
   - Connection failures return user-friendly errors
   - Timeout returns timeout error

5. **Performance**:
   - Response time <5 seconds for typical inputs (under load)

### Test File Locations

- `tests/contract/test_mcp_contract.py` - Protocol compliance
- `tests/contract/test_tool_schemas.py` - Input/output schema validation
- `tests/contract/test_error_handling.py` - Error response format

---

## Integration Guidelines

### For AI Assistants

1. **Tool Discovery**: Call `list_tools()` on startup to discover available tools
2. **Input Validation**: Validate user input against tool schemas before calling
3. **Error Handling**: Display error messages to users; suggest corrective actions
4. **Context Management**: Use retrieved source code as context for code analysis

### For Continue.dev Users

1. **Configuration**: Add MCP server config to `~/.continue/config.json`
2. **Usage**: Ask natural language questions; Continue will invoke tools automatically
3. **Examples**:
   - "Show me the source for program PAYROLL"
   - "What fields are in the CUST-REC copybook?"
   - "Explain the logic in the BILLING program"

---

## References

- **MCP Specification**: https://modelcontextprotocol.io/specification
- **JSON Schema**: https://json-schema.org/
- **JSON-RPC 2.0**: https://www.jsonrpc.org/specification

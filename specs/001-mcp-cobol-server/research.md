# Research & Technical Decisions: MCP COBOL Server

**Created**: 2026-03-16
**Branch**: `001-mcp-cobol-server`

This document consolidates all technical decisions made during the planning phase, resolving uncertainties from the Technical Context section.

---

## Technology Stack Decisions

### Decision 1: Python 3.10+ as Implementation Language

**Rationale**: 
- MCP SDK (`mcp` package) is Python-native with first-party support
- Rich ecosystem for SSH (paramiko) and async operations
- Cross-platform compatibility (Windows, macOS, Linux) for developer workstations
- Strong typing support via type hints improves code quality

**Alternatives Considered**:
- **Node.js/TypeScript**: Good MCP support but weaker SSH library ecosystem
- **Rust**: Excellent performance but steeper learning curve, overkill for I/O-bound tool
- **Go**: Good SSH support but MCP ecosystem less mature than Python

---

### Decision 2: MCP SDK (`mcp` package) for Protocol Implementation

**Rationale**:
- Official MCP SDK from the Model Context Protocol project
- Handles protocol complexity (tool registration, schema validation, stdio transport)
- Actively maintained with growing ecosystem
- Reduces implementation to business logic (tool handlers)

**Alternatives Considered**:
- **Custom MCP implementation**: Would require deep protocol understanding, high maintenance burden
- **Other protocol adapters**: MCP is the standard supported by Continue.dev and emerging AI tools

---

### Decision 3: Paramiko for SSH Communication

**Rationale**:
- Mature, battle-tested SSH library for Python (20+ years)
- Supports key-based authentication, connection pooling, timeout handling
- Well-documented with extensive community knowledge
- Handles z/OS USS filesystem access patterns

**Alternatives Considered**:
- **asyncssh**: Async alternative but less mature, smaller community
- **subprocess + ssh command**: Platform-dependent, harder to manage credentials securely
- **Fabric**: Higher-level abstraction, adds unnecessary complexity for simple file reads

---

### Decision 4: pytest + pytest-asyncio for Testing

**Rationale**:
- Industry standard for Python testing
- pytest-asyncio provides async test support for MCP server
- Rich fixture system for mocking SSH connections
- Excellent integration with CI/CD pipelines

**Alternatives Considered**:
- **unittest**: Built-in but verbose, less flexible
- **nose2**: Less active development, smaller ecosystem

---

## Architecture Decisions

### Decision 5: Modular Architecture with Clear Separation

**Module Structure**:
```
mcp_server/
├── server.py      → MCP protocol handling (@server.list_tools, @server.call_tool)
├── tools.py       → Business logic (get_cobol_source, get_copybook implementations)
├── ssh_client.py  → Infrastructure (SSH connection pool, command execution)
└── config.py      → Configuration (env var parsing, validation, type safety)
```

**Rationale**:
- Aligns with Constitution Principle III (Modularity & Extensibility)
- Each module has single responsibility, independently testable
- New tools can be added to `tools.py` without touching `server.py` or `ssh_client.py`
- SSH implementation can be swapped without affecting business logic

---

### Decision 6: SSH Connection Pooling with Configurable Limits

**Design**:
- Maintain a pool of 5-10 reusable SSH connections (configurable via `MAX_CONNECTIONS` env var)
- Connections are reused across tool calls within the same session
- Excess requests are queued (not rejected) to handle burst scenarios
- Idle connections timeout after configurable period (default: 60 seconds)

**Rationale**:
- Aligns with Constitution Principle V (Performance & Resilience)
- SSH connection establishment is expensive (~1-2 seconds)
- Connection reuse reduces per-request latency to <500ms for typical sources
- Pool prevents resource exhaustion on mainframe side

**Implementation Pattern**:
```python
class SSHConnectionPool:
    def __init__(self, max_connections=10):
        self._pool = asyncio.Queue(maxsize=max_connections)
        self._semaphore = asyncio.Semaphore(max_connections)
    
    async def acquire(self):
        await self._semaphore.acquire()
        # Create or reuse connection
        return conn
    
    async def release(self, conn):
        # Return to pool or close if stale
        self._pool.put_nowait(conn)
        self._semaphore.release()
```

---

### Decision 7: USS (UNIX System Services) Filesystem Access

**Command Pattern**:
```bash
cat "//'USER.COBOL.SRC(PROGRAM)'"
```

**Rationale**:
- Simpler than TSO commands, more reliable for file reads
- Aligns with spec clarification (USS only, TSO not supported)
- Standard POSIX-like interface on z/OS
- Paramiko's SFTP support can also be used for direct file reads

**Alternatives Considered**:
- **TSO commands**: More complex, requires TSO environment setup
- **Endevor/Changeman APIs**: Requires additional mainframe software, licensing
- **Direct dataset allocation**: Lower-level, more error-prone

---

## Security Decisions

### Decision 8: Environment Variables for All Credentials

**Required Variables**:
- `MF_HOST`: Mainframe hostname or IP
- `MF_USER`: SSH username
- `MF_KEYFILE`: Path to private SSH key file (PEM or OpenSSH format)
- `COBOL_SRC_DSN`: Dataset name for COBOL source (e.g., `USER.COBOL.SRC`)
- `COPYBOOK_DSN`: Dataset name for copybooks (e.g., `USER.COPYBOOK`)
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

**Validation**:
- Server validates all required variables on startup
- Exits with clear error message if any are missing
- No fallback defaults for sensitive parameters

**Rationale**:
- Aligns with Constitution Principle II (Configuration-Driven)
- Prevents accidental credential commits to version control
- Enables different configurations per environment (dev, test, prod)

---

### Decision 9: Read-Only Access Enforcement

**Implementation**:
- SSH user configured with read-only permissions on target datasets
- Server only executes read commands (`cat`, SFTP `get`)
- No write, delete, or modify operations exposed
- Dataset names are configurable but validated against allowlist pattern (optional enhancement)

**Rationale**:
- Aligns with Constitution Principle I (Security-First)
- Least privilege principle
- Prevents accidental or malicious modifications to production source code

---

## Error Handling Decisions

### Decision 10: User-Friendly Error Messages

**Error Categories and Messages**:

| Scenario | User Message | Log Level |
|----------|--------------|-----------|
| SSH connection timeout | "Unable to connect to mainframe. Check network connectivity and try again." | WARNING |
| Authentication failure | "Authentication failed. Check SSH key permissions and try again." | WARNING |
| Program not found | "Program '{program}' not found in dataset {dataset}." | INFO |
| Copybook not found | "Copybook '{copybook}' not found in dataset {dataset}." | INFO |
| Permission denied | "Access denied. Check that your user has read permission for this dataset." | WARNING |
| Missing env var | "Configuration error: Required environment variable '{var}' is not set." | ERROR |
| Connection limit exceeded | "Server is busy handling other requests. Please try again in a few seconds." | INFO |
| Invalid program name | "Invalid program name. Names must be 1-8 alphanumeric characters." | INFO |

**Rationale**:
- Aligns with Constitution Principle IV (Observability & Debuggability)
- User messages are actionable, never expose stack traces or internals
- Log messages include full context for debugging

---

## Performance Decisions

### Decision 11: Performance Targets and Optimization Strategies

**Targets** (from spec Success Criteria):
- SC-001: <5 seconds for COBOL program retrieval (<10KB)
- SC-002: <5 seconds for copybook retrieval
- SC-004: <2 seconds server startup time

**Optimization Strategies**:
1. **Connection pooling**: Reuse SSH connections (saves 1-2s per request)
2. **Async I/O**: Use asyncio for non-blocking operations
3. **Minimal processing**: Return source as-is, no transformation
4. **Lazy initialization**: Defer SSH connection until first tool call

**Measurement**:
- Instrument tool handlers with timing logs
- Log request duration at INFO level
- Alert on p95 latency >5s in production usage

---

## Integration Decisions

### Decision 12: Continue.dev Integration Pattern

**Configuration** (user adds to `~/.continue/config.json`):
```json
{
  "experimental": {
    "mcpServers": {
      "mainframe": {
        "command": "python",
        "args": ["/absolute/path/to/src/mcp_server/server.py"],
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

**Usage Flow**:
1. User restarts VS Code after config change
2. Continue.dev spawns MCP server as child process (stdio transport)
3. Server initializes, validates env vars, ready for tool calls
4. User asks: "Show me the source for program PAYROLL"
5. Continue.dev invokes `get_cobol_source(program="PAYROLL")`
6. Server retrieves source via SSH, returns as text content
7. Continue.dev displays source in chat context

**Rationale**:
- Standard MCP integration pattern
- No custom Continue.dev modifications required
- Works with any MCP-compatible AI assistant (not just Copilot)

---

## Testing Strategy

### Decision 13: Testing Pyramid

**Unit Tests** (REQUIRED - Constitution):
- `test_config.py`: Env var parsing, validation, error messages
- `test_tools.py`: Tool handlers with mocked SSH (success and error paths)
- `test_ssh_client.py`: Connection pool logic, timeout handling

**Contract Tests** (REQUIRED - Constitution):
- `test_mcp_contract.py`: Verify MCP protocol compliance
  - `list_tools()` returns correct tool definitions
  - `call_tool()` validates input schemas
  - Error responses follow MCP format

**Integration Tests** (OPTIONAL - requires test mainframe):
- `test_mainframe_integration.py`: Real SSH connection to test mainframe
- Validate end-to-end source retrieval
- Skip in CI if mainframe unavailable

**Manual Testing** (REQUIRED - Constitution):
- Install Continue.dev extension
- Configure MCP server
- Verify tools appear in Continue chat
- Execute real queries against mainframe

---

## Future Enhancement Considerations

### Not In Scope (MVP)

These are explicitly deferred to future features:

- **Caching**: No local caching of source code in MVP
- **Endevor/Changeman integration**: USS filesystem access only
- **Additional tools**: Only `get_cobol_source` and `get_copybook` in MVP
- **Resources endpoint**: MCP resources for frequently-accessed data
- **Search functionality**: No code search in MVP
- **Write operations**: Read-only access only

### Potential Future Additions

When justified by user demand:

- `get_jcl`: Retrieve JCL members from PDS
- `list_programs`: List all programs in a dataset/module
- `search_code`: Search for text patterns across programs
- `get_dependencies`: Analyze copybook dependencies
- **Caching layer**: Redis or local file cache for frequently-accessed sources
- **Multi-mainframe support**: Configure multiple mainframe connections

---

## References

- **MCP Specification**: https://modelcontextprotocol.io/
- **Continue.dev Documentation**: https://docs.continue.dev/
- **Paramiko Documentation**: https://docs.paramiko.org/
- **z/OS USS Guide**: IBM documentation on UNIX System Services
- **Python asyncio**: https://docs.python.org/3/library/asyncio.html

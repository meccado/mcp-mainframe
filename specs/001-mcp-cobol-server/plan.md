# Implementation Plan: MCP COBOL Server

**Branch**: `001-mcp-cobol-server` | **Date**: 2026-03-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-mcp-cobol-server/spec.md`

## Summary

Build an MCP (Model Context Protocol) server that provides live COBOL mainframe source code and copybook retrieval to AI assistants via Continue.dev. The server exposes two tools (`get_cobol_source`, `get_copybook`) that connect to z/OS mainframe via SSH key-based authentication and retrieve source members from PDS datasets using USS (UNIX System Services) filesystem access.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `mcp` (official MCP SDK), `paramiko` (SSH library)
**Storage**: N/A (reads from mainframe datasets, no local persistence)
**Testing**: pytest, pytest-asyncio
**Target Platform**: Cross-platform (Windows, macOS, Linux) - runs locally where VS Code is installed
**Project Type**: CLI tool / MCP server (stdio-based)
**Performance Goals**: <5 second response time for typical source retrieval (<10KB), <2 second startup time
**Constraints**: SSH key-based auth only, read-only mainframe access, USS filesystem required, 5-10 concurrent connection limit
**Scale/Scope**: Single developer workstation usage (not a multi-tenant service)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Compliance Assessment

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Security-First** | ✅ PASS | SSH key-based auth (FR-005), env vars for credentials (FR-010), read-only access, no credential exposure (FR-015) |
| **II. Configuration-Driven** | ✅ PASS | All connection params via env vars (FR-010), validation on startup (FR-011, FR-012), no defaults for sensitive params |
| **III. Modularity & Extensibility** | ✅ PASS | Architecture separates MCP/SSH/commands/config (FR-016), independently testable modules |
| **IV. Observability & Debuggability** | ✅ PASS | Logging to stderr (FR-013), configurable levels (FR-014), user-friendly errors (FR-008, FR-009) |
| **V. Performance & Resilience** | ✅ PASS | <5s target (SC-001, SC-002), connection reuse, retry logic, connection limits (FR-017, FR-018) |

**Gates**: ALL PASSED - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-cobol-server/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py          # Main MCP server entry point
│   ├── tools.py           # Tool implementations (get_cobol_source, get_copybook)
│   ├── ssh_client.py      # SSH connection handling with connection pooling
│   └── config.py          # Environment variable parsing and validation
tests/
├── contract/
│   └── test_mcp_contract.py
├── integration/
│   └── test_mainframe_integration.py
└── unit/
    ├── test_config.py
    ├── test_tools.py
    └── test_ssh_client.py
```

**Structure Decision**: Single project structure (Option 1 from template). MCP server is a standalone Python package with clear module separation: `server.py` (MCP protocol), `tools.py` (business logic), `ssh_client.py` (infrastructure), `config.py` (configuration). Tests organized by type: contract (MCP protocol), integration (mainframe connectivity), unit (individual modules).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles pass compliance assessment.

---

## Phase 0 & Phase 1 Completion Report

### Phase 0: Research ✅ COMPLETE

**Output**: `research.md`

**Decisions Made**:
1. Python 3.10+ with MCP SDK and paramiko
2. Modular architecture (server/tools/ssh_client/config)
3. SSH connection pooling with 5-10 concurrent limit
4. USS filesystem access only (TSO not supported)
5. Environment variables for all credentials
6. User-friendly error messages with proper logging
7. pytest + pytest-asyncio for testing
8. Continue.dev integration via stdio transport

**All NEEDS CLARIFICATION items resolved**: Yes

---

### Phase 1: Design & Contracts ✅ COMPLETE

**Outputs**:
- `data-model.md` - Entity definitions, validation rules, data flow
- `contracts/mcp-tools.md` - Tool interface contracts (get_cobol_source, get_copybook)
- `quickstart.md` - User guide for setup and usage
- `QWEN.md` - Agent context updated with tech stack

**Agent Context Update**: ✅ Complete
- File: `QWEN.md`
- Technologies added: Python 3.10+, MCP SDK, paramiko
- Project type: CLI tool / MCP server

---

### Constitution Check (Post-Design) ✅ RE-EVALUATED

**Status**: ALL PRINCIPLES STILL PASS

| Principle | Pre-Design | Post-Design | Status |
|-----------|------------|-------------|--------|
| I. Security-First | ✅ PASS | ✅ PASS | No changes |
| II. Configuration-Driven | ✅ PASS | ✅ PASS | No changes |
| III. Modularity & Extensibility | ✅ PASS | ✅ PASS | No changes |
| IV. Observability & Debuggability | ✅ PASS | ✅ PASS | No changes |
| V. Performance & Resilience | ✅ PASS | ✅ PASS | No changes |

**Design Validated**: All architecture decisions align with constitution principles.

---

### Ready for Phase 2: Tasks

**Next Command**: `/speckit.tasks`

**Prerequisites Met**:
- ✅ spec.md (user stories, requirements, success criteria)
- ✅ plan.md (technical context, constitution check, project structure)
- ✅ research.md (all technical decisions documented)
- ✅ data-model.md (entities, validation, data flow)
- ✅ contracts/mcp-tools.md (tool interface contracts)
- ✅ quickstart.md (user integration guide)
- ✅ QWEN.md (agent context updated)

**Task Generation Context**:
- 3 user stories (P1: COBOL source, P2: Copybook, P3: Configuration)
- 18 functional requirements
- 4 modules (server, tools, ssh_client, config)
- 3 test categories (contract, integration, unit)
- Tests: OPTIONAL (include if TDD approach requested)

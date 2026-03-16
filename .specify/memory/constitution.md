<!--
  Sync Impact Report
  ==================
  Version change: (none) → 1.0.0 (initial)
  Modified principles: (none - initial creation)
  Added sections: Core Principles (5), Security & Compliance, Development Workflow, Governance
  Removed sections: (none)
  Templates requiring updates:
    - ✅ .specify/templates/plan-template.md (compatible with Constitution Check gates)
    - ✅ .specify/templates/spec-template.md (compatible with mandatory sections)
    - ✅ .specify/templates/tasks-template.md (compatible with task categorization)
    - ✅ .qwen/commands/*.md (no outdated agent references)
  Follow-up TODOs: (none)
-->

# MCP Mainframe Constitution

## Core Principles

### I. Security-First (NON-NEGOTIABLE)

All mainframe connections MUST use SSH key-based authentication. Credentials MUST be provided exclusively via environment variables—never hardcoded in source files, logs, or tool outputs. The server MUST operate with least privilege (read-only access to source datasets). Security violations are automatically CRITICAL and require immediate remediation.

**Rationale**: Mainframe access involves sensitive production code; credential exposure or unauthorized modifications could have severe business impact.

### II. Configuration-Driven

All environment-specific parameters MUST be configurable via environment variables: `MF_HOST`, `MF_USER`, `MF_KEYFILE`, `COBOL_SRC_DSN`, `COPYBOOK_DSN`. The server MUST validate required variables on startup and exit with a clear error if missing. Default values are prohibited for connection parameters.

**Rationale**: Enables deployment across environments without code changes; prevents accidental commits of sensitive configuration.

### III. Modularity & Extensibility

The architecture MUST maintain clear separation between: MCP protocol handling, SSH communication, mainframe command generation, and configuration parsing. New tools (e.g., `get_jcl`, `list_programs`) MUST be addable without modifying core MCP logic. Each module MUST be independently testable.

**Rationale**: Facilitates future enhancements, simplifies testing, and isolates failure domains.

### IV. Observability & Debuggability

The server MUST log significant events (startup, tool invocation, errors) to stderr with configurable log levels (`LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR). Error messages MUST be user-friendly and actionable—never expose stack traces or internal details to end users. SSH connection errors, missing datasets, and permission issues MUST return specific, helpful messages.

**Rationale**: Enables troubleshooting without compromising security; supports production debugging.

### V. Performance & Resilience

Tool invocations SHOULD complete within 5 seconds for typical source retrieval. SSH connections SHOULD be reused across multiple tool calls within the same session. The server MUST handle network timeouts gracefully and implement retry logic for transient SSH failures (maximum one retry).

**Rationale**: Mainframe operations have latency; connection reuse reduces overhead; resilience prevents frustrating user experience.

## Security & Compliance

**Credential Handling**:
- SSH private keys MUST be referenced by file path, never embedded
- Passwords are prohibited; key-based authentication is mandatory
- Environment variables MUST be cleared from process memory after use where feasible

**Audit & Logging**:
- Logs MUST NOT contain credentials, dataset contents, or connection strings
- Log entries MUST include timestamps and operation identifiers
- Sensitive operations (connection attempts, dataset access) MUST be logged at INFO level

**Access Control**:
- The server MUST validate that the SSH user has read-only permissions on target datasets
- Write operations to mainframe datasets are explicitly out of scope

## Development Workflow

**Specification-Driven**:
- Every feature MUST start with a clear specification (WHAT/WHY) before technical planning (HOW)
- Success criteria MUST be measurable and technology-agnostic
- User stories MUST be independently testable and deliverable as incremental value

**Testing Requirements**:
- Unit tests REQUIRED for: environment variable parsing, SSH command mocking, tool handlers, error responses
- Integration tests OPTIONAL (requires test mainframe dataset)
- Manual testing REQUIRED: Verify tools appear in Continue.dev, execute real query

**Code Quality**:
- Python 3.10+ with type hints where beneficial
- Inline comments and docstrings MUST explain non-obvious logic
- Modular structure with clear separation of concerns

**Constitution Compliance**:
- All PRs and code reviews MUST verify compliance with these principles
- Complexity additions (new dependencies, architectural patterns) MUST be justified with rationale
- Use `.specify/templates/plan-template.md` Constitution Check gates to validate adherence

## Governance

**Authority**: This constitution supersedes all other development practices and guidelines within the project. Any conflicting practices in templates, commands, or documentation MUST be amended to align with these principles.

**Amendment Procedure**:
1. Propose amendment with clear rationale and impact analysis
2. Document version bump according to semantic versioning:
   - MAJOR: Backward-incompatible principle removals or redefinitions
   - MINOR: New principles added or materially expanded guidance
   - PATCH: Clarifications, wording refinements, non-semantic changes
3. Update `.specify/memory/constitution.md` with sync impact report
4. Propagate changes to dependent templates (plan, spec, tasks)
5. Commit with message: `docs: amend constitution to vX.Y.Z (description)`

**Compliance Review**:
- Every feature specification MUST pass Constitution Check gates in `plan.md`
- Violations MUST be documented in the Complexity Tracking table with justification
- Automated checks (where feasible) SHOULD validate principle adherence

**Version**: 1.0.0 | **Ratified**: 2026-03-16 | **Last Amended**: 2026-03-16

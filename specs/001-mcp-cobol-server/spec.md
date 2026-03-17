# Feature Specification: MCP COBOL Server

**Feature Branch**: `001-mcp-cobol-server`
**Created**: 2026-03-16
**Status**: Draft
**Input**: User description: "MCP COBOL server with get_cobol_source and get_copybook tools"

## User Scenarios & Testing

### User Story 1 - Retrieve COBOL Program Source (Priority: P1)

As a developer working with mainframe COBOL applications, I want to retrieve the latest source code for a specific COBOL program directly from the mainframe within my VS Code environment, so that I can understand the program's logic without manually accessing the mainframe or copying files.

**Why this priority**: This is the core value proposition of the feature—providing instant access to COBOL source code. Without this capability, the entire feature provides no value. This represents the minimum viable product.

**Independent Test**: Can be fully tested by requesting a known COBOL program (e.g., "PAYROLL") and verifying the source code is returned correctly. Delivers standalone value even without copybook retrieval.

**Acceptance Scenarios**:

1. **Given** the MCP server is configured with valid mainframe credentials, **When** I request source for an existing program named "PAYROLL", **Then** the complete COBOL source code is returned as plain text.
2. **Given** the MCP server is configured correctly, **When** I request source for a non-existent program, **Then** a clear error message indicates the program was not found.
3. **Given** the mainframe is unreachable, **When** I request any program source, **Then** a user-friendly error message indicates the connection issue without exposing technical details.

---

### User Story 2 - Retrieve Copybook Source (Priority: P2)

As a developer analyzing COBOL data structures, I want to retrieve copybook definitions directly from the mainframe, so that I can understand record layouts and field definitions without leaving my development environment.

**Why this priority**: Copybooks are essential for understanding COBOL data structures, but they are secondary to retrieving program source. This feature enhances the core capability but the system provides value without it.

**Independent Test**: Can be fully tested by requesting a known copybook (e.g., "CUST-REC") and verifying the copybook source is returned correctly. Works independently of program source retrieval.

**Acceptance Scenarios**:

1. **Given** the MCP server is configured with valid mainframe credentials, **When** I request a copybook named "CUST-REC", **Then** the complete copybook source is returned as plain text.
2. **Given** the MCP server is configured correctly, **When** I request a non-existent copybook, **Then** a clear error message indicates the copybook was not found.
3. **Given** the copybook dataset is accessible, **When** I request multiple different copybooks in sequence, **Then** each request returns the correct source independently.

---

### User Story 3 - Configure Mainframe Connection Securely (Priority: P3)

As a developer deploying this MCP server, I want to configure all mainframe connection parameters via environment variables, so that sensitive credentials are never hardcoded in source files and can be managed securely across different environments.

**Why this priority**: Security configuration is critical for production use but the feature can be demonstrated with hardcoded values during initial development. This becomes higher priority when moving to production.

**Independent Test**: Can be tested by setting environment variables and verifying the server uses them correctly, or by omitting required variables and verifying the server exits with a clear error message.

**Acceptance Scenarios**:

1. **Given** all required environment variables are set (MF_HOST, MF_USER, MF_KEYFILE, COBOL_SRC_DSN, COPYBOOK_DSN), **When** the MCP server starts, **Then** it initializes successfully and is ready to accept tool calls.
2. **Given** one or more required environment variables are missing, **When** the MCP server starts, **Then** it logs a clear error message indicating which variables are missing and exits gracefully.
3. **Given** the server is running, **When** I examine logs or tool outputs, **Then** no credentials, connection strings, or sensitive data are exposed.

---

### Edge Cases

- **What happens when** the mainframe SSH connection times out mid-request? The server returns a user-friendly timeout error message and logs the incident at WARNING level.
- **How does system handle** a program name with special characters or spaces? The server validates the program name and returns an error if it contains invalid characters.
- **What happens when** the user lacks read permissions for a dataset? The server returns a permission denied error without exposing internal details.
- **How does system handle** concurrent requests for the same program? Each request is processed independently; SSH connection reuse is managed internally.
- **What happens when** the dataset name is misconfigured? The server returns a clear error indicating the dataset could not be accessed.
- **What happens when** the maximum concurrent connection limit (5-10) is exceeded? Additional requests are queued or return a polite "server busy" message with a retry suggestion.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a tool named `get_cobol_source` that retrieves COBOL program source from the mainframe.
- **FR-002**: The `get_cobol_source` tool MUST accept a single required parameter `program` (the program name).
- **FR-003**: System MUST provide a tool named `get_copybook` that retrieves copybook source from the mainframe.
- **FR-004**: The `get_copybook` tool MUST accept a single required parameter `copybook` (the copybook name).
- **FR-005**: System MUST connect to the mainframe via SSH using key-based authentication.
- **FR-006**: System MUST retrieve source code from configurable mainframe datasets (PDS).
- **FR-007**: System MUST return retrieved source code as plain text.
- **FR-008**: System MUST return clear, user-friendly error messages when programs or copybooks are not found.
- **FR-009**: System MUST return clear, user-friendly error messages when connection failures occur.
- **FR-010**: System MUST accept all mainframe connection parameters via environment variables (MF_HOST, MF_USER, MF_KEYFILE, COBOL_SRC_DSN, COPYBOOK_DSN).
- **FR-011**: System MUST validate that all required environment variables are set on startup.
- **FR-012**: System MUST exit with a clear error message if required environment variables are missing.
- **FR-013**: System MUST log significant events (startup, tool invocation, errors) to stderr.
- **FR-014**: System MUST support configurable log levels (DEBUG, INFO, WARNING, ERROR) via LOG_LEVEL environment variable.
- **FR-015**: System MUST NOT expose credentials, dataset contents, or connection strings in logs or outputs.
- **FR-016**: System architecture MUST allow easy addition of new tools without modifying core MCP logic.
- **FR-017**: System MUST enforce a configurable maximum concurrent SSH connection limit (default: 5-10 connections).
- **FR-018**: System MUST handle excess requests gracefully by queuing or returning a "server busy" response with retry suggestion.

### Key Entities

- **COBOL Program**: A source code member stored in a mainframe PDS (Partitioned Data Set), containing executable COBOL logic.
- **Copybook**: A reusable COBOL source member containing data structure definitions, typically stored in a separate PDS.
- **MCP Tool**: A function exposed by the MCP server that can be invoked by AI assistants to perform specific operations.
- **Mainframe Dataset**: A z/OS data storage unit (PDS) containing source code members, accessible via SSH/USS filesystem paths.

**Clarification**: System assumes USS (UNIX System Services) is available on the mainframe for dataset access. TSO is not supported.

## Clarifications

### Session 2026-03-16

- Q: Which mainframe access method should be assumed as the primary/required approach? → A: USS (UNIX System Services) only
- Q: Should the system enforce any limits on concurrent requests or implement rate limiting? → A: Simple connection limit (5-10 concurrent SSH connections)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Developers can retrieve COBOL program source within 5 seconds for typical programs (under 10KB).
- **SC-002**: Developers can retrieve copybook source within 5 seconds for typical copybooks.
- **SC-003**: 100% of error scenarios return user-friendly error messages without exposing technical details or credentials.
- **SC-004**: Server starts successfully within 2 seconds when all required environment variables are provided.
- **SC-005**: Server exits gracefully with clear error messages when any required environment variable is missing.
- **SC-006**: Zero credentials or sensitive data exposed in logs during normal operation or error conditions.
- **SC-007**: New tools can be added by creating a single new file without modifying existing MCP server core logic.

# Design Documentation Template

## Purpose
Create comprehensive design documentation for COBOL programs, systems, and enhancements.

## Template Structure

```markdown
# Design Document: [System/Program Name]

**Document ID**: [DD-XXX]
**Version**: [X.X]
**Date**: [YYYY-MM-DD]
**Author**: [Name]
**Status**: [Draft/Review/Approved]

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Business Requirements](#2-business-requirements)
3. [System Overview](#3-system-overview)
4. [Architecture Design](#4-architecture-design)
5. [Detailed Design](#5-detailed-design)
6. [Data Design](#6-data-design)
7. [Interface Design](#7-interface-design)
8. [Error Handling](#8-error-handling)
9. [Security Design](#9-security-design)
10. [Testing Strategy](#10-testing-strategy)
11. [Migration Plan](#11-migration-plan)
12. [Appendices](#12-appendices)

---

## 1. Introduction

### 1.1 Purpose
[Describe the purpose of this design document and what system/program it covers]

### 1.2 Scope
**In Scope**:
- [Feature/capability 1]
- [Feature/capability 2]

**Out of Scope**:
- [What is explicitly excluded]

### 1.3 Definitions and Acronyms
| Term | Definition |
|------|-----------|
| [Term] | [Definition] |
| COBOL | Common Business Oriented Language |
| JCL | Job Control Language |
| VSAM | Virtual Storage Access Method |

### 1.4 References
| Document | Version | Date |
|----------|---------|------|
| [Requirements Document] | [Version] | [Date] |
| [Related Design Docs] | [Version] | [Date] |

---

## 2. Business Requirements

### 2.1 Business Problem
[Describe the business problem being solved]

### 2.2 Business Objectives
| Objective ID | Description | Priority |
|-------------|-------------|----------|
| BO-001 | [Objective] | High/Medium/Low |

### 2.3 Functional Requirements
| Req ID | Description | Priority | Design Decision |
|--------|-------------|----------|----------------|
| FR-001 | [Requirement] | High | [How addressed in design] |

### 2.4 Non-Functional Requirements
| Req ID | Category | Description | Design Decision |
|--------|----------|-------------|----------------|
| NFR-001 | Performance | [Requirement] | [How addressed] |
| NFR-002 | Security | [Requirement] | [How addressed] |

---

## 3. System Overview

### 3.1 Current State (As-Is)
[Describe existing system if this is an enhancement/modification]

```
[Current State Diagram]
```

### 3.2 Future State (To-Be)
[Describe the new/modified system]

```
[Future State Diagram]
```

### 3.3 System Context
```
[Context Diagram showing system boundaries and external interfaces]
```

**External Systems**:
| System | Interface Type | Data Flow |
|--------|---------------|-----------|
| [System 1] | [File/API/DB] | [In/Out/Both] |

---

## 4. Architecture Design

### 4.1 High-Level Architecture
```
[Architecture Diagram]
```

### 4.2 Component Overview
| Component | Type | Purpose | Technology |
|-----------|------|---------|------------|
| [Component 1] | [Batch/Online] | [Purpose] | [COBOL/JCL/DB2] |

### 4.3 Processing Model
**Batch Processing**:
- [Describe batch jobs and schedules]

**Online Processing** (if applicable):
- [Describe online transactions]

### 4.4 Data Flow Architecture
```
[Data Flow Diagram]
```

**Data Flow Description**:
1. [Step 1: Data ingestion]
2. [Step 2: Processing]
3. [Step 3: Output]

---

## 5. Detailed Design

### 5.1 Program Structure

#### [Program Name 1]
**Purpose**: [What this program does]

**Design**:
```
[Program Flow Chart or Pseudocode]
```

**Key Processing Logic**:
[Describe algorithms, calculations, business rules]

**Dependencies**:
- [Programs this program calls]
- [Programs that call this program]

#### [Program Name 2]
[Repeat structure for each program]

### 5.2 Job Design (Batch)

#### [Job Name 1]
**Purpose**: [What this job does]

**JCL Structure**:
```
[Job Flow Diagram]
```

**Steps**:
| Step | Program | Purpose | Conditions |
|------|---------|---------|------------|
| STEP001 | [PGM] | [Purpose] | [Always/Conditional] |

### 5.3 Business Rules Implementation

| Rule ID | Business Rule | Implementation |
|---------|--------------|----------------|
| BR-001 | [Rule description] | [How implemented in code] |

---

## 6. Data Design

### 6.1 Data Entities
| Entity | Description | Storage |
|--------|-------------|---------|
| [Entity 1] | [Description] | [VSAM/DB2/Flat file] |

### 6.2 File/Database Design

#### [File/Database Name 1]
**Type**: [VSAM/DB2/Flat file]
**Organization**: [KSDS/ESDS/Relational/Sequential]

**Record Layout**:
```cobol
01  RECORD-LAYOUT.
    05  FIELD-1          PIC X(10).
    05  FIELD-2          PIC 9(8)V99.
    05  FIELD-3          PIC X(30).
```

**Field Definitions**:
| Field Name | Type | Length | Description |
|------------|------|--------|-------------|
| FIELD-1 | Alphanumeric | 10 | [Description] |

**Indexes/Keys** (if applicable):
| Key Name | Fields | Type |
|----------|--------|------|
| PRIMARY | FIELD-1 | Unique/Non-unique |

### 6.3 Data Relationships
```
[Entity Relationship Diagram]
```

### 6.4 Data Volume and Growth
| Dataset | Current Records | Growth Rate | Retention |
|---------|----------------|-------------|-----------|
| [Dataset] | [Number] | [%/period] | [Days/Years] |

---

## 7. Interface Design

### 7.1 Input Interfaces

#### [Interface Name 1]
**Source**: [System/Department]
**Format**: [File format/API/Message]
**Frequency**: [Real-time/Batch schedule]
**Volume**: [Records per transaction/day]

**Input Layout**:
[Show input record structure]

**Validation Rules**:
- [Validation rule 1]
- [Validation rule 2]

### 7.2 Output Interfaces

#### [Interface Name 1]
**Destination**: [System/Department]
**Format**: [File format/Report/API]
**Frequency**: [When generated]
**Volume**: [Records per output]

**Output Layout**:
[Show output record structure]

### 7.3 External APIs (if applicable)
| API | Method | Purpose | Request/Response |
|-----|--------|---------|-----------------|
| [API Name] | [GET/POST] | [Purpose] | [Format] |

---

## 8. Error Handling

### 8.1 Error Categories
| Category | Description | Action |
|----------|-------------|--------|
| Data Errors | Invalid input data | Log and reject |
| System Errors | System failures | Retry or abort |
| Business Errors | Business rule violations | Log and flag |

### 8.2 Error Handling Strategy
**Program Level**:
- [How errors are handled in each program]

**Job Level**:
- [How errors are handled in job streams]

### 8.3 Error Codes and Messages
| Code | Severity | Message | Action |
|------|----------|---------|--------|
| 00 | Success | Processing completed | Continue |
| 04 | Warning | [Message] | Review and continue |
| 08 | Error | [Message] | Investigate |
| 12 | Severe | [Message] | Abort and notify |

### 8.4 Recovery Procedures
**Automatic Recovery**:
- [What the system handles automatically]

**Manual Recovery**:
- [When human intervention is required]

**Restart Procedures**:
- [How to restart after failure]

---

## 9. Security Design

### 9.1 Access Control
**Program Access**:
| Program | Access Level | Authorization |
|---------|-------------|---------------|
| [Program] | [Read/Update/Admin] | [RACF/ACF2] |

**Data Access**:
| Dataset | Access Level | Authorization |
|---------|-------------|---------------|
| [Dataset] | [Read/Update] | [RACF/ACF2] |

### 9.2 Data Security
**Sensitive Data**:
- [List sensitive data elements]

**Protection Measures**:
- [Encryption/Masking/Access controls]

### 9.3 Audit Requirements
**Audit Trail**:
- [What is logged]
- [Where logs are stored]
- [Retention period]

---

## 10. Testing Strategy

### 10.1 Testing Approach
**Unit Testing**:
- [What will be tested at unit level]

**Integration Testing**:
- [What will be tested at integration level]

**System Testing**:
- [What will be tested at system level]

### 10.2 Test Scenarios
| Scenario ID | Description | Expected Result |
|------------|-------------|-----------------|
| TS-001 | [Scenario] | [Expected outcome] |

### 10.3 Test Data Requirements
**Test Data Needs**:
- [Describe test data requirements]

**Data Masking** (if needed):
- [Describe data masking requirements]

---

## 11. Migration Plan

### 11.1 Migration Approach
**Migration Type**:
- [ ] Big Bang
- [ ] Phased
- [ ] Parallel Run
- [ ] Pilot

### 11.2 Migration Steps
1. [Step 1: Preparation]
2. [Step 2: Data migration]
3. [Step 3: System deployment]
4. [Step 4: Validation]
5. [Step 5: Cutover]

### 11.3 Rollback Plan
**If Migration Fails**:
1. [Rollback step 1]
2. [Rollback step 2]
3. [Rollback step 3]

### 11.4 Success Criteria
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

---

## 12. Appendices

### Appendix A: Related Documents
[List all related documents]

### Appendix B: Technical Specifications
[Detailed technical specifications]

### Appendix C: Code Samples
[Sample code for key logic]

### Appendix D: Review and Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | [Name] | | [Date] |
| Reviewer | [Name] | | [Date] |
| Approver | [Name] | | [Date] |

### Appendix E: Change History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial version |
| 1.1 | [Date] | [Name] | [Description] |
```

## Usage Guidelines

### When to Use
- New program development
- Major enhancements
- System modifications
- Compliance documentation

### Review Process
1. **Technical Review**: By development team
2. **Business Review**: By business stakeholders
3. **Security Review**: By security team (if applicable)
4. **Operations Review**: By operations team

### Maintenance
- Update design document when requirements change
- Maintain version control
- Keep approval records

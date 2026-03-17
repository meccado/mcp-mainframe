# JCL Explanation and Documentation Prompt

## Purpose
Explain and document JCL (Job Control Language) job streams, procedures, and steps in clear, understandable terms.

## Instructions

When explaining or documenting JCL, use this structure:

### 1. Job Overview
```markdown
## Job Overview

**Job Name**: [job-name]
**Job Number**: [job-id if applicable]
**Type**: [Batch/ Scheduled/On-demand]
**Priority**: [job class/priority]

### Business Purpose
[Describe what business function this job performs]

### Executive Summary
[2-3 sentence summary suitable for management]

**Example**: "This nightly job processes all customer transactions from the previous day, updates account balances, and generates exception reports for the operations team."
```

### 2. Job Flow Diagram
```markdown
## Job Flow

```
[JOB: jobname]
    |
    +-- STEP001: [Step name and purpose]
    |       |
    |       +-- Program: [program-name]
    |       +-- Input: [input-dataset]
    |       +-- Output: [output-dataset]
    |
    +-- STEP002: [Step name and purpose]
    |       |
    |       +-- Program: [program-name]
    |       ...
    |
    +-- STEP003: [Conditional step]
            |
            +-- IF: [condition from previous step]
            +-- Program: [program-name]
```

**Flow Description**:
[Explain the flow in plain English]
```

### 3. Step-by-Step Explanation

For each step in the job:

```markdown
### STEP[XXX]: [step-name] - [Purpose]

**Program**: [program-name or utility]
**Condition**: [RUN/IF condition]
**Return Codes**: [Expected return codes and meanings]

#### What This Step Does
[Plain English explanation of step purpose and function]

#### Input
| DD Name | Dataset | DISP | Purpose |
|---------|---------|------|---------|
| SYSIN | [dataset/name] | SHR | Control cards/parameters |
| INPUT | [dataset/name] | SHR | Input data file |

#### Output
| DD Name | Dataset | DISP | Purpose |
|---------|---------|------|---------|
| SYSOUT | [class] | * | Spool output |
| OUTPUT | [dataset/name] | NEW | Output results |

#### Processing Logic
[Explain what the program does with the input to produce output]

#### Key Parameters
```jcl
[Show relevant JCL statements]
```

**Parameter Explanation**:
- `PARM='value'` - [What this parameter controls]
- `COND=(code,operator)` - [When this step runs]
- `REGION=nnnnK` - [Memory allocation]

#### Success Criteria
- **Expected Return Code**: 0
- **Expected Output**: [Description of successful output]
- **Validation**: [How to verify step completed successfully]

#### Failure Scenarios
| Return Code | Meaning | Common Causes | Action |
|-------------|---------|---------------|--------|
| 00 | Success | - | Continue to next step |
| 04 | Warning | [Common causes] | Review output, may continue |
| 08 | Error | [Common causes] | Investigate, may need rerun |
| 12 | Severe | [Common causes] | Stop job, fix required |
```

### 4. Dataset Reference
```markdown
## Dataset Reference

### Input Datasets
| Dataset Name | DD Name | DISP | Space | Record Format | Purpose |
|-------------|---------|------|-------|---------------|---------|
| [dsn] | [dd] | SHR | [space] | [recfm] | [purpose] |

### Output Datasets
| Dataset Name | DD Name | DISP | Space | Record Format | Purpose | Retention |
|-------------|---------|------|-------|---------------|---------|-----------|
| [dsn] | [dd] | CATLG | [space] | [recfm] | [purpose] | [days] |

### Temporary Datasets
| DD Name | Purpose | Deleted When |
|---------|---------|--------------|
| [&&temp] | [purpose] | Job step completion |
```

### 5. Schedule and Dependencies
```markdown
## Schedule and Dependencies

### Schedule
- **Frequency**: [Daily/Weekly/Monthly/On-demand]
- **Time**: [HH:MM in 24-hour format]
- **Timezone**: [EST/CST/PST/etc.]
- **Calendar**: [Business days/All days/Custom]

### Dependencies
**This Job Depends On**:
- [Job/Process 1] - [What it provides]
- [Job/Process 2] - [What it provides]

**Jobs That Depend On This**:
- [Job 1] - [What it needs from this job]
- [Job 2] - [What it needs from this job]

### Critical Path
[Explain where this job fits in the overall processing schedule]
```

### 6. Operations Guide
```markdown
## Operations Guide

### How to Monitor
1. **Check Job Status**: [Command or tool]
2. **Review Output**: [Where to find SYSOUT]
3. **Verify Results**: [Validation steps]

### Common Issues and Resolutions

#### Issue: [Problem description]
**Symptoms**:
- [Symptom 1]
- [Symptom 2]

**Root Cause**:
[Explanation of what causes this issue]

**Resolution**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Prevention**:
[How to prevent this issue in the future]

### Restart Procedures
**If job fails at STEP001**:
1. [Action 1]
2. [Action 2]
3. Restart command: `//STEP001 EXEC PGM=...,RESTART=STEP001`

**If job fails at STEP002**:
[Similar instructions]

### Emergency Contacts
| Role | Name | Contact |
|------|------|---------|
| On-call Support | [Team] | [Phone/Email] |
| Application Owner | [Name] | [Phone/Email] |
| Operations | [Team] | [Phone] |
```

### 7. JCL Code Reference
```markdown
## Complete JCL Listing

```jcl
[Include complete, well-commented JCL code]
//JOBNAME  JOB (ACCOUNT),'DESCRIPTION',CLASS=A,MSGCLASS=X
//***********************************************************
//* STEP001: [Description]
//***********************************************************
//STEP001  EXEC PGM=PROGRAM1
//INPUT    DD DSN=INPUT.DATASET,DISP=SHR
//OUTPUT   DD DSN=OUTPUT.DATASET,DISP=(NEW,CATLG),
//            SPACE=(CYL,(10,5)),UNIT=SYSDA
//SYSOUT   DD SYSOUT=*
//...
```

### Code Annotations
[Add line-by-line or section-by-section explanations]
```

### 8. Change History
```markdown
## Change History

| Date | Author | Change Description | Steps Affected |
|------|--------|-------------------|----------------|
| YYYY-MM-DD | [Name] | Initial version | All |
| YYYY-MM-DD | [Name] | Added STEP003 | Added STEP003 |
| YYYY-MM-DD | [Name] | Changed schedule | N/A |
```

## Special JCL Constructs Explained

### Conditional Processing
```markdown
### IF/THEN/ELSE Logic

**Condition**: `IF STEP001.RC = 0 THEN`
**Meaning**: "If step STEP001 completed successfully (return code 0)"
**Action**: [What happens when condition is true]

**Condition**: `IF STEP002.RC > 4 THEN`
**Meaning**: "If step STEP002 had an error (return code greater than 4)"
**Action**: [What happens when condition is true]
```

### Procedure Calls
```markdown
### PROC [procedure-name]

**What It Is**: [Reusable JCL template]
**Parameters**:
- `&PARAM1` - [Description, default value]
- `&PARAM2` - [Description, default value]

**Called With**:
```jcl
//STEP001 EXEC PROC=PROCNAME,PARAM1='value1'
```
```

### Utilities Explained
```markdown
### IEBGENER
**Purpose**: Copy datasets
**What It Does**: [Plain English explanation]

### SORT (DFSORT/SyncSort)
**Purpose**: Sort, merge, copy data
**What It Does**: [Plain English explanation]
**Sort Keys**: [Fields used for sorting]

### IDCAMS
**Purpose**: Define and manage VSAM datasets
**What It Does**: [Plain English explanation]
```

## Writing Guidelines

### Do
- ✅ Explain business purpose first
- ✅ Use clear step names
- ✅ Comment JCL thoroughly
- ✅ Explain return codes
- ✅ Include restart procedures
- ✅ Document all datasets

### Don't
- ❌ Use cryptic step names
- ❌ Leave return codes unexplained
- ❌ Omit dataset information
- ❌ Skip restart instructions
- ❌ Use undefined abbreviations

## Example Output

See the structure above for a complete example. Each section should be filled in with specific details from the JCL being documented.

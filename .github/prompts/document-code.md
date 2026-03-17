# Code Documentation Prompt

## Purpose
Generate comprehensive documentation for COBOL programs and related mainframe artifacts.

## Instructions

When documenting COBOL code, follow this structure:

### 1. Program Overview
```markdown
## Program Overview

**Program Name**: [program-name]
**Type**: [Batch/Online/Utility]
**Module**: [module/functional-area]

### Business Purpose
[Describe what business problem this program solves]

### Technical Summary
[Brief technical description of program functionality]
```

### 2. Program Structure
```markdown
## Program Structure

### Divisions
- **Identification Division**: Program ID, author, date
- **Environment Division**: System configuration, file assignments
- **Data Division**: 
  - File Section (FD entries)
  - Working-Storage Section
  - Linkage Section (if called program)
- **Procedure Division**: Main logic and paragraphs
```

### 3. File Dependencies
```markdown
## File Dependencies

| DD Name | Dataset Name | DISP | Purpose |
|---------|-------------|------|---------|
| SYSIN | [dataset] | SHR | Input parameters |
| SYSOUT | [dataset] | NEW | Output report |
| INPUT-FILE | [dataset] | SHR | Input data |
| OUTPUT-FILE | [dataset] | OLD | Output results |
```

### 4. Data Structures
```markdown
## Key Data Structures

### [Copybook/Structure Name]
```cobol
[Show key record layout]
```

**Fields**:
- [Field-1] - [Description, picture clause, usage]
- [Field-2] - [Description, picture clause, usage]
```

### 5. Processing Logic
```markdown
## Processing Logic

### Main Flow
1. [Step 1: Initialization]
2. [Step 2: Input processing]
3. [Step 3: Business logic]
4. [Step 4: Output generation]
5. [Step 5: Cleanup]

### Key Paragraphs/Sections
- [Paragraph-1] - [Purpose and logic]
- [Paragraph-2] - [Purpose and logic]
```

### 6. Error Handling
```markdown
## Error Handling

| Error Code | Condition | Action |
|------------|-----------|--------|
| 00 | Success | Normal completion |
| 08 | Warning | Processing completed with warnings |
| 12 | Error | Processing terminated |
| 16 | Severe | Abnormal termination |
```

### 7. Change History
```markdown
## Change History

| Date | Author | Change Description |
|------|--------|-------------------|
| YYYY-MM-DD | [Name] | Initial version |
| YYYY-MM-DD | [Name] | [Description of change] |
```

## Example Usage

**Input**: COBOL source code
**Output**: Complete program documentation in markdown format

## Tips

- Use clear, concise language
- Include business context, not just technical details
- Document all file dependencies
- Explain complex calculations or business rules
- Note any assumptions or limitations
- Include examples for complex logic

# Code Documentation Instructions

## Purpose
Generate comprehensive documentation for COBOL programs.

## Steps

### 1. Program Overview
- Extract program name from IDENTIFICATION DIVISION
- Identify program type (Batch/Online/Utility)
- Summarize business purpose in 2-3 sentences
- List technical summary

### 2. Program Structure
Document:
- Identification Division details (Author, Date, Program ID)
- Environment Division (System configuration)
- Data Division (File Section, Working-Storage, Linkage)
- Procedure Division (Main paragraphs)

### 3. File Dependencies
Create table with:
| DD Name | Dataset | DISP | Purpose |
|---------|---------|------|---------|

### 4. Data Structures
For each copybook/structure:
- Show record layout
- List key fields with descriptions
- Note picture clauses and usage

### 5. Processing Logic
Document:
- Main flow (5-7 steps)
- Key paragraphs with purposes
- Business rules implemented

### 6. Error Handling
List:
- Error codes and meanings
- Error handling approach
- Recovery procedures

### 7. Change History
Track:
- Date, Author, Description

## Examples

See `document-code.prompt.md` for example output format.

## Best Practices

- Use clear, concise language
- Include business context
- Document all file dependencies
- Explain complex calculations
- Note assumptions and limitations

## References

- [COBOL Programming Standards](../../docs/standards.md)
- [Documentation Guidelines](../../docs/documentation.md)

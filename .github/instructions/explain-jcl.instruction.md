# JCL Documentation Instructions

## Purpose
Document and explain JCL job streams.

## Steps

### 1. Job Overview
Document:
- Job name, number, type
- Business purpose
- Executive summary

### 2. Job Flow
Create:
- Visual flow diagram
- Step descriptions
- Conditional logic

### 3. Step-by-Step
For each step:
- Step name and purpose
- Program/utility used
- Input datasets
- Output datasets
- Processing logic
- Success criteria
- Failure scenarios

### 4. Dataset Reference
List:
- Input datasets (name, DD, DISP, purpose)
- Output datasets (name, DD, DISP, retention)
- Temporary datasets

### 5. Schedule & Dependencies
Document:
- Frequency and timing
- Predecessor jobs
- Successor jobs
- Critical path

### 6. Operations Guide
Provide:
- Monitoring instructions
- Common issues and resolutions
- Restart procedures
- Emergency contacts

## Examples

See `explain-jcl.prompt.md` for format.

## Best Practices

- Explain business purpose first
- Use clear step names
- Comment JCL thoroughly
- Document return codes
- Include restart procedures

## References

- [JCL Standards](../../docs/jcl-standards.md)
- [Operations Guide](../../docs/operations.md)

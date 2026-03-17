# Code Review Instructions

## Purpose
Conduct standardized code reviews for COBOL programs.

## Steps

### 1. Functionality Review
Check:
- Requirements coverage
- Business logic correctness
- Test coverage

### 2. Code Quality Review
Assess:
- Code structure
- Naming conventions
- Code readability
- Comments and documentation

### 3. Performance Review
Evaluate:
- Efficiency (file access, processing)
- Resource usage (memory, CPU)

### 4. Security Review
Check:
- Data security
- Access control
- Audit requirements

### 5. Error Handling Review
Verify:
- Error detection
- Error recovery
- Error messages

### 6. Maintainability Review
Assess:
- Modularity
- Changeability
- Technical debt

### 7. Document Issues
Categorize by severity:
- **Critical**: Must fix before merge
- **High**: Should fix soon
- **Medium**: Consider fixing
- **Low**: Suggestions

### 8. Make Recommendation
Choose:
- Approved
- Approved with Comments
- Changes Required
- Rejected

## Examples

See `code-review.template.md` for review format.

## Best Practices

- Be constructive and specific
- Focus on code, not person
- Provide actionable feedback
- Be timely (within SLA)
- Follow up on actions

## Severity Definitions

- **Critical**: Blocks merge, affects correctness/security
- **High**: Affects quality, should fix in sprint
- **Medium**: Improves maintainability
- **Low**: Nice to have

## References

- [Code Review Guide](../../docs/code-review.md)
- [Coding Standards](../../docs/standards.md)

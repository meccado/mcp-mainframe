# Code Analysis Prompt

## Purpose
Perform comprehensive static code analysis on COBOL programs to identify issues, improvements, and best practices.

## Instructions

When analyzing COBOL code, provide feedback in these categories:

### 1. Code Quality Metrics
```markdown
## Code Quality Metrics

**Lines of Code**: [total]
**Complexity Score**: [low/medium/high]
**Maintainability Index**: [score 0-100]
**Comment Density**: [percentage]
```

### 2. Structure Analysis
```markdown
## Structure Analysis

### Strengths
- ✅ [Well-structured paragraphs]
- ✅ [Clear variable naming]
- ✅ [Proper division organization]

### Areas for Improvement
- ⚠️ [Long paragraphs that should be split]
- ⚠️ [Magic numbers that should be constants]
- ⚠️ [Missing error handling]
```

### 3. Best Practices Compliance
```markdown
## Best Practices Compliance

| Category | Status | Notes |
|----------|--------|-------|
| Naming Conventions | ✅/⚠️/❌ | [Details] |
| Code Organization | ✅/⚠️/❌ | [Details] |
| Error Handling | ✅/⚠️/❌ | [Details] |
| Comments | ✅/⚠️/❌ | [Details] |
| Performance | ✅/⚠️/❌ | [Details] |
| Security | ✅/⚠️/❌ | [Details] |
```

### 4. Issues Found
```markdown
## Issues Found

### Critical
- [ ] **Line XX**: [Description of critical issue]
  - **Impact**: [Business/technical impact]
  - **Fix**: [Recommended fix]

### High Priority
- [ ] **Line XX**: [Description of high priority issue]
  - **Impact**: [Business/technical impact]
  - **Fix**: [Recommended fix]

### Medium Priority
- [ ] **Line XX**: [Description of medium priority issue]
  - **Impact**: [Business/technical impact]
  - **Fix**: [Recommended fix]

### Low Priority / Suggestions
- [ ] **Line XX**: [Description of suggestion]
  - **Benefit**: [What improvement this brings]
```

### 5. Specific Analysis Areas

#### A. Variable Usage
- Check for unused variables
- Identify variables that could be constants
- Find poorly named variables
- Detect potential data type issues

#### B. Control Structures
- Review PERFORM loops for proper termination
- Check IF statements for completeness
- Identify nested complexity
- Find potential infinite loops

#### C. File Handling
- Verify all files are properly opened/closed
- Check for missing error handling on I/O
- Review file status checking
- Identify inefficient file access patterns

#### D. Error Handling
- Check for consistent error handling
- Verify error codes are meaningful
- Review error message clarity
- Identify missing error scenarios

#### E. Performance
- Identify inefficient loops
- Find redundant computations
- Check for optimal file access
- Review memory usage patterns

#### F. Security
- Check for hardcoded credentials
- Review input validation
- Check for SQL injection risks (if embedded SQL)
- Verify proper authorization checks

### 6. Recommendations Summary
```markdown
## Recommendations Summary

### Immediate Actions (Do Now)
1. [Critical fix 1]
2. [Critical fix 2]

### Short-term Improvements (This Sprint)
1. [High priority improvement 1]
2. [High priority improvement 2]

### Long-term Enhancements (Backlog)
1. [Medium priority enhancement 1]
2. [Medium priority enhancement 2]

### Technical Debt
- [List technical debt items with priority]
```

### 7. Modernization Opportunities
```markdown
## Modernization Opportunities

| Current Approach | Modern Alternative | Effort | Benefit |
|-----------------|-------------------|--------|---------|
| [e.g., Sequential file] | [e.g., VSAM/DB2] | Low/Med/High | [Description] |
| [e.g., DISPLAY for logging] | [e.g., Structured logging] | Low | [Description] |
```

## Example Usage

**Input**: COBOL source code
**Output**: Comprehensive code analysis report with actionable recommendations

## Scoring Guide

- ✅ **Compliant**: Meets best practice standards
- ⚠️ **Partial Compliance**: Some issues found, needs improvement
- ❌ **Non-Compliant**: Significant issues, requires immediate attention

## Priority Levels

- **Critical**: Must fix immediately - affects correctness, security, or stability
- **High**: Should fix soon - affects maintainability or performance
- **Medium**: Should consider - improves code quality
- **Low**: Nice to have - minor improvements

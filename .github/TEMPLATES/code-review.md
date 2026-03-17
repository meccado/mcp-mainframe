# Code Review Template

## Purpose
Standardize code reviews for COBOL programs to ensure quality, maintainability, and best practices.

## Review Template

```markdown
# Code Review: [Program/Job Name]

**Review ID**: [CR-XXX]
**Date**: [YYYY-MM-DD]
**Reviewer**: [Name]
**Author**: [Name]
**Change Type**: [New/Enhancement/Bug Fix/Refactoring]

---

## Review Summary

| Aspect | Rating | Notes |
|--------|--------|-------|
| Functionality | ✅/⚠️/❌ | [Summary] |
| Code Quality | ✅/⚠️/❌ | [Summary] |
| Performance | ✅/⚠️/❌ | [Summary] |
| Security | ✅/⚠️/❌ | [Summary] |
| Maintainability | ✅/⚠️/❌ | [Summary] |
| Documentation | ✅/⚠️/❌ | [Summary] |

**Overall Status**: 
- [ ] **Approved** - Ready for merge/deployment
- [ ] **Approved with Comments** - Minor issues to address
- [ ] **Changes Required** - Must address before merge
- [ ] **Rejected** - Major redesign needed

---

## 1. Functionality Review

### 1.1 Requirements Coverage
| Req ID | Requirement | Implemented | Tested | Notes |
|--------|-------------|-------------|--------|-------|
| FR-001 | [Requirement] | ✅/❌ | ✅/❌ | [Notes] |

### 1.2 Business Logic
**Correctness**:
- [ ] Business rules correctly implemented
- [ ] Calculations are accurate
- [ ] Edge cases handled

**Issues Found**:
| Severity | Line | Issue | Recommendation |
|----------|------|-------|----------------|
| High/Med/Low | [Line #] | [Description] | [Fix] |

### 1.3 Test Coverage
- [ ] Unit tests provided
- [ ] Test cases cover normal flow
- [ ] Test cases cover error scenarios
- [ ] Test cases cover edge cases

**Test Quality**: [Comments on test coverage]

---

## 2. Code Quality Review

### 2.1 Code Structure
**Organization**:
- [ ] Programs are well-organized
- [ ] Paragraphs have clear purposes
- [ ] No duplicate code
- [ ] Proper separation of concerns

**Comments**: [Specific feedback on structure]

### 2.2 Naming Conventions
**Standards Compliance**:
- [ ] Program names follow standards
- [ ] Variable names are meaningful
- [ ] Paragraph names are descriptive
- [ ] Copybook names follow standards

**Issues**:
| Item | Current Name | Suggested Name | Reason |
|------|-------------|----------------|--------|
| [Variable] | [Name] | [Better name] | [Reason] |

### 2.3 Code Readability
- [ ] Code is easy to understand
- [ ] Complex logic is well-commented
- [ ] No overly long paragraphs (>50 lines)
- [ ] Consistent indentation and formatting

**Suggestions**: [Specific readability improvements]

### 2.4 Comments and Documentation
**Inline Comments**:
- [ ] Sufficient comments for complex logic
- [ ] Comments are accurate and up-to-date
- [ ] No commented-out code
- [ ] Header comments include program info

**Documentation**:
- [ ] Program documentation updated
- [ ] Copybook documentation complete
- [ ] JCL documentation provided (if applicable)

---

## 3. Performance Review

### 3.1 Efficiency
**File Access**:
- [ ] Efficient file access patterns
- [ ] Proper use of indexed access
- [ ] Minimal I/O operations
- [ ] Appropriate buffer sizes

**Processing**:
- [ ] No unnecessary loops
- [ ] Efficient sorting/searching
- [ ] Minimal data movement
- [ ] Appropriate use of tables

### 3.2 Resource Usage
**Memory**:
- [ ] Working storage appropriately sized
- [ ] No excessive memory allocation
- [ ] Proper use of REDEFINES

**CPU**:
- [ ] No CPU-intensive operations in loops
- [ ] Efficient arithmetic operations
- [ ] Appropriate use of built-in functions

**Performance Issues**:
| Issue | Impact | Recommendation |
|-------|--------|----------------|
| [Issue] | High/Med/Low | [Fix] |

---

## 4. Security Review

### 4.1 Data Security
- [ ] No hardcoded passwords or credentials
- [ ] Sensitive data properly protected
- [ ] Input validation implemented
- [ ] No SQL injection vulnerabilities (if embedded SQL)

### 4.2 Access Control
- [ ] Proper authorization checks
- [ ] Audit logging implemented (if required)
- [ ] No unauthorized data access

### 4.3 Security Issues
| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| Critical/High/Med | [Issue] | [Line/Section] | [Fix] |

---

## 5. Error Handling Review

### 5.1 Error Detection
- [ ] All file status codes checked
- [ ] Return codes properly validated
- [ ] Input data validated
- [ ] Boundary conditions checked

### 5.2 Error Recovery
- [ ] Appropriate error messages
- [ ] Graceful degradation
- [ ] Proper cleanup on errors
- [ ] Restart capability (if batch)

### 5.3 Error Handling Issues
| Issue | Current Behavior | Recommended Behavior |
|-------|-----------------|---------------------|
| [Issue] | [What happens now] | [What should happen] |

---

## 6. Maintainability Review

### 6.1 Modularity
- [ ] Programs are appropriately sized
- [ ] Reusable components identified
- [ ] Copybooks used for common code
- [ ] Clear interfaces between modules

### 6.2 Changeability
- [ ] Easy to modify
- [ ] Minimal coupling between modules
- [ ] Configuration parameters externalized
- [ ] No magic numbers (use constants)

### 6.3 Technical Debt
**New Technical Debt Introduced**:
| Item | Impact | Should Fix When |
|------|--------|----------------|
| [Debt item] | High/Med/Low | [Now/Soon/Later] |

---

## 7. Specific Code Issues

### 7.1 Critical Issues (Must Fix)
| # | Line | Issue | Impact | Fix |
|---|------|-------|--------|-----|
| 1 | [Line] | [Description] | [Impact] | [Fix] |

### 7.2 High Priority Issues (Should Fix)
| # | Line | Issue | Impact | Fix |
|---|------|-------|--------|-----|
| 1 | [Line] | [Description] | [Impact] | [Fix] |

### 7.3 Medium Priority Issues (Consider Fixing)
| # | Line | Issue | Impact | Fix |
|---|------|-------|--------|-----|
| 1 | [Line] | [Description] | [Impact] | [Fix] |

### 7.4 Suggestions (Nice to Have)
| # | Line | Suggestion | Benefit |
|---|------|------------|---------|
| 1 | [Line] | [Suggestion] | [Benefit] |

---

## 8. Deployment Readiness

### 8.1 Prerequisites
- [ ] All dependencies identified
- [ ] JCL updated (if applicable)
- [ ] Control tables updated (if applicable)
- [ ] Database changes scripted (if applicable)

### 8.2 Documentation
- [ ] User documentation updated
- [ ] Operations documentation complete
- [ ] Support procedures documented
- [ ] Training materials updated (if needed)

### 8.3 Testing Evidence
- [ ] Unit test results provided
- [ ] Integration test results provided
- [ ] Performance test results (if applicable)
- [ ] User acceptance test sign-off (if applicable)

### 8.4 Rollback Plan
- [ ] Rollback procedure documented
- [ ] Rollback tested (if complex)
- [ ] Data recovery procedure defined

---

## 9. Review Actions

### Actions for Author
| # | Action | Priority | Due Date | Status |
|---|--------|----------|----------|--------|
| 1 | [Action] | High/Med/Low | [Date] | Open |

### Actions for Reviewer
| # | Action | Priority | Due Date | Status |
|---|--------|----------|----------|--------|
| 1 | [Action] | High/Med/Low | [Date] | Open |

---

## 10. Approval

### Review Decision
- [ ] **Approved** - Code meets all standards, ready for merge
- [ ] **Approved with Minor Changes** - Address comments, no re-review needed
- [ ] **Changes Required** - Address issues, re-review required
- [ ] **Rejected** - Significant redesign needed

### Sign-off
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Reviewer | [Name] | | [Date] |
| Author (acknowledgment) | [Name] | | [Date] |

### Re-Review (if required)
| Date | Reviewer | Status | Notes |
|------|----------|--------|-------|
| [Date] | [Name] | Pass/Fail | [Notes] |

---

## Appendix: Review Checklist

### Quick Reference Checklist
- [ ] Code compiles without errors
- [ ] Code compiles without warnings
- [ ] All requirements implemented
- [ ] Test cases provided and passing
- [ ] No security vulnerabilities
- [ ] Error handling complete
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Follows coding standards
- [ ] No unnecessary complexity

### Common COBOL Issues to Check
- [ ] File status codes checked after every I/O
- [ ] Subscript bounds validated
- [ ] Numeric fields validated before COMPUTE
- [ ] No uninitialized variables
- [ ] Proper use of ON SIZE ERROR
- [ ] Appropriate PIC clauses
- [ ] Consistent date formats
- [ ] Proper SORT usage

---

## Notes for Reviewers

### Review Guidelines
1. **Be constructive** - Focus on code, not the person
2. **Be specific** - Provide exact line numbers and suggestions
3. **Be timely** - Complete reviews within [SLA]
4. **Be thorough** - Don't rush, quality matters
5. **Be consistent** - Apply same standards to all code

### Severity Definitions
- **Critical**: Must fix immediately, blocks merge
- **High**: Should fix soon, affects quality/security
- **Medium**: Consider fixing, improves maintainability
- **Low**: Nice to have, minor improvement

### When to Escalate
- Security vulnerabilities found
- Performance issues affecting production
- Architecture concerns
- Disagreements on approach

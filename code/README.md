# Test Code for Prompts

This folder contains sample COBOL and JCL files for testing the GitHub Copilot prompts.

**Note**: This folder is excluded from git commits (see `.gitignore`).

## Files

### COBOL Programs
- `PAYROLL.cbl` - Sample payroll calculation program
  - Features: File I/O, calculations, error handling
  - Use with: `/mf-document-code`, `/mf-analyze-code`, `/mf-explain-cobol`

### JCL Jobs
- `PAYROLL.jcl` - Sample payroll processing job stream
  - Features: Multiple steps, conditional processing, restart logic
  - Use with: `/mf-explain-jcl`

## Testing Prompts

### Test Document Code
```
/mf-document-code

[Paste content from PAYROLL.cbl]
```

### Test Analyze Code
```
/mf-analyze-code

[Paste content from PAYROLL.cbl]
```

### Test Explain COBOL
```
/mf-explain-cobol

[Paste content from PAYROLL.cbl]

Audience: Business Users
```

### Test Explain JCL
```
/mf-explain-jcl

[Paste content from PAYROLL.jcl]
```

## Adding Test Files

Feel free to add your own COBOL and JCL files here for testing. Just remember:
- Files in this folder are NOT committed to git
- Use for local testing only
- Keep examples realistic but simple

## Prompt Shortcuts Reference

| Shortcut | Purpose |
|----------|---------|
| `/mf-document-code` | Document COBOL programs |
| `/mf-analyze-code` | Analyze code quality |
| `/mf-explain-cobol` | Explain COBOL code |
| `/mf-explain-jcl` | Document JCL jobs |

See [`.github/prompts/README.md`](../.github/prompts/README.md) for full details.

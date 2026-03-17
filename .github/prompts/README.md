# GitHub Templates and Prompts

This folder contains comprehensive templates and prompts for COBOL mainframe development, documentation, and code review.

## 📁 Folder Structure

```
.github/
├── prompts/              # AI prompts for various tasks
│   ├── README.md
│   ├── document-code.md
│   ├── analyze-code.md
│   ├── explain-cobol.md
│   └── explain-jcl.md
├── TEMPLATES/            # Documentation templates
│   ├── design-document.md
│   └── code-review.md
├── instructions/         # Usage instructions (future)
└── agents/              # Agent configurations (future)
```

## 📝 Available Prompts

### Code Documentation

#### [`document-code.md`](prompts/document-code.md)
Generate comprehensive documentation for COBOL programs including:
- Program overview and structure
- File dependencies
- Data structures
- Processing logic
- Error handling
- Change history

**Use when**: Documenting new programs or updating existing program docs

#### [`explain-cobol.md`](prompts/explain-cobol.md)
Explain COBOL code in plain English for technical and non-technical audiences:
- Executive summary
- High-level flow
- Detailed walkthrough
- Business rules explained
- Common scenarios
- FAQ

**Use when**: 
- Onboarding new developers
- Explaining code to business stakeholders
- Creating training materials

### Code Analysis

#### [`analyze-code.md`](prompts/analyze-code.md)
Perform comprehensive static code analysis:
- Code quality metrics
- Best practices compliance
- Issues by priority
- Recommendations
- Modernization opportunities

**Use when**:
- Code quality assessments
- Technical debt evaluation
- Pre-refactoring analysis

### JCL Documentation

#### [`explain-jcl.md`](prompts/explain-jcl.md)
Explain and document JCL job streams:
- Job overview and flow
- Step-by-step explanation
- Dataset reference
- Schedule and dependencies
- Operations guide
- Restart procedures

**Use when**:
- Documenting batch jobs
- Creating operations runbooks
- Training operations staff

## 📋 Available Templates

### Design Documentation

#### [`design-document.md`](TEMPLATES/design-document.md)
Comprehensive design document template covering:
- Business requirements
- System overview
- Architecture design
- Detailed design
- Data design
- Interface design
- Error handling
- Security design
- Testing strategy
- Migration plan

**Use when**:
- New system development
- Major enhancements
- System modifications
- Compliance documentation

**Sections**: 12 major sections with subsections

### Code Review

#### [`code-review.md`](TEMPLATES/code-review.md)
Standardized code review template ensuring:
- Functionality verification
- Code quality assessment
- Performance review
- Security check
- Error handling validation
- Maintainability evaluation

**Use when**:
- Pull request reviews
- Code quality gates
- Pre-deployment checks

**Features**:
- Rating system (✅/⚠️/❌)
- Issue tracking by severity
- Action items
- Approval workflow

## 🚀 How to Use

### Using Prompts with AI Assistants

1. **Choose the right prompt** for your task
2. **Copy the prompt content**
3. **Paste into AI chat** (GitHub Copilot, ChatGPT, etc.)
4. **Provide the code** or context
5. **Review and refine** the output

**Example**:
```
1. Open prompts/explain-cobol.md
2. Copy the entire prompt
3. Paste into Copilot Chat
4. Add: "Here's the COBOL code to explain: [paste code]"
5. Review the explanation
```

### Using Templates

1. **Choose the appropriate template**
2. **Copy the template**
3. **Fill in the sections** relevant to your project
4. **Remove N/A sections** if not applicable
5. **Save in appropriate location** (docs/, wiki, etc.)

**Example for Design Doc**:
```
1. Copy TEMPLATES/design-document.md
2. Save as docs/design-DD-001.md
3. Fill in all applicable sections
4. Review with team
5. Get approval signatures
```

## 📖 Best Practices

### For Prompts

**Do**:
- ✅ Read the entire prompt before using
- ✅ Customize for your specific context
- ✅ Provide complete code/context to AI
- ✅ Review AI output for accuracy
- ✅ Iterate and refine as needed

**Don't**:
- ❌ Use prompts without understanding
- ❌ Accept AI output without review
- ❌ Use for security-sensitive code without safeguards
- ❌ Expect perfect results on first try

### For Templates

**Do**:
- ✅ Use templates consistently
- ✅ Fill in all required sections
- ✅ Keep documents up to date
- ✅ Get proper reviews and approvals
- ✅ Store in accessible location

**Don't**:
- ❌ Skip sections without reason
- ❌ Create documents and forget them
- ❌ Use templates as mere formalities
- ❌ Over-complicate simple changes

## 🎯 Use Cases

### Scenario 1: New Developer Onboarding
**Goal**: Help new developer understand legacy COBOL code

**Approach**:
1. Use `explain-cobol.md` prompt for key programs
2. Generate documentation with `document-code.md`
3. Create program overview documents
4. Build knowledge base gradually

**Outcome**: New developer productive faster, less tribal knowledge

### Scenario 2: Code Modernization Project
**Goal**: Assess and modernize legacy COBOL applications

**Approach**:
1. Use `analyze-code.md` for each program
2. Document current state with `document-code.md`
3. Create design doc with `design-document.md`
4. Use `code-review.md` for modernization reviews

**Outcome**: Clear modernization roadmap, documented decisions

### Scenario 3: Batch Job Documentation
**Goal**: Document critical batch jobs for operations

**Approach**:
1. Use `explain-jcl.md` for each job
2. Create operations runbook
3. Document restart procedures
4. Train operations team

**Outcome**: Reduced incidents, faster recovery

### Scenario 4: Compliance Documentation
**Goal**: Meet regulatory documentation requirements

**Approach**:
1. Use `design-document.md` for system design
2. Use `document-code.md` for programs
3. Use `code-review.md` for review evidence
4. Maintain change history

**Outcome**: Audit-ready documentation

## 🔄 Continuous Improvement

### Suggesting Improvements

Found a way to make these prompts/templates better?

1. **Test your improvement** with real code
2. **Create a pull request** with the change
3. **Explain the benefit** in the PR description
4. **Get team feedback**

### Version Control

These templates and prompts are version-controlled:
- Track changes over time
- See who made what changes
- Revert if needed
- Maintain consistency

## 📚 Additional Resources

### Related Documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) - Code of conduct
- [README.md](../README.md) - Project overview

### External Resources
- [COBOL Programming Standards](https://example.com/cobol-standards)
- [JCL Reference](https://example.com/jcl-reference)
- [Code Review Best Practices](https://example.com/code-review)

## ❓ FAQ

**Q: Can I use these with non-COBOL projects?**
A: Yes! Many prompts and templates can be adapted for other languages. Adjust the language-specific sections as needed.

**Q: How do I customize these for my team?**
A: Copy the files, modify to fit your needs, and maintain your own version. Consider contributing improvements back.

**Q: Are these suitable for beginners?**
A: Yes, the prompts are designed to work for various skill levels. The explanations generated can be adjusted based on the audience.

**Q: Can I automate using these templates?**
A: Absolutely! These can be integrated into CI/CD pipelines, documentation generators, or custom tools.

**Q: How often are these updated?**
A: As needed based on feedback and best practice evolution. Check the git history for recent changes.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- New prompt types
- Template improvements
- Additional use cases
- Bug fixes
- Examples and samples

## 📞 Support

For questions or issues:
1. Check this README
2. Review the specific prompt/template
3. Open an issue on GitHub
4. Ask in team channels

---

**Last Updated**: [Date]
**Maintained By**: [Team/Person]
**Version**: 1.0.0

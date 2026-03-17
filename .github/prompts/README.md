# GitHub Copilot Prompts for Mainframe Development

Quick access prompts for COBOL mainframe development tasks. Use with GitHub Copilot Chat using `/mf-[prompt-name]` shortcut.

## 🚀 Quick Start

### Using Prompts

1. **Open Copilot Chat** in VS Code (`Ctrl+Alt+I` / `Cmd+Alt+I`)
2. **Type shortcut**: `/mf-[prompt-name]`
3. **Paste your code** after the prompt
4. **Get instant results**

### Available Prompts

| Shortcut | Prompt | Purpose |
|----------|--------|---------|
| `/mf-document-code` | document-code.prompt.md | Document COBOL programs |
| `/mf-analyze-code` | analyze-code.prompt.md | Analyze code quality |
| `/mf-explain-cobol` | explain-cobol.prompt.md | Explain COBOL in plain English |
| `/mf-explain-jcl` | explain-jcl.prompt.md | Document JCL jobs |

## 📁 Structure

```
.github/
├── prompts/              # Quick prompts with shortcuts
│   ├── [name].prompt.md  # Use with /mf-[name]
│   └── README.md         # This file
├── instructions/         # Detailed instructions
│   ├── [name].instruction.md
│   └── README.md
└── templates/            # Reusable templates
    ├── [name].template.md
    └── README.md
```

## 📝 Prompt Examples

### Document COBOL Code
```
/mf-document-code

[Paste COBOL code here]
```

**Output**: Complete program documentation with structure, file dependencies, and processing logic.

### Analyze Code Quality
```
/mf-analyze-code

[Paste COBOL code here]
```

**Output**: Quality metrics, best practices compliance, issues by priority, recommendations.

### Explain to Business Users
```
/mf-explain-cobol

[Paste COBOL code here]

Audience: Business Users
```

**Output**: Business-friendly explanation with examples and analogies.

### Document JCL Job
```
/mf-explain-jcl

[Paste JCL code here]
```

**Output**: Job flow, step explanations, dataset reference, operations guide.

## 📚 Instructions

Detailed instructions for each prompt are in the [`instructions/`](../instructions/) folder:

- [Document Code Instructions](../instructions/document-code.instruction.md)
- [Analyze Code Instructions](../instructions/analyze-code.instruction.md)
- [Explain COBOL Instructions](../instructions/explain-cobol.instruction.md)
- [Explain JCL Instructions](../instructions/explain-jcl.instruction.md)
- [Design Document Instructions](../instructions/design-document.instruction.md)
- [Code Review Instructions](../instructions/review-code.instruction.md)

## 📋 Templates

Reusable templates in the [`templates/`](../templates/) folder:

- [Design Document Template](../templates/design-document.template.md)
- [Code Review Template](../templates/code-review.template.md)

## 🎯 Best Practices

### For Prompts
- ✅ Be specific about what you want
- ✅ Include complete code/context
- ✅ Specify audience if relevant
- ✅ Review and refine AI output

### For Instructions
- ✅ Read instructions first for context
- ✅ Follow steps systematically
- ✅ Use examples as guides
- ✅ Apply best practices

### For Templates
- ✅ Copy template before use
- ✅ Fill all applicable sections
- ✅ Remove N/A sections
- ✅ Get proper approvals

## 🔧 Customization

### Create Custom Prompts

1. Copy a prompt file
2. Modify for your needs
3. Use naming: `[name].prompt.md`
4. Shortcut will be `/mf-[name]`

### Add Custom Instructions

1. Create file in `instructions/`
2. Follow structure: Purpose, Steps, Examples, Best Practices
3. Reference from prompt files

## 📖 Additional Resources

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [README.md](../README.md) - Project overview
- [BACKENDS.md](../BACKENDS.md) - Backend comparison guide

## ❓ FAQ

**Q: How do I use these in VS Code?**  
A: Open Copilot Chat, type `/mf-` to see available prompts, select one, paste code.

**Q: Can I customize prompts?**  
A: Yes! Copy and modify in `.github/prompts/`.

**Q: Do these work with other AI tools?**  
A: Yes, copy prompt content and use with ChatGPT, Claude, etc.

**Q: How do I add a new prompt?**  
A: Create `[name].prompt.md` in `prompts/`, it will auto-have `/mf-[name]` shortcut.

---

**Last Updated**: 2026-03-16  
**Version**: 2.0.0 (Restructured for shortcuts)

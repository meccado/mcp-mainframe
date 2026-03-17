# COBOL Code Explanation Prompt

## Purpose
Explain COBOL code in clear, plain English for both technical and non-technical stakeholders.

## Instructions

When explaining COBOL code, use this structure:

### 1. Executive Summary
```markdown
## What This Program Does

**In One Sentence**: [Simple one-sentence description]

**Business Purpose**: 
[Explain the business value and purpose in 2-3 sentences]

**Example**: 
[Provide a concrete example of how this program is used]
```

### 2. High-Level Flow
```markdown
## How It Works (Simple View)

This program:
1. **[Step 1]** - [What it does in plain English]
2. **[Step 2]** - [What it does in plain English]
3. **[Step 3]** - [What it does in plain English]
4. **[Step 4]** - [What it does in plain English]

**Think of it like**: [Real-world analogy]
```

### 3. Detailed Explanation
```markdown
## Detailed Walkthrough

### Input Stage
**What comes in**: [Describe input files/data]
**Where from**: [Source systems or departments]
**Format**: [Record layout summary]

### Processing Stage
**Main Logic**:
- [Explain key calculations or transformations]
- [Explain business rules applied]
- [Explain any validations performed]

**Key Business Rules**:
1. [Rule 1] - [Why it exists, what it does]
2. [Rule 2] - [Why it exists, what it does]
3. [Rule 3] - [Why it exists, what it does]

### Output Stage
**What goes out**: [Describe output files/reports]
**Where to**: [Destination systems or departments]
**Format**: [Output format summary]
```

### 4. Code Section Explanations

For each major paragraph or section:

```markdown
### [Paragraph/Section Name]

**Purpose**: [What this section does]

**In Plain English**: 
[Explain in simple terms, avoiding technical jargon]

**Example**:
[Provide a concrete example with sample data]

**COBOL Code**:
```cobol
[Show relevant code snippet]
```

**Line-by-Line Explanation**:
- Line X: [What this line does]
- Line Y: [What this line does]
```

### 5. Data Explained
```markdown
## Key Data Elements

### Input Data
| Field Name | What It Is | Example | Business Meaning |
|------------|-----------|---------|------------------|
| CUST-ID | Customer identifier | 12345 | Unique customer number |
| TRANS-AMT | Transaction amount | 1500.00 | Dollar amount of transaction |

### Output Data
| Field Name | What It Is | Example | Business Meaning |
|------------|-----------|---------|------------------|
| ACCT-BAL | Account balance | 5000.00 | Current account balance |
| STATUS-CODE | Transaction status | 00 | Success indicator |
```

### 6. Business Rules Explained
```markdown
## Business Rules

### Rule: [Rule Name]

**What It Does**: 
[Plain English description]

**Why It Exists**: 
[Business reason for this rule]

**How It Works**:
[Step-by-step explanation]

**Example**:
```
Before: [Input scenario]
After: [Output result]
```

**COBOL Implementation**:
```cobol
[Show relevant code]
```
```

### 7. Common Scenarios
```markdown
## Common Scenarios

### Scenario 1: [Normal Processing]
**When**: [Conditions]
**What Happens**: [Step-by-step flow]
**Result**: [Expected outcome]

### Scenario 2: [Error Condition]
**When**: [Error conditions]
**What Happens**: [Error handling flow]
**Result**: [Error message/recovery]

### Scenario 3: [Edge Case]
**When**: [Special conditions]
**What Happens**: [Special processing]
**Result**: [Special handling outcome]
```

### 8. Questions & Answers
```markdown
## Frequently Asked Questions

**Q: [Common question]?**
A: [Clear, concise answer]

**Q: [Another common question]?**
A: [Clear, concise answer]

**Q: [Technical question]?**
A: [Answer in business terms]
```

## Writing Guidelines

### Do
- ✅ Use simple, clear language
- ✅ Provide concrete examples
- ✅ Explain business context
- ✅ Use analogies when helpful
- ✅ Define technical terms when first used
- ✅ Include visual descriptions where helpful

### Don't
- ❌ Use jargon without explanation
- ❌ Assume prior COBOL knowledge
- ❌ Skip business context
- ❌ Use abbreviations without defining them
- ❌ Focus only on technical details

## Audience Levels

### For Business Users
- Focus on business purpose and outcomes
- Minimize technical details
- Use business examples
- Explain impact on their work

### For Developers (Non-COBOL)
- Explain COBOL-specific concepts
- Compare to modern equivalents
- Show data flow clearly
- Include technical details with explanations

### For New COBOL Developers
- Explain COBOL idioms and patterns
- Show best practices
- Highlight common pitfalls
- Provide learning resources

## Example Output Structure

```markdown
# Program Explanation: PAYROLL

## Executive Summary
This program calculates employee weekly pay including overtime.

## Simple Flow
1. Reads employee time cards
2. Calculates regular and overtime hours
3. Applies pay rates and deductions
4. Produces pay stubs and updates records

## Detailed Explanation
[... detailed content ...]

## Business Rules
[... rules explained ...]

## Examples
[... sample scenarios ...]
```

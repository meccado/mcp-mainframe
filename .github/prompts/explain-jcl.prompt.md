# /mf-explain-jcl

**Purpose**: Explain and document JCL job streams.

**Usage**: Paste JCL code after this prompt.

**Output Structure**:
1. Job Overview (Name, Type, Business Purpose)
2. Job Flow (Diagram and description)
3. Step-by-Step Explanation (Each step detailed)
4. Dataset Reference (Input/Output tables)
5. Schedule & Dependencies (Timing, predecessors, successors)
6. Operations Guide (Monitor, issues, restart)
7. Complete JCL Listing (With annotations)

**Instructions**: See [JCL Instructions](../instructions/explain-jcl.instruction.md)

**Special Focus**: Conditional processing, return codes, restart procedures

**Example**:
```jcl
[Paste JCL code here]
```

**Output**: Complete job documentation for operations

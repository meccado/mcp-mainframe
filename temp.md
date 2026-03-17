Great question! You're right to wonder about a more native GitHub integration. The landscape has evolved significantly since we discussed the Continue.dev approach. Let me clarify your options:

## The Short Answer

**Yes, you can use GitHub Copilot directly with MCP without Continue.dev** – and you can configure it right inside your repository using `.github` folders. Here's how:

## Option 1: GitHub's Native Custom Agents (The `.github/agents` Approach)

GitHub recently introduced **Custom agents for GitHub Copilot** . This is exactly what you're asking about:

- You can define agent configurations in `.github/agents/` in any repository (or at the organization level in `{org}/.github/agents`)
- These agents can be tailored with prompts, tool selections, and **MCP server configurations** 
- They work across Copilot coding agent in github.com, the Copilot CLI, and will come to VS Code in a future release 

**For your mainframe COBOL context**, you could create a custom agent with your MCP server pre-configured. This is the most "GitHub-native" approach.

## Option 2: Direct MCP Configuration in VS Code (The `.vscode/mcp.json` Approach)

This is available *today* and works with your existing Copilot setup:

### Step-by-Step Implementation

1. **Create a `.vscode/mcp.json` file** in your repository:

```json
{
  "servers": {
    "mainframe-cobol": {
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/your/mcp-server.py"],
      "env": {
        "MF_HOST": "your.mainframe.com",
        "MF_USER": "youruserid",
        "MF_KEYFILE": "/path/to/private_key",
        "COBOL_SRC_DSN": "USER.COBOL.SRC"
      }
    }
  }
}
```

2. **Enable MCP in VS Code settings**:
   - Add `"chat.mcp.enabled": true` to your `settings.json` 

3. **Use Copilot in Agent Mode**:
   - Open Copilot Chat
   - Select **Agent mode** from the dropdown
   - Click the **Tools** button – your MCP tools should appear
   - Ask questions like "Show me the source for program PAYROLL" 

### Alternative: SSE/HTTP Transport

If you prefer to run your MCP server remotely (e.g., on a server accessible to your team):

```json
{
  "servers": {
    "mainframe-cobol": {
      "type": "sse",
      "url": "https://your-mcp-server.example.com/mcp"
    }
  }
}
```

## Option 3: GitHub Workspace/Organization Level Configuration

For team-wide access, you can configure MCP servers at the workspace level in VS Code, or use GitHub's organization-level agent configurations in `.github-private` repositories .

## Important Considerations

### What Works vs. What's Coming

| Approach | Availability | Configuration Location |
|----------|--------------|------------------------|
| `.vscode/mcp.json` | Available now | Your local repo |
| Copilot Agent Mode with MCP | Available now | Via VS Code UI + config |
| `.github/agents/` with MCP | Announced Oct 2025 | Repository/organization level |
| Organization-wide agents | Announced | `{org}/.github-private/agents` |

### Security Notes

- Copilot shows a security confirmation when first invoking MCP tools 
- For production, consider authentication (Microsoft Entra ID for Azure-hosted MCP servers) 
- MCP servers run with the permissions of the user executing them 

## Recommendation for Your Scenario

**Use Option 2 (`.vscode/mcp.json`) today**. Here's why:

1. **Immediate availability** – works with your current VS Code + Copilot
2. **Your existing MCP server is reusable** – the server code we discussed earlier works unchanged
3. **Version control friendly** – commit `.vscode/mcp.json` to your repo so your team shares the config
4. **No additional extensions** – pure VS Code + Copilot

Once GitHub's custom agents mature and gain VS Code support, you can migrate your configuration to `.github/agents/` for organization-wide distribution.

## Example: Your Complete VS Code Setup

```
your-cobol-repo/
├── .vscode/
│   └── mcp.json           # MCP server configuration
├── mcp-server/
│   └── mainframe-mcp.py   # Your Python MCP server
├── .github/
│   └── copilot-instructions.md  # Optional: global instructions
└── ... (your COBOL files)
```

The MCP server code you wrote earlier remains exactly the same – only the integration method changes from Continue.dev to native VS Code/Copilot.

Would you like me to help you adapt your existing MCP server code for this native integration?
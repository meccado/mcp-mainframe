# VS Code MCP Configuration

This folder contains MCP server configurations for the MCP COBOL Server with support for **four backends**.

## Files

- **`mcp.json`**: SSH backend configuration (default)
- **`mcp.endevor.json`**: Endevor backend configuration
- **`mcp.zosmf.json`**: z/OSMF backend configuration (Recommended)
- **`mcp.zowe.json`**: Zowe backend configuration (Recommended for Modern DevOps)

## Quick Start

### 1. Enable MCP in VS Code

- Open Settings (`Ctrl+,` or `Cmd+,`)
- Search for `chat.mcp.enabled`
- Enable it: `"chat.mcp.enabled": true`

### 2. Choose Your Backend

**For SSH** (default):
```bash
# Already configured in mcp.json
# Just update the values with your credentials
```

**For Endevor**:
```bash
cp .vscode/mcp.endevor.json .vscode/mcp.json
# Edit .vscode/mcp.json with your Endevor credentials
```

**For z/OSMF** (Recommended):
```bash
cp .vscode/mcp.zosmf.json .vscode/mcp.json
# Edit .vscode/mcp.json with your z/OSMF credentials
```

**For Zowe** (Modern DevOps):
```bash
cp .vscode/mcp.zowe.json .vscode/mcp.json
# Edit .vscode/mcp.json with your Zowe credentials
```

### 3. Configure Credentials

Edit `.vscode/mcp.json` and replace placeholder values:

**SSH Backend**:
```json
{
  "BACKEND": "SSH",
  "MF_HOST": "zos.yourcompany.com",
  "MF_USER": "YOURUSERID",
  "MF_KEYFILE": "/path/to/your/ssh/key",
  "COBOL_SRC_DSN": "YOUR.COBOL.SRC",
  "COPYBOOK_DSN": "YOUR.COPYBOOK"
}
```

**z/OSMF Backend**:
```json
{
  "BACKEND": "ZOSMF",
  "ZOSMF_BASE_URL": "https://zosmf.yourcompany.com:10443",
  "ZOSMF_USER": "YOURUSERID",
  "ZOSMF_PASSWORD": "${env:ZOSMF_PASSWORD}",
  "COBOL_SRC_DSN": "YOUR.COBOL.SRC",
  "COPYBOOK_DSN": "YOUR.COPYBOOK",
  "ZOSMF_VERIFY_CERT": "true"
}
```

**Zowe Backend**:
```json
{
  "BACKEND": "ZOWE",
  "ZOWE_BASE_URL": "https://zowe.yourcompany.com:10010",
  "ZOWE_USER": "YOURUSERID",
  "ZOWE_PASSWORD": "${env:ZOWE_PASSWORD}",
  "COBOL_SRC_DSN": "YOUR.COBOL.SRC",
  "COPYBOOK_DSN": "YOUR.COPYBOOK",
  "ZOWE_VERIFY_CERT": "true"
}
```

### 4. Using with Copilot

1. **Open Copilot Chat** (`Ctrl+Alt+I` or `Cmd+Alt+I`)
2. **Select Agent Mode** from the dropdown
3. **Click the Tools button** (🔧) - your MCP tools should appear:
   - `get_cobol_source` - Retrieve COBOL program source
   - `get_copybook` - Retrieve copybook source
4. **Ask questions** like:
   - "Show me the source for program PAYROLL"
   - "Get the CUST-REC copybook and explain the fields"
   - "List available resources"

## Backend Selection Guide

| Backend | Best For | Setup Complexity |
|---------|----------|------------------|
| **SSH** | Development, quick setup | Low |
| **Endevor** | Enterprise with Endevor | Medium |
| **z/OSMF** | Production (IBM shops) | Medium |
| **Zowe** | Modern DevOps | Medium |

**Recommendation**: 
- **Development**: SSH (if USS available) or z/OSMF
- **Production**: z/OSMF (native IBM) or Zowe (open source)

See [BACKENDS.md](../BACKENDS.md) for detailed comparison.

## Using Environment Variables

For better security, use environment variables for sensitive data:

**Windows (PowerShell)**:
```powershell
$env:ZOSMF_PASSWORD = "your_password"
$env:ZOWE_PASSWORD = "your_password"
```

**macOS/Linux**:
```bash
export ZOSMF_PASSWORD="your_password"
export ZOWE_PASSWORD="your_password"
```

Then reference in `mcp.json`:
```json
"ZOSMF_PASSWORD": "${env:ZOSMF_PASSWORD}"
```

## Troubleshooting

### Tools Don't Appear in Copilot

1. Check MCP is enabled: `"chat.mcp.enabled": true`
2. Check Output panel → "MCP Server" logs
3. Verify `.vscode/mcp.json` syntax is valid JSON
4. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"

### Connection Errors

**SSH**:
- Verify SSH key exists and has correct permissions (`chmod 600`)
- Test SSH: `ssh -i /path/to/key USER@HOST`

**z/OSMF/Zowe**:
- Verify URL is correct (include port number)
- Check credentials
- For development with self-signed certs: set `ZOSMF_VERIFY_CERT` or `ZOWE_VERIFY_CERT` to `"false"`

### Backend Not Working

1. Check backend name is correct: `SSH`, `ENDEVOR`, `ZOSMF`, or `ZOWE`
2. Verify all required environment variables for your backend
3. Check logs in Output panel → "MCP Server"

## Advanced Configuration

### Custom Log Level

```json
"LOG_LEVEL": "DEBUG"  // Options: DEBUG, INFO, WARNING, ERROR
```

### Connection Pool Size (SSH only)

```json
"MAX_CONNECTIONS": "15"  // Range: 1-20
```

### Timeout Settings

```json
"CONNECTION_TIMEOUT": "60"  // Seconds
```

### Frequently Accessed Programs

```json
"FREQUENT_PROGRAMS": "PAYROLL,BILLING,CUSTUPD,INVOICE"
"FREQUENT_COPYBOOKS": "CUST-REC,ORDER-REC,COMMON1,DATEFLDS"
```

## Resources

- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/mcp-servers)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Backend Comparison Guide](../BACKENDS.md)
- [z/OSMF REST API](https://www.ibm.com/docs/en/zos/2.5.0?topic=services-zosmf-rest-apis)
- [Zowe Documentation](https://docs.zowe.org/)

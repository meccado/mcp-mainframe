# Quickstart Guide: MCP COBOL Server

**Created**: 2026-03-16
**Branch**: `001-mcp-cobol-server`

Get up and running with the MCP COBOL Server in 5 minutes.

---

## Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.10+** installed on your workstation
- ✅ **SSH access** to a z/OS mainframe with USS (UNIX System Services)
- ✅ **Read permissions** on COBOL source and copybook datasets
- ✅ **VS Code** with **Continue.dev** extension installed
- ✅ **SSH key pair** for mainframe authentication (password auth not supported)

---

## Step 1: Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd mcp-mainframe

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment Variables

Create a `.env` file in the project root (or set system environment variables):

```bash
# Mainframe connection
MF_HOST=zos.yourcompany.com
MF_USER=YOURUSERID
MF_KEYFILE=/home/youruser/.ssh/id_rsa

# Dataset names (adjust to your mainframe)
COBOL_SRC_DSN=YOUR.COBOL.SRC
COPYBOOK_DSN=YOUR.COPYBOOK

# Optional: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Optional: Maximum concurrent SSH connections (default: 10)
MAX_CONNECTIONS=10
```

**Important**: 
- `MF_KEYFILE` must point to your private SSH key (not the `.pub` file)
- SSH key should have permissions `600` (read/write for owner only)
- Never commit `.env` file to version control (it's in `.gitignore`)

---

## Step 3: Test the Server Manually

Before integrating with Continue.dev, test the server standalone:

```bash
# Run the server (it will wait for MCP connection)
python src/mcp_server/server.py
```

If configuration is valid, you should see:
```
INFO: MCP COBOL Server starting...
INFO: Configuration validated successfully
INFO: Waiting for MCP connection...
```

If there's an error, you'll see a clear message like:
```
ERROR: Configuration error: Required environment variable 'MF_HOST' is not set.
```

Press `Ctrl+C` to exit the server.

---

## Step 4: Configure Continue.dev

Add the MCP server to your Continue configuration:

**File**: `~/.continue/config.json` (create if it doesn't exist)

```json
{
  "experimental": {
    "mcpServers": {
      "mainframe": {
        "command": "python",
        "args": ["/absolute/path/to/mcp-mainframe/src/mcp_server/server.py"],
        "env": {
          "MF_HOST": "zos.yourcompany.com",
          "MF_USER": "YOURUSERID",
          "MF_KEYFILE": "/home/youruser/.ssh/id_rsa",
          "COBOL_SRC_DSN": "YOUR.COBOL.SRC",
          "COPYBOOK_DSN": "YOUR.COPYBOOK",
          "LOG_LEVEL": "INFO"
        }
      }
    }
  }
}
```

**Important**:
- Use **absolute paths** for `args[0]` (Continue.dev needs full path)
- Environment variables in config override system variables
- Restart VS Code after changing config

---

## Step 5: Verify Integration

After restarting VS Code:

1. **Open Continue.dev** (usually `Ctrl+L` or `Cmd+L`)
2. **Ask a test question**: "What tools are available?"
3. **Expected response**: Continue should list `get_cobol_source` and `get_copybook`

If tools don't appear:
- Check Continue.dev console for errors
- Verify the path to `server.py` is correct
- Ensure environment variables are set correctly

---

## Step 6: Use the Tools

### Example 1: Retrieve COBOL Source

**Ask Continue**:
```
Using get_cobol_source, show me the source for program PAYROLL
```

**Expected Output**:
```
Here's the COBOL source for program PAYROLL:

       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAYROLL.
       ...
```

### Example 2: Retrieve Copybook

**Ask Continue**:
```
Get the CUST-REC copybook and explain the fields
```

**Expected Output**:
```
Here's the CUST-REC copybook:

       01  CUSTOMER-RECORD.
           05  CUST-ID              PIC X(10).
           ...

This copybook defines a customer record with the following fields:
- CUST-ID: Customer identifier (10 characters)
- ...
```

### Example 3: Analyze Program Logic

**Ask Continue**:
```
Using get_cobol_source, retrieve the BILLING program and explain what it does
```

**Expected Output**:
```
I've retrieved the BILLING program. Here's what it does:

1. Initializes billing variables...
2. Reads customer accounts...
3. Calculates charges...
```

---

## Troubleshooting

### "Configuration error: Required environment variable is not set"

**Solution**: Ensure all 5 required variables are set:
- `MF_HOST`
- `MF_USER`
- `MF_KEYFILE`
- `COBOL_SRC_DSN`
- `COPYBOOK_DSN`

### "Authentication failed"

**Possible causes**:
- SSH key file path is incorrect
- SSH key permissions are too open (should be `600`)
- Mainframe user ID is incorrect
- SSH key is not authorized on mainframe

**Solution**:
```bash
# Check key permissions
ls -l ~/.ssh/id_rsa
# Should show: -rw------- (600)

# Fix permissions if needed
chmod 600 ~/.ssh/id_rsa

# Test SSH connection manually
ssh -i ~/.ssh/id_rsa YOURUSERID@zos.yourcompany.com
```

### "Program not found"

**Possible causes**:
- Program name is misspelled
- Program doesn't exist in the configured dataset
- Dataset name (`COBOL_SRC_DSN`) is incorrect

**Solution**:
- Verify program name with your mainframe team
- Check that `COBOL_SRC_DSN` points to the correct dataset
- Try a different known program name

### "Unable to connect to mainframe"

**Possible causes**:
- Network connectivity issue
- Mainframe is down
- Firewall blocking SSH (port 22)
- Incorrect hostname

**Solution**:
```bash
# Test network connectivity
ping zos.yourcompany.com

# Test SSH port
telnet zos.yourcompany.com 22
# Or use nc (netcat)
nc -zv zos.yourcompany.com 22
```

### "Server is busy"

**Cause**: Maximum concurrent connection limit reached (default: 10)

**Solution**:
- Wait a few seconds and try again
- Increase `MAX_CONNECTIONS` if needed (not recommended without mainframe team approval)

### Tools don't appear in Continue.dev

**Solution**:
1. Check Continue.dev console for errors
2. Verify `config.json` syntax is valid JSON
3. Ensure absolute path to `server.py` is correct
4. Restart VS Code completely
5. Test server manually (Step 3) to verify configuration

---

## Next Steps

Now that you're up and running:

- **Explore**: Try retrieving different programs and copybooks
- **Analyze**: Ask Continue to explain program logic, find bugs, suggest improvements
- **Navigate**: Use retrieved source as context for larger refactoring tasks
- **Extend**: See the documentation for adding new tools (e.g., `get_jcl`, `list_programs`)

---

## Resources

- **Full Documentation**: See other files in `specs/001-mcp-cobol-server/`
- **MCP Specification**: https://modelcontextprotocol.io/
- **Continue.dev Docs**: https://docs.continue.dev/
- **Support**: Contact your mainframe team for dataset access issues

---

## Quick Reference

### Environment Variables

| Variable | Required | Example |
|----------|----------|---------|
| `MF_HOST` | Yes | `zos.company.com` |
| `MF_USER` | Yes | `MYUSERID` |
| `MF_KEYFILE` | Yes | `/home/user/.ssh/id_rsa` |
| `COBOL_SRC_DSN` | Yes | `USER.COBOL.SRC` |
| `COPYBOOK_DSN` | Yes | `USER.COPYBOOK` |
| `LOG_LEVEL` | No | `INFO` |
| `MAX_CONNECTIONS` | No | `10` |

### Tool Names

- `get_cobol_source(program: string)` - Retrieve COBOL program
- `get_copybook(copybook: string)` - Retrieve copybook

### Performance Targets

- Response time: <5 seconds (typical)
- Concurrent requests: Up to 10
- Startup time: <2 seconds

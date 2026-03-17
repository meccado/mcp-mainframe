# Mainframe Backend Comparison Guide

This guide helps you choose the right backend for connecting the MCP COBOL Server to your mainframe.

## Quick Decision Matrix

| If you have... | Use this backend |
|----------------|------------------|
| SSH access to USS filesystem | **SSH** (simplest) |
| CA Endevor for change management | **Endevor** |
| IBM z/OSMF installed | **z/OSMF** (recommended) |
| Zowe API ML installed | **Zowe** (modern, vendor-neutral) |
| Nothing installed | Install **z/OSMF** or **Zowe** |

## Backend Details

### 1. SSH Backend

**What**: Direct SSH connection to mainframe USS (UNIX System Services) filesystem

**Requirements**:
- SSH server enabled on z/OS
- USS filesystem access
- Read permissions on PDS datasets

**Pros**:
- ✅ Simple to set up
- ✅ No additional software needed
- ✅ Direct filesystem access
- ✅ Fast performance

**Cons**:
- ❌ Requires USS expertise
- ❌ No integration with change management
- ❌ Limited to USS-accessible datasets

**Configuration**:
```bash
BACKEND=SSH
MF_HOST=zos.yourcompany.com
MF_USER=YOURUSERID
MF_KEYFILE=/path/to/ssh/key
COBOL_SRC_DSN=USER.COBOL.SRC
COPYBOOK_DSN=USER.COPYBOOK
```

**Best For**: Small teams, development environments, quick setup

---

### 2. Endevor Backend

**What**: CA Endevor REST API for source code management

**Requirements**:
- CA Endevor installed on mainframe
- Endevor web services configured
- Endevor user credentials

**Pros**:
- ✅ Integrates with change management
- ✅ Tracks source code versions
- ✅ Enterprise-grade security
- ✅ Audit trail

**Cons**:
- ❌ Requires Broadcom licensing
- ❌ More complex setup
- ❌ Vendor lock-in

**Configuration**:
```bash
BACKEND=ENDEVOR
ENDEVOR_BASE_URL=https://endevor.yourcompany.com/api/v1
ENDEVOR_USER=YOURUSERID
ENDEVOR_PASSWORD=your_token
ENDEVOR_STAGE=PROD
```

**Best For**: Enterprises already using Endevor for change management

---

### 3. z/OSMF Backend (Recommended)

**What**: IBM z/OS Management Facility REST APIs (native IBM)

**Requirements**:
- z/OSMF installed on z/OS (standard on modern z/OS)
- z/OSMF user credentials
- RACF permissions for dataset access

**Pros**:
- ✅ Native IBM solution (no additional software)
- ✅ Comprehensive REST API
- ✅ Good security with RACF integration
- ✅ Well-documented
- ✅ Future-proof (IBM investment)

**Cons**:
- ❌ Requires z/OSMF setup (if not already installed)
- ❌ Certificate management for production

**Configuration**:
```bash
BACKEND=ZOSMF
ZOSMF_BASE_URL=https://zosmf.yourcompany.com:10443
ZOSMF_USER=YOURUSERID
ZOSMF_PASSWORD=your_password
COBOL_SRC_DSN=USER.COBOL.SRC
COPYBOOK_DSN=USER.COPYBOOK
ZOSMF_VERIFY_CERT=true  # false for dev with self-signed certs
```

**Best For**: Most enterprises - **RECOMMENDED** for production use

**API Reference**: [IBM z/OSMF REST API Guide](https://www.ibm.com/docs/en/zos/2.5.0?topic=services-zosmf-rest-apis)

---

### 4. Zowe Backend (Recommended for Modern DevOps)

**What**: Zowe API Mediation Layer (open source, vendor-neutral)

**Requirements**:
- Zowe installed on mainframe
- Zowe API ML configured
- Zowe user credentials

**Pros**:
- ✅ Open source (Open Mainframe Project)
- ✅ Vendor-neutral
- ✅ Modern REST API with OpenAPI spec
- ✅ Active community and ecosystem
- ✅ Integrates with modern DevOps tools
- ✅ JWT token authentication

**Cons**:
- ❌ Requires Zowe installation
- ❌ Additional infrastructure

**Configuration**:
```bash
BACKEND=ZOWE
ZOWE_BASE_URL=https://zowe.yourcompany.com:10010
ZOWE_USER=YOURUSERID
ZOWE_PASSWORD=your_password
COBOL_SRC_DSN=USER.COBOL.SRC
COPYBOOK_DSN=USER.COPYBOOK
ZOWE_VERIFY_CERT=true
```

**Best For**: Modern DevOps environments, teams embracing open source

**Documentation**: [Zowe Docs](https://docs.zowe.org/)

---

## Backend Comparison Table

| Feature | SSH | Endevor | z/OSMF | Zowe |
|---------|-----|---------|--------|------|
| **Setup Complexity** | Low | Medium | Medium | Medium |
| **Additional Software** | No | Yes (Broadcom) | No (IBM native) | Yes (Open Source) |
| **Cost** | Free | Licensed | Free (with z/OS) | Free (Open Source) |
| **Change Management** | No | ✅ Yes | ❌ No | ❌ No |
| **Vendor** | N/A | Broadcom | IBM | Open Mainframe Project |
| **API Type** | SSH/Unix | REST | REST | REST + JWT |
| **Security** | SSH keys | Endevor auth | RACF | RACF + JWT |
| **Best Use Case** | Dev/Quick setup | Enterprise with Endevor | Production (IBM shops) | Modern DevOps |

---

## Migration Between Backends

You can easily switch between backends by changing environment variables:

```bash
# From SSH to z/OSMF
export BACKEND=ZOSMF
export ZOSMF_BASE_URL=https://zosmf.yourcompany.com:10443
export ZOSMF_USER=YOURUSERID
export ZOSMF_PASSWORD=your_password
# Keep the same dataset names
export COBOL_SRC_DSN=USER.COBOL.SRC
export COPYBOOK_DSN=USER.COPYBOOK
```

The MCP tools (`get_cobol_source`, `get_copybook`) work identically regardless of backend!

---

## Performance Comparison

| Backend | Typical Latency | Concurrent Requests | Notes |
|---------|----------------|---------------------|-------|
| SSH | <1s | 5-10 (configurable) | Fastest for single requests |
| Endevor | 1-3s | 10-20 | Slower due to change mgmt overhead |
| z/OSMF | <1s | 10-20 | Excellent performance |
| Zowe | <1s | 20-50 | Best scalability with JWT |

---

## Security Considerations

### SSH Backend
- Use SSH key authentication (no passwords)
- Protect private keys with `chmod 600`
- Use bastion hosts for production access

### Endevor Backend
- Use access tokens instead of passwords
- Rotate credentials regularly
- Integrate with corporate SSO if available

### z/OSMF Backend
- Use HTTPS with valid certificates
- Configure RACF permissions properly
- Consider certificate pinning for production

### Zowe Backend
- Use JWT tokens for authentication
- Configure token expiration appropriately
- Use HTTPS with valid certificates
- Integrate with corporate identity provider

---

## Troubleshooting

### Connection Issues

**SSH**:
```bash
# Test SSH connectivity
ssh -i /path/to/key USER@HOST
```

**z/OSMF/Zowe**:
```bash
# Test REST API
curl -u USER:PASS https://host:port/zosmf/info
```

### Permission Denied

- Check RACF permissions for dataset access
- Verify user has READ access to PDS/PDSE
- For z/OSMF/Zowe, check API ML gateway permissions

### Certificate Errors (Development)

For development with self-signed certificates:
```bash
# z/OSMF
ZOSMF_VERIFY_CERT=false

# Zowe
ZOWE_VERIFY_CERT=false
```

**⚠️ Never use in production!**

---

## Recommendation Summary

**For Development**: SSH (quick setup) or z/OSMF (if available)

**For Production**: 
- **IBM shops**: z/OSMF (native, well-supported)
- **Modern DevOps**: Zowe (open source, scalable)
- **Endevor users**: Endevor (if already invested)

**For Enterprise**: z/OSMF or Zowe (both excellent choices)

---

## Getting Help

- **z/OSMF**: [IBM Documentation](https://www.ibm.com/docs/en/zos/2.5.0?topic=services-zosmf-rest-apis)
- **Zowe**: [Zowe Documentation](https://docs.zowe.org/)
- **Endevor**: [Broadcom TechDocs](https://techdocs.broadcom.com/)
- **SSH**: [IBM USS Guide](https://www.ibm.com/docs/en/zos)

---

**Questions?** Open an issue on GitHub or consult your mainframe team.

# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a reported vulnerability, what to expect if the vulnerability is accepted or declined, etc.

**Important**: For security issues, please do NOT open a public issue on GitHub.

Instead, please report security vulnerabilities via:

1. **GitHub Private Vulnerability Reporting**: Use the "Report a vulnerability" button in the Security tab
2. **Email**: security@example.com (replace with actual security contact)

### What to Include

Please include the following information in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)
- Your contact information for follow-up

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Resolution**: Depends on severity and complexity

### Security Best Practices

When using the MCP COBOL Server:

1. **Never commit credentials**: Use environment variables or Docker secrets
2. **Use SSH key authentication**: Never use passwords for mainframe access
3. **Restrict SSH key permissions**: Use `chmod 600` for private keys
4. **Keep dependencies updated**: Regularly run `pip install --upgrade -r requirements.txt`
5. **Use Docker in production**: Leverage container isolation and security features
6. **Monitor logs**: Watch for unusual access patterns or errors
7. **Limit network exposure**: Only expose necessary ports

### Security Features

The MCP COBOL Server includes these security features:

- ✅ SSH key-based authentication only
- ✅ No credential logging
- ✅ Read-only mainframe access
- ✅ Non-root Docker container user
- ✅ Environment variable configuration
- ✅ Input validation for program/copybook names

Thank you for helping keep the MCP COBOL Server secure!

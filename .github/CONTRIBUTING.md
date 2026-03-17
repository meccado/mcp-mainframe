# Contributing to MCP COBOL Server

First off, thank you for considering contributing to MCP COBOL Server! It's people like you that make MCP COBOL Server such a great tool for mainframe development.

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for MCP COBOL Server. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report**

* Check the [documentation](README.md) for answers
* Check the [Issues](https://github.com/meccado/mcp-mainframe/issues) to see if the problem has already been reported
* If it's a security issue, please read our [Security Policy](SECURITY.md)

**How Do I Submit A (Good) Bug Report?**

Bugs are tracked as [GitHub issues](https://github.com/meccado/mcp-mainframe/issues). Create an issue and provide the following information:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed and what behavior you expected
* Include screenshots or animated GIFs if possible
* Include logs from the MCP server
* Note if the issue occurs with SSH backend, Endevor backend, or both

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for MCP COBOL Server, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion**

* Check if the enhancement is already implemented in the [latest version](https://github.com/meccado/mcp-mainframe/releases/latest)
* Check if the enhancement has already been suggested
* Think about whether the enhancement aligns with the project's goals

**How Do I Submit A (Good) Enhancement Suggestion?**

Enhancement suggestions are tracked as [GitHub issues](https://github.com/meccado/mcp-mainframe/issues). Create an issue and provide:

* Use a clear and descriptive title
* Provide a detailed description of the suggested enhancement
* Explain why this enhancement would be useful
* List some examples of how this enhancement would be used
* Note which backend (SSH/Endevor) this applies to

### Pull Requests

The process described here has several goals:

* Maintain MCP COBOL Server's quality
* Fix problems that are important to users
* Engage the community in working toward the best possible MCP COBOL Server
* Enable a sustainable system for MCP COBOL Server's maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in [the template](PULL_REQUEST_TEMPLATE.md)
2. Follow the [styleguides](#styleguides)
3. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing

### Local Development

To develop locally:

```bash
# Clone the repository
git clone https://github.com/meccado/mcp-mainframe.git
cd mcp-mainframe

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov ruff black mypy

# Run tests
pytest

# Run linters
ruff check src/
black --check src/
```

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🐛 `:bug:` when fixing a bug
    * ✨ `:sparkles:` when adding new features
    * 📝 `:memo:` when writing docs
    * 🚀 `:rocket:` when improving performance
    * ✅ `:white_check_mark:` when adding tests
    * 🔒 `:lock:` when dealing with security

### Python Styleguide

* Follow [PEP 8](https://pep8.org/) for Python code style
* Use [Black](https://github.com/psf/black) for formatting
* Use [isort](https://pycqa.github.io/isort/) for import sorting
* Use type hints where possible
* Write docstrings for all public functions and classes

```python
def get_cobol_source(program: str) -> str:
    """
    Retrieve COBOL program source from mainframe.
    
    Args:
        program: The COBOL program name (1-8 alphanumeric characters)
        
    Returns:
        COBOL source code as plain text
        
    Raises:
        ValueError: If program name is invalid
        FileNotFoundError: If program not found
    """
    pass
```

### Documentation Styleguide

* Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
* Reference methods and classes with markdown: `ClassName.method_name()`
* Use code blocks for examples
* Keep documentation up to date with code changes

## Additional Notes

### Issues and Labels

This project uses the following labels:

* 🐛 `bug` - Something isn't working
* ✨ `enhancement` - New feature or request
* 📚 `documentation` - Improvements or additions to documentation
* 🧪 `tests` - Adding or updating tests
* 🔧 `maintenance` - Maintenance tasks
* 🚀 `performance` - Performance improvements
* 🔒 `security` - Security issues or improvements
* 👋 `good first issue` - Good for newcomers
* 🤔 `help wanted` - Extra attention is needed

### Docker Development

When developing with Docker:

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up -d --build

# Run tests in container
docker-compose exec mcp-cobol-server pytest
```

### MCP Server Testing

When testing the MCP server:

1. **Unit Tests**: Run `pytest tests/unit/`
2. **Integration Tests**: Run `pytest tests/integration/` (requires mainframe connection)
3. **Manual Testing**: Use VS Code with MCP enabled

Thank you for contributing to MCP COBOL Server! 🎉

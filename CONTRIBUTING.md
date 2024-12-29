# Contributing to Markdown to JSON Database Converter

Thank you for your interest in contributing to our project! This document provides guidelines and instructions for contributing.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Pull Request Process](#pull-request-process)
5. [Coding Standards](#coding-standards)
6. [Documentation](#documentation)
7. [Testing](#testing)
8. [Security](#security)

## Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Git

### Setup Development Environment
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/markdown-to-json-db.git
   cd markdown-to-json-db
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Process

### Branching Strategy
- `main`: Production-ready code
- `develop`: Development branch
- Feature branches: `feature/your-feature-name`
- Bug fix branches: `fix/bug-description`
- Release branches: `release/version-number`

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

Example:
```
feat(validator): add schema validation for nested sections

- Added recursive validation for nested sections
- Improved error messages for schema violations
- Updated tests to cover new validation logic

Closes #123
```

## Pull Request Process

1. Update documentation to reflect changes
2. Add/update tests as needed
3. Ensure all tests pass
4. Update the README.md if needed
5. Create a pull request with:
   - Clear description of changes
   - Link to related issue(s)
   - Screenshots/examples if applicable

### PR Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] CI/CD checks passing

## Coding Standards

### Python Style Guide
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints (PEP 484)
- Maximum line length: 88 characters
- Use docstrings following Google style

### Example
```python
from typing import Dict, Any, Optional

def validate_section(data: Dict[str, Any]) -> Optional[str]:
    """Validate a document section.

    Args:
        data: Dictionary containing section data.

    Returns:
        Optional error message, None if valid.

    Example:
        >>> result = validate_section({"title": "Test", "level": 1})
        >>> print(result)
        None
    """
    if not isinstance(data.get("title"), str):
        return "Title must be a string"
    return None
```

## Documentation

### Requirements
- All modules must have docstrings
- All public functions/methods must have docstrings
- Include examples in docstrings
- Keep diagrams up to date
- Document breaking changes

### Example
```python
"""
Module for document validation.

This module provides validation functionality for markdown documents,
ensuring proper structure and content.

Example:
    >>> validator = DocumentValidator()
    >>> result = validator.validate(document)
    >>> print(result.is_valid)
    True
"""
```

## Testing

### Requirements
- Write unit tests for new code
- Update existing tests for changes
- Maintain 80%+ code coverage
- Include integration tests for features

### Running Tests
```bash
# Unit tests
python -m pytest tests/

# With coverage
python -m pytest --cov=markdown_converter tests/

# Integration tests
python run_tests.py
```

## Security

### Guidelines
- Never commit sensitive data
- Use environment variables for configuration
- Validate all input data
- Follow secure coding practices
- Report security issues privately

### Reporting Security Issues
Email security issues to: security@stride.ae

## Questions?
Feel free to reach out to the maintainers:
- Tariq Ahmed (t.ahmed@stride.ae)

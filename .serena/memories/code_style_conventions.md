# Code Style and Conventions

## Python Style Guidelines
- **Line Length**: 100 characters (black configuration)
- **Type Hints**: Mandatory (mypy strict mode enabled)
- **Import Sorting**: isort with specific sections order
- **Code Formatting**: black for consistent formatting
- **Linting**: ruff for error detection and style enforcement

## Architecture Patterns
- **Clean Architecture**: Domain-driven design with hexagonal architecture
- **SOLID Principles**: Enforced throughout codebase
- **Dependency Injection**: Used for external dependencies
- **Port & Adapter Pattern**: Clear separation between domain and infrastructure

## Naming Conventions
- **Files**: snake_case for Python files
- **Classes**: PascalCase
- **Functions/Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Private members**: Leading underscore

## Testing Standards
- **Framework**: pytest with pytest-cov for coverage
- **Test Structure**: Arrange-Act-Assert pattern
- **Mocking**: pytest-mock for external dependencies
- **Coverage**: Minimum 20% (configured in pyproject.toml)

## Documentation
- **Docstrings**: Required for public methods and classes
- **Type Annotations**: Mandatory for all function signatures
- **README**: Maintained with usage instructions

## Git Workflow
- **Pre-commit hooks**: Automatic code quality checks
- **Branch protection**: Main branch requires passing tests
- **Commit messages**: Descriptive and clear

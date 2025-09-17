# Task Completion Checklist

## Code Quality Gates (Required before completion)
1. **Run all quality checks**: `make all` (includes black, isort, lint, mypy)
2. **Run tests**: `make test` - ensure all tests pass with adequate coverage
3. **Type checking**: `make mypy` - no type errors allowed
4. **Pre-commit validation**: All hooks must pass

## Testing Requirements
- Write tests for new functionality (TDD approach preferred)
- Maintain or improve test coverage (minimum 20%)
- Verify integration tests pass
- Mock external dependencies appropriately

## Architecture Compliance
- Follow Clean Architecture principles
- Respect layer boundaries (Domain → Application → Infrastructure)
- Use dependency injection for external services
- Maintain SOLID principles

## Documentation Updates
- Update docstrings for new/modified functions
- Ensure type hints are complete and accurate
- Update README.md if public interface changes

## Database Changes
- Create and apply migrations if schema changes: `make alembic-make-migrations "description"`
- Test migrations on clean database
- Verify backward compatibility

## Final Verification
- Start development environment: `make up-dev`
- Verify health endpoint: `http://localhost:8666/v1/ping`
- Test main functionality through Streamlit UI: `http://localhost:8501/`
- Check logs for any errors or warnings

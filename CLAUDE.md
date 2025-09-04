# Software Architecture Learning Environment

## Core Learning Objectives

- Master Test-Driven Development (TDD)
- Apply Clean Architecture (Hexagonal/Onion)
- Practice SOLID & CUPID principles
- Learn Domain-Driven Design patterns

## Architecture Standards

### Hexagonal Architecture Layers

- **Domain Layer**: Pure business logic, no dependencies
- **Application Layer**: Use cases, orchestration
- **Infrastructure Layer**: External systems, databases, APIs
- **Presentation Layer**: Controllers, CLI, web interfaces

### SOLID Principles Enforcement

- **S**: Single Responsibility - one reason to change
- **O**: Open/Closed - open for extension, closed for modification
- **L**: Liskov Substitution - subtypes must be substitutable
- **I**: Interface Segregation - many specific interfaces
- **D**: Dependency Inversion - depend on abstractions

### CUPID Properties Focus

- **Composable**: Build from smaller parts
- **Unix philosophy**: Do one thing well
- **Predictable**: Consistent behavior
- **Idiomatic**: Follow language conventions
- **Domain-based**: Reflect business concepts

## Development Workflow

### TDD Cycle (RED-GREEN-REFACTOR)

1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Clean up while keeping tests green

### Code Quality Gates

- All code must have tests
- No commits without passing tests
- Use dependency injection
- Follow project naming conventions
- Document architectural decisions

## Technology Preferences

- **Python**: Use type hints, dataclasses, pytest
- **TypeScript**: Strict mode, explicit interfaces
- **Testing**: Property-based testing when applicable
- **Dependencies**: Prefer composition over inheritance

## Learning Approach

- Start with simple problems using TDD
- Gradually introduce architectural patterns
- Always explain WHY, not just HOW
- Focus on maintainable, readable code

# Pipeline Monitor System Tray App

## Domain Overview

A lightweight desktop system tray application for monitoring CI/CD pipeline status from GitHub. The app provides real-time visual feedback through a colored icon:
- **RED circle**: Pipeline failed
- **YELLOW circle**: Pipeline running
- **GREEN circle**: Pipeline passed

The focus is on simplicity and learning AI-assisted development with sub-agents in Python.

## Core Features

1. **System Tray Icon**
   - Display colored status indicator (red/yellow/green)
   - Update icon when pipeline status changes
   - Click to open settings dialog

2. **Pipeline Polling**
   - Poll GitHub provider API for pipeline status
   - Polling interval: every 2 minutes
   - Handle API errors gracefully

3. **Settings Dialog**
   - Configure GitHub repository URL
   - Set API credentials/tokens
   - Persist settings across sessions

## Technical Guidelines

### Coding Conventions
- Use type hints for all function signatures
- Follow PEP-8 naming: `snake_case` for functions/variables, `PascalCase` for classes
- Use f-strings for string formatting
- Prefer pathlib over os.path
- Use double-quotes for strings by default

### Testing (pytest)
- **BDD/TDD integration tests** with Arrange-Act-Assert structure
- Test features and behavior, not implementation details
- Use pytest fixtures for test setup
- Mock only external dependencies (API calls, filesystem, network)
- Keep tests deterministic (use freezegun for time, set random seeds)

### TDD Process (CRITICAL - FOLLOW EXACTLY)
1. **RED**: Write ONE failing test at a time
   - Only ONE test - never multiple tests
   - Verify it fails for the correct reason (not syntax/missing deps)
   - Use red-test-writer agent for this phase
2. **GREEN**: Write minimal code to pass that ONE test
   - Absolute minimum implementation
   - Use green-minimal-implementer agent for this phase
3. **REFACTOR**: Improve code while keeping test green
   - Use code-refactorer agent after each green phase (if refactoring necessary)
4. **REPEAT**: Start next cycle with ONE new failing test

### Architecture
- **Separation of Concerns**
  - GUI layer (system tray, dialogs) - framework-specific code
  - Business logic layer (status management, polling) - framework-agnostic
  - API client layer (Git provider APIs) - abstracted and mockable
  - Data layer (settings persistence) - file-based or simple database

- **Dependency Injection**
  - Use dependency injection for testability
  - Abstract external dependencies behind interfaces/protocols
  - Make components loosely coupled

### Code Quality
- **Limits**: Module: ~300 lines (flexible), Function: 25 lines (prefer 10-15), Nesting: 3 levels max (prefer 1-2)
- Use guard clauses to flatten logic
- Automated linting (Ruff), type checking (Mypy), security checks (Bandit)
- **Self-documenting code**: Write clear, readable code without excessive comments
- Use docstrings for public APIs only

### Commands to Run
- After code changes: `pytest` (run tests)
- Before completing tasks: `pytest && ruff check && mypy .` (full compliance)
- Generate coverage: `pytest --cov=. --cov-report=html --cov-report=term-missing`

### Code Quality Commands
**Full Checks:**
- `pytest && ruff check && mypy .` - Run ALL checks (tests + quality + types)
- `pytest --cov=. --cov-report=html` - Tests with coverage report

**Individual Tools:**
- `ruff check` - Linting and code quality
- `ruff check --fix` - Auto-fix issues
- `ruff format` - Format code
- `mypy .` - Type checking
- `bandit -r .` - Security scanning
- `pip-audit` - Dependency vulnerability scanning

**Testing:**
- `pytest` - Run all tests
- `pytest tests/test_api.py` - Run specific test file
- `pytest -k test_name` - Run tests matching pattern
- `pytest --cov=. --cov-branch` - Include branch coverage

### Development Workflow (TDD)
1. **RED**: Write ONE failing test using `red-test-writer` agent
   - Verify it fails for the right reason with `pytest`
2. **GREEN**: Implement minimal code using `green-minimal-implementer` agent
   - Just enough to make that ONE test pass
3. Run quick check: `ruff check && mypy .`
4. **REFACTOR**: Improve code if needed (test stays green)
5. **REPEAT**: Go back to step 1 for next feature
6. Before committing: `pytest && ruff check && mypy .`

**NEVER**: Write multiple tests at once or implement before writing a test

### Typical Development Session
```bash
# After making changes, run tests & quick check
pytest
ruff check && mypy .

# Fix any issues automatically
ruff check --fix
ruff format

# Before finishing work
pytest --cov=. --cov-report=html
pytest && ruff check && mypy .

# If all passes, commit
git commit -m "feat: add pipeline polling feature"
```

### Key Reminders
- Don't create files unless necessary
- Prefer editing over creating
- No proactive documentation files
- Follow all limits and guidelines strictly
- Ensure automated compliance checks
- Write self-documenting code without excessive comments
- Focus on clear, readable code that explains itself

### CRITICAL: Task Delegation
**ALWAYS delegate tasks to appropriate sub-agents:**
- **red-test-writer**: Writing ONE failing test at a time
- **green-minimal-implementer**: Making tests pass with minimal code
- **code-refactorer**: Refactoring code after tests pass
- **dependency-manager**: Adding/updating packages, security audits
- **code-quality-reviewer**: Reviewing code changes
- **test-coverage-analyzer**: Coverage quality analysis

**NEVER do the implementation work yourself - delegate to agents!**

### Automated Compliance Setup
The project uses comprehensive automated compliance tools:

1. **Code Quality Tools**
   - Ruff: Linting and formatting (extremely fast, replaces Flake8, Black, isort)
   - Mypy: Static type checking
   - Bandit: Security scanning
   - pip-audit: Dependency vulnerability checks

2. **Testing & Coverage**
   - pytest: TDD/BDD style tests with AAA structure
   - pytest-cov: 90% minimum coverage requirement
   - pytest fixtures: Test data and setup

3. **Git Hooks (optional)**
   - Pre-commit: Ruff, Mypy on staged files
   - Pre-push: Full test suite, all quality checks

### Python Best Practices
- Use dataclasses for data structures
- Use context managers for resource management
- Use type hints from `typing` module
- Leverage standard library (itertools, functools, collections)
- Use list/dict comprehensions appropriately
- Follow PEP-8 strictly (enforced by Ruff)

### Package Guidelines
- **CRITICAL: Only install packages with permissive open-source licenses**
  - NEVER install packages with commercial, proprietary, or GPL licenses
  - Acceptable licenses: MIT, Apache-2.0, BSD, PSF, ISC
  - Always verify package license before installation
  - Use dependency-manager agent for all package operations

## Project Reminders
- Code quality warnings are NEVER acceptable and must always be fixed
- Type errors from Mypy must be resolved, not ignored
- Test coverage below 90% requires justification

# tests/

Test suite for the project, run with `pytest`.

## Structure

```
tests/
  conftest.py         # Shared fixtures
  test_[module].py    # Tests mirroring src/ module structure
```

## Conventions

- Test file names must start with `test_`
- Mirror the `src/` directory structure for discoverability
- Use fixtures in `conftest.py` for shared test data and setup
- Run tests: `pytest tests/`

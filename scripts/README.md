# scripts/

Standalone scripts for one-off tasks, pipeline orchestration, and automation.

## Structure

```
scripts/
  setup_db.py         # Database initialization
  run_pipeline.py     # End-to-end pipeline execution
  export_results.py   # Export/upload results
```

## Conventions

- Scripts should be executable from the project root: `python scripts/[name].py`
- Import shared logic from `src/` rather than duplicating code
- Include a docstring at the top of each script explaining its purpose and usage

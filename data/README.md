# data/

Data directory for raw inputs, intermediate outputs, and processed results.

## Structure

```
data/
  raw/          # Original, immutable data files
  processed/    # Cleaned and transformed data
  external/     # Data from third-party sources
```

## Conventions

- Raw data is never modified in place — always write to `processed/`
- Large files should be added to `.gitignore` and managed externally (S3, DVC, etc.)
- Include a data dictionary or schema description for each dataset

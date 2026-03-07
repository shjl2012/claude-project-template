# data/ — Data Directory

- **Raw data is immutable**: Never overwrite files in `raw/`. Write outputs to `processed/`.
- **Sensitive data**: Do not commit PII or credentials. Use `.gitignore` for large/sensitive files.
- **Schema changes**: If column names or data formats change, update the data dictionary and notify downstream consumers in `src/` and `notebooks/`.

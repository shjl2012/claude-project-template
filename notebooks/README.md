# notebooks/

Jupyter notebooks for exploratory data analysis, prototyping, and experimentation.

## Structure

```
notebooks/
  01_eda.ipynb          # Exploratory data analysis
  02_feature_eng.ipynb  # Feature engineering experiments
  03_modeling.ipynb      # Model training and evaluation
  ...
```

## Conventions

- Prefix notebooks with a number to indicate execution order
- Notebooks are for exploration — production logic should be extracted to `src/`
- Clear all outputs before committing (or use a pre-commit hook to strip outputs)

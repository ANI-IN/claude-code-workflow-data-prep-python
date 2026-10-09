# Reference Solution: Min-Max Scaling

This branch, `solution/minmax-scaling`, holds a finished result of the exercise: min-max scaling implemented in the feature pipeline, following the Explore, Plan, Code, Commit loop.

Use it only as a reference to compare against your own work. The `main` branch is the starting point, so do the exercises there first and check this branch afterward:

```bash
git diff main origin/solution/minmax-scaling
```

## What changed

**`src/data_prep/pipeline/feature_pipeline.py`**

- `prepare_column(values, scaling="minmax")` now returns scaled values instead of raising `NotImplementedError`.
- `minmax_scale()` maps the smallest value to `0.0`, the largest to `1.0`, and everything else in between, using `(value - min) / (max - min)`.
- Missing values stay `None` in the same positions, and they are ignored when finding the minimum and maximum. This follows the `CLAUDE.md` rule: never silently drop or invent missing values.
- A constant column, where every value is the same, has a range of zero. Instead of raising `ZeroDivisionError`, every present value maps to `0.0`, the same choice scikit-learn's `MinMaxScaler` makes. This is the case the plan revision asked to test. Mapping to `0.5` or raising a clear error would also be fine if the plan documents it.
- A column that is empty or entirely missing comes back unchanged.
- If the values are so far apart that `max - min` overflows to infinity (values near the float limit of about `1e308`), the values are halved before scaling. Halving is exact, so the output stays in `[0, 1]` instead of turning into `NaN`. The reviewer subagent tends to catch this one.
- `prepare_column()` always returns a new list, so the caller's data is never modified.
- `prepare_column_keeping_original()` returns a frozen `PreparedColumn` dataclass holding both the original values and the prepared output, stored as tuples so neither can be changed afterward.
- The no-scaling path behaves exactly as before.

**`src/data_prep/api/dataset.py`**

- `handle_prepare()` accepts an optional `scaling`, so the feature can be reached through the public route. The default stays `"none"`, so existing callers are unaffected.

**`pyproject.toml`**

- Unchanged. The feature needs no new dependency. This is the answer to the "do we need a new dependency?" question from the Explore and Plan step: min-max scaling is a few lines of arithmetic on plain Python lists, and `CLAUDE.md` asks to prefer the standard library.

**`tests/`**

- New tests cover missing values, negative values, a real dataset column, a constant column, empty and all-missing columns, a range that overflows the float limit, not modifying the input, keeping the original values, and requesting scaling through the API.

## Success criteria met

- `prepare_column()` can return min-max scaled values in `[0, 1]`.
- The original values are still available.
- `pytest` passes: 34 tests, including the min-max test that fails on `main`.
- `ruff check .`, `ruff format --check .`, and `mypy` pass with no issues.

## How to check it

```bash
git checkout solution/minmax-scaling
pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
mypy
```

## Notes

- **Why not scikit-learn?** `sklearn.preprocessing.MinMaxScaler` does the same job and is the right tool once a project already uses NumPy arrays and scikit-learn models. Here the pipeline works on plain lists of a few columns, so adding scikit-learn (and NumPy with it) as a runtime dependency would be a lot of weight for five lines of arithmetic.
- **Train versus test data.** In a real training pipeline you compute the minimum and maximum on the training set only, then reuse those numbers to scale validation and test data. Computing them on all the data leaks information from the test set into training. That is a natural next feature to take through the loop.
- **Scope.** The teaching point is the workflow, not the scaler. A production service would also handle outliers, which can squash every other value toward 0 or 1.

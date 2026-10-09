# Exercise 2: Code (Against the Plan)

**Goal:** Approve the plan from Exercise 1 and let Claude implement min-max scaling, using the test suite as the source of truth. This is the Code step of the loop.

## Background

Once the plan looks right, you approve it and Claude works through the steps. Claude does its best to troubleshoot before it considers the plan finished, but sometimes you will need to step in. Because you planned first, you also have the context of how you got here, which helps guide Claude's next decisions.

Three things make this phase smoother, and all of them are already set up in this project:

- **Success criteria.** The plan should state what "correct" looks like. Here it is concrete: the pipeline returns values in `[0, 1]`, missing values stay `None`, callers can get the original values alongside the scaled ones, and the tests pass.
- **Tools that let Claude check its own work.** `pytest`, `ruff`, and `mypy` give fast, objective feedback, so there is less back-and-forth with you.
- **A test suite as the source of truth.** `tests/test_feature_pipeline.py` defines the feature, so Claude troubleshoots against real feedback instead of guessing. Make sure tests are reliable before you trust them, to avoid false positives.

## Steps

1. Before approving, create a branch for your work, so `main` stays as the starting point. You can run a shell command from inside Claude Code by starting it with `!`, or use a second terminal:

   ```
   ! git switch -c minmax-scaling
   ```

2. When the plan looks right, **Approve** it. Claude begins working through the steps. You can let it auto-accept file edits or confirm each one.

3. After the change, run the checks:

   ```bash
   pytest
   ruff check .
   ruff format --check .
   mypy
   ```

4. Read the results. If a test fails, let Claude troubleshoot against the failing assertion rather than guessing. The failing test tells Claude precisely what "correct" means.

5. If Claude keeps running into the same issue, ask it to save the solution to `CLAUDE.md`, so it does not rediscover the fix next time.

6. Stop when every check passes and you have reviewed the change yourself. You will commit in Exercise 3.

## What to observe

- Approving the plan is the moment Claude switches from read-only exploration to making edits. You chose when that happened.
- `test_minmax_scales_values_into_the_unit_range` is written to fail until the feature exists. Watch it move from failing to passing as the implementation lands.
- A test that fails for the right reason is useful. It is the signal that guides the implementation.
- If the plan included your revision, Claude also adds tests for a constant column (every value the same, so `max - min` is zero) and for keeping the original values. Without that test, a naive formula raises `ZeroDivisionError` on real data.
- A constant column has no single right answer. Mapping it to `0.0`, mapping it to `0.5`, or raising a clear error are all defensible, as long as the plan states the choice and a test pins it down. The reference solution uses `0.0`, the same as scikit-learn's `MinMaxScaler`.
- Claude may tidy up the `FEATURE TASK` note in the module docstring once the feature works. That is expected: it is a teaching marker, and your branch no longer needs it.

## Look at the code

Open the tests before you run anything:

- `tests/conftest.py` builds `housing_csv`, a small house-prices table with missing cells. Using realistic data means the edge cases show up in the tests, not only in production.
- `tests/test_feature_pipeline.py` checks that `[1000, 1500, 2000]` scales to `[0.0, 0.5, 1.0]`: the smallest value becomes 0, the largest becomes 1, and everything else lands in between.
- The module docstring says plainly that the min-max test is written to fail until the feature is implemented.

The failing min-max test is not a defect. It is the source of truth that defines the feature. Make it pass by implementing the feature, not by weakening the test.

Then open `src/data_prep/pipeline/feature_pipeline.py` again and compare the implementation against its `Success criteria`. The feature is done when the pipeline can return scaled values, the original values are still available, and all checks pass.

## Learning outcome

You practiced the Code step. You approved a reviewed plan, implemented it against clear success criteria, and used a reliable test suite, plus a linter and type checker, so troubleshooting was grounded in real feedback rather than guesswork.

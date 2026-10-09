# Explore, Plan, Code, Commit: A Python Workflow Project

A small, hands-on Python project for practicing the four-step loop that keeps AI-assisted coding with Claude Code reliable: **Explore, Plan, Code, Commit**. In about 15 minutes you take one real feature, adding min-max feature scaling to an ML data-preparation pipeline, through all four steps, and you practice course-correcting early, while it is cheapest.

It is written for early-career software and AI/ML engineers. The code is deliberately small, but it is organized the way a real Python service is: a `src/` package layout, type hints checked by mypy, linting with Ruff, and a pytest suite that acts as the source of truth.

## 1. Project Overview

The sample code is a data-preparation service for model training. It downloads a CSV dataset (a small house-prices table) from a dataset store over HTTPS, reads one numeric column, parses it into numbers with missing cells kept as `None`, and returns the prepared values.

Before a model is trained, numeric features are usually scaled to a common range. Without scaling, a feature with a large range, such as square footage in the thousands, can drown out a feature with a small range, such as the number of bedrooms. Min-max scaling maps every value into `[0, 1]`, and it is one of the first preprocessing steps most ML engineers write.

The project exists to teach a working habit rather than to ship a product:

- Let Claude read the code and propose a plan before writing anything.
- Approve the plan and let Claude implement it against a test suite.
- Get a fresh-eyes review from a subagent, then a commit message in your style.

The feature used to teach the loop is min-max scaling in the feature pipeline. You build it yourself as you follow the exercises.

## 2. Intentional Starting State

**Some parts of this project are intentionally incomplete, and you should not patch them before the exercise asks you to.** They create the "before" state of the exercise.

- `src/data_prep/pipeline/feature_pipeline.py` carries a `FEATURE TASK` comment, and calling `prepare_column(..., scaling="minmax")` raises `NotImplementedError` on purpose.
- `tests/test_feature_pipeline.py::test_minmax_scales_values_into_the_unit_range` is written to fail until the feature is built.
- The project has no runtime dependencies. Whether the feature needs one, such as NumPy or scikit-learn, is a question for the Explore and Plan step.

So on `main`, `pytest` reports **one intentionally failing test**. That failure is the target for the Code step.

## 3. Branches

| Branch | Contents |
|---|---|
| `main` | The starting point. Do the exercises here. |
| `solution/minmax-scaling` | A reference solution with min-max scaling implemented and every test passing. See `SOLUTION.md` on that branch. Compare against it only after you finish. |

## 4. Prerequisites

- Python 3.10 or newer. Check with `python3 --version`. On some systems, including macOS, `python3` can be older than 3.10. If so, install a newer Python and create the virtual environment with it by name, for example `python3.12 -m venv .venv`.
- Git.
- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) installed, so that `claude` is available in your terminal.

## 5. Setup

```bash
git clone https://github.com/ANI-IN/claude-code-workflow-data-prep-python.git
cd claude-code-workflow-data-prep-python

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

`pip install -e ".[dev]"` installs the package in editable mode along with the development tools: pytest, Ruff, and mypy. The tests never touch the network, so you do not need a dataset store or a token to run them.

## 6. Commands

| Task | Command |
|---|---|
| Run the tests | `pytest` |
| Lint | `ruff check .` |
| Check formatting | `ruff format --check .` |
| Type check | `mypy` |

On `main`, `pytest` should end with `1 failed, 22 passed`. The one failure is the min-max test, and it is intentional, so pytest still prints `FAILED` and exits with a non-zero code until you build the feature. Ruff and mypy should pass cleanly.

## 7. Project Structure

```
claude-code-workflow-data-prep-python/
├── CLAUDE.md                     Project conventions Claude reads every session
├── README.md                     This file
├── pyproject.toml                Package metadata, dependencies, and tool settings
├── .gitignore
├── .claude/
│   └── agents/
│       └── code-reviewer.md      Read-only reviewer subagent used in the Commit step
├── docs/
│   └── explore-plan-code-commit.docx   The full lesson document
├── src/
│   └── data_prep/
│       ├── config.py             Settings read from environment variables (no hardcoded tokens)
│       ├── api/
│       │   └── dataset.py        Public route: validates the name, fetches the CSV, prepares a column
│       ├── integrations/
│       │   └── dataset_source.py Downloads a CSV dataset over HTTPS
│       └── pipeline/
│           └── feature_pipeline.py  Column processing. The min-max feature is built here
├── tests/
│   ├── conftest.py               Shared fixtures (a small house-prices CSV with missing cells)
│   ├── test_feature_pipeline.py  Source of truth for the pipeline. The min-max test fails until built
│   ├── test_dataset_api.py       Name validation and request flow
│   ├── test_dataset_source.py    HTTPS URL, auth header, and timeout (no real network calls)
│   └── test_config.py            Settings come from the environment
└── exercises/
    ├── README.md                 Why the loop works, how to use the exercises, troubleshooting
    ├── 01-explore-and-plan.md
    ├── 02-code-against-the-plan.md
    └── 03-commit-with-review.md
```

## 8. Exercises

Start Claude Code from the project root and work through the guides in order:

```bash
claude
```

1. [`exercises/README.md`](exercises/README.md): why the loop works, how to use the guides, and troubleshooting.
2. [`exercises/01-explore-and-plan.md`](exercises/01-explore-and-plan.md): explore the code and produce a plan in Plan Mode.
3. [`exercises/02-code-against-the-plan.md`](exercises/02-code-against-the-plan.md): approve the plan and implement it against the tests.
4. [`exercises/03-commit-with-review.md`](exercises/03-commit-with-review.md): run a read-only subagent review, then commit.

Each guide tells you what to do, what to observe, what to look for in the code, and the intended learning outcome. The same lesson is also available as a Word document in [`docs/`](docs/).

## 9. Additional Notes

- **Conventions.** `CLAUDE.md` holds the rules Claude reads every session: data-source endpoints must use HTTPS, credentials are never hardcoded, missing values stay `None`, and code follows PEP 8 with type hints, enforced by Ruff and mypy.
- **The review step.** The Commit step uses the read-only `code-reviewer` subagent in `.claude/agents/code-reviewer.md`. It runs in its own context, so it does not carry the assumptions the main agent built up while writing the change.
- **Scope.** This is a teaching project, not production software. The data source and pipeline are deliberately minimal so the workflow stays in focus.

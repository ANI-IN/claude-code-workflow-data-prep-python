# Project
ML data-preparation service. Python backend that downloads CSV datasets
and prepares their numeric columns as features for model training.

# Map
- src/data_prep/api/          public dataset API handlers
- src/data_prep/integrations/ clients for external data sources
- src/data_prep/pipeline/     column processing (parse, clean, scale); add feature work here
- src/data_prep/config.py     settings read from environment variables
- tests/                      pytest suite; the source of truth for "correct"

# Commands
- Install:    `pip install -e ".[dev]"` (inside a virtual environment)
- Run tests:  `pytest`
- Lint:       `ruff check .` and `ruff format --check .`
- Type check: `mypy`

# Code Style
- PEP 8, 4-space indentation, enforced by Ruff.
- Type hints on every function; mypy runs in strict mode.
- Absolute imports from `data_prep`; no wildcard imports.
- All data-source endpoints must use HTTPS (https://).
- Never hardcode credentials; read them from config.
- Missing values are `None`. Never silently drop or invent them.
- Prefer the standard library; add a runtime dependency only when it clearly pays for itself.

# Workflow
Follow Explore -> Plan -> Code -> Commit.
- Explore & plan in Plan Mode before editing.
- State explicit success criteria in every plan.
- Validate against tests/ (and Ruff + mypy) before considering work done.
- Run the code-reviewer subagent before committing.

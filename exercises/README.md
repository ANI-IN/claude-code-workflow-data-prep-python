# Exercises: The Explore, Plan, Code, Commit Workflow

These exercises are a hands-on walkthrough of the four-step loop that makes Claude Code reliable. You take one real feature, adding min-max feature scaling to an ML data-preparation pipeline, through the full loop, and practice course-correcting early while it is cheapest.

All examples use Python.

## Why this loop

Most people jump straight to "write the code," which means more correcting later. The Explore, Plan, Code, Commit loop front-loads the thinking, so problems get caught before any code exists, where they are cheapest to fix.

| Step | What it does |
|---|---|
| Explore | Gives Claude the context it needs about your project. |
| Plan | Produces an approach you can review and measure success against. |
| Code | The back-and-forth to reach the final implementation. |
| Commit | Review and push, then start the next feature. |

## How to use these exercises

1. Read the root [`README.md`](../README.md) first and complete the setup, so that `pytest` runs inside your virtual environment.
2. Start Claude Code from the project root, with your virtual environment active:

   ```bash
   claude
   ```

3. Work through the exercises in order. Each file is one step of the loop and builds on the one before it:
   - [`01-explore-and-plan.md`](01-explore-and-plan.md): read the code and produce a plan in Plan Mode.
   - [`02-code-against-the-plan.md`](02-code-against-the-plan.md): approve the plan and implement it against the test suite.
   - [`03-commit-with-review.md`](03-commit-with-review.md): run a read-only subagent review, then write a commit message in your style.
4. Keep each exercise open while you work. Do what the **Steps** section says, watch for what **What to observe** calls out, and read the **Look at the code** notes so you understand why each move matters.

## A note on the starting state

The project ships intentionally incomplete. Min-max scaling is not built yet, and one test is written to fail until you build it. These are deliberate teaching markers, not defects. Leave them in place until the Code step asks you to implement the feature. When you finish, you can compare your work with the `solution/minmax-scaling` branch.

## Key takeaways

- Explore and Plan in Plan Mode (Shift + Tab) so Claude proposes an approach before editing anything.
- Course-correct on the plan. It is the cheapest place to fix direction, because no code exists yet.
- Code against clear success criteria and a reliable test suite that acts as the source of truth.
- Give Claude tools that let it check its own work. Here that means `pytest`, `ruff`, and `mypy`.
- Commit only after a read-only subagent review, then generate a commit message in your style.
- The loop ties the core Claude Code practices together: Plan Mode for exploring, `CLAUDE.md` for conventions, subagents for review, and context discipline throughout.

## Troubleshooting

| Symptom | Resolution |
|---|---|
| Claude starts editing before you are ready | You are not in Plan Mode. Press Shift + Tab until the footer reads "plan mode on". |
| The plan misses requirements | Add explicit success criteria to your prompt and ask for a revision before approving. |
| Tests pass but the result is wrong | The tests are not a reliable source of truth yet. Tighten them first, then run them again. |
| The reviewer repeats the main agent's blind spots | Confirm it is a separate subagent with read-only tools, not the same thread reviewing itself. |
| `ModuleNotFoundError: data_prep` | Activate the virtual environment and run `pip install -e ".[dev]"` from the project root. |
| `requires a different Python` during `pip install` | The virtual environment uses Python older than 3.10. Delete `.venv` and recreate it with a newer interpreter, for example `python3.12 -m venv .venv`. |
| `git push` is rejected | You cloned a repository you cannot push to. Commit locally, or fork the repository on GitHub first if you want to push your work. |

# Exercise 3: Commit (with a Fresh-Eyes Review)

**Goal:** Before you push, get a second opinion from a read-only subagent, then have Claude write a commit message in your style. This is the Commit step that closes the loop.

## Background

A subagent runs in its own context. It looks at the code with fresh eyes and does not carry the bias the main agent picked up while writing the change this session. That independence is the point, because it lets the reviewer catch what the author missed.

The reviewer for this project is already defined in `.claude/agents/code-reviewer.md`, so Claude Code picks it up automatically.

## Steps

1. Once you have tested the change yourself and are happy with it, ask Claude to run a review with the read-only code-reviewer subagent:

   ```
   Use the code-reviewer subagent to review the min-max scaling changes before I commit.
   ```

2. Read the structured assessment the reviewer returns. It covers security, correctness, conventions, and whether the change is ready to merge. Address anything it flags, then run `pytest`, `ruff check .`, `ruff format --check .`, and `mypy` again.

3. When the review is clean, ask Claude to write the commit message in your style:

   ```
   Write a commit message for these changes in our conventional-commits style.
   ```

4. Review the message and commit it on your branch. Then you are ready to start the next feature. Rinse and repeat. You cloned this repository, so you cannot push to it. Fork it on GitHub first if you want to push your work.

5. Optional: compare your result with the reference solution:

   ```bash
   git diff origin/solution/minmax-scaling       # your branch versus the reference
   git diff main origin/solution/minmax-scaling  # what the reference changed
   ```

## What to observe

- The reviewer reads the changed files and returns a report. Confirm it runs as a separate subagent with read-only tools, not the same thread reviewing its own work.
- A fresh context is what catches blind spots. If the same thread reviewed itself, it would tend to repeat its own assumptions.
- Typical findings for this feature include division by zero on a constant column, a column where every value is missing, values so large that `max - min` overflows to infinity and the output turns into `NaN`, a new dependency added without a clear reason, and scaling that changes the caller's list in place instead of returning a new one.
- The commit message reflects your conventions, because you asked for your style rather than a generic message.

## Look at the code

Open `CLAUDE.md` at the project root. This is where the project conventions live, and both the reviewer and the main agent read it. Notice the rules the review holds the change to: HTTPS for every data-source endpoint, no hardcoded credentials, missing values kept as `None`, type hints everywhere, and code that passes Ruff and mypy. A good commit respects these conventions.

Then open `.claude/agents/code-reviewer.md`. Its `tools` line is restricted to `Read, Grep, Glob`, which is what lets it review your work without editing it.

## Learning outcome

You practiced the Commit step. You used an independent, read-only subagent for a fresh-eyes review before committing, then generated a commit message in your own style. Together with the earlier exercises, you have now run the full Explore, Plan, Code, Commit loop from start to finish.

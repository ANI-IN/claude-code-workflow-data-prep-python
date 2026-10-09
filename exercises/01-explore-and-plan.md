# Exercise 1: Explore and Plan (in Plan Mode)

**Goal:** Let Claude read the codebase and propose an approach for adding min-max scaling, before a single line of code is written. This is the Explore and Plan half of the loop, and it is the cheapest place to catch problems.

## Background

Plan Mode lets Claude read your code but not edit it. Claude gathers context and returns a plan of action that you can review and measure against your own success criteria. Because nothing is written yet, this is the best moment to course-correct.

You can also run the Explore subagent outside Plan Mode when you only want a general summary of a codebase without intending to change it.

## Steps

1. Activate your virtual environment, then start Claude Code from the project root:

   ```bash
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   claude
   ```

2. Enter Plan Mode. Press **Shift + Tab** until the footer reads "plan mode on".

3. Ask Claude to explore and plan the feature:

   ```
   I need to add min-max scaling to our feature pipeline. Figure out where
   in the pipeline it should happen, whether we need a new dependency, and
   how to approach it. Keep missing values as None per our conventions.
   ```

4. Read the plan Claude returns. Decide whether it meets your criteria. If anything is off, such as the wrong location, a missing step, or no test coverage, ask for a revision now, before any code is written. For example:

   ```
   Revise: keep the original values too, and add a test for a column
   where every value is the same.
   ```

5. Do not approve yet. Stop once you have a plan you are happy with. You will approve and implement it in Exercise 2.

## What to observe

- In Plan Mode, Claude reads files but never edits them. Check that the footer reads "plan mode on" before you send the prompt.
- Claude will likely read `src/data_prep/pipeline/`, `src/data_prep/api/`, `pyproject.toml`, `CLAUDE.md`, and the tests, then propose doing the scaling inside `src/data_prep/pipeline/feature_pipeline.py`, where columns are already processed.
- A good plan answers the dependency question with evidence. The pipeline works on plain Python lists, the project has no runtime dependencies, and `CLAUDE.md` says to prefer the standard library. Min-max scaling is a few lines of arithmetic, so pulling in NumPy or scikit-learn just for `MinMaxScaler` is hard to justify here. If the plan does add a dependency, it should say why, and put it in the runtime `dependencies` list, not the `dev` extra.
- A good plan also thinks about the data, not only the formula: what happens to `None` values, and what happens when the column's minimum equals its maximum. Your revision makes that second case explicit.
- The plan is a proposal, not a commitment. Requesting a revision here costs nothing, because no code exists yet.

## Look at the code

Open `src/data_prep/pipeline/feature_pipeline.py` and study the starting state. Notice two things:

- The `Scaling` type allows `"minmax"`, yet the code is marked as not implemented yet.
- Calling `prepare_column(values, scaling="minmax")` raises `NotImplementedError("Min-max scaling not implemented yet")`.

These are intentional. They describe the "before" state of the exercise and tell you exactly what the feature needs to do. Read the `FEATURE TASK` and `Success criteria` sections of the module docstring. They are your target for Exercise 2. Do not change anything yet.

## Learning outcome

You practiced the Explore and Plan half of the loop. You saw that Plan Mode keeps Claude read-only while it gathers context, and that reviewing and revising the plan, including its dependency choices and data edge cases, is the cheapest way to steer direction before any code exists.

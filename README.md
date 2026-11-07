# hive-test

Deliberately broken code for live end-to-end testing of [HiveMind](https://github.com/lakshya076/HiveMind) and [hivemind-worker](https://github.com/lakshya076/hivemind-worker).

Each task under `tasks/` is a small bug or missing feature with a `check.py` that fails until it is fixed. You dispatch a task to your fleet with `hive dispatch`, workers fix it on `exp/*` branches, and you merge the winner locally with `hive merge`.

> [!IMPORTANT]
> **Never push a fix to `main`.** Workers always branch from the default branch, so `main` must stay broken. If a fix lands on `main`, every later run of that task ends `no_changes`. Merge winners into your local clone only. To get a clean local copy again, run `git reset --hard origin/main` (this discards your local merges).

## Tasks

| Task | What is broken | What it exercises in HiveMind |
|---|---|---|
| `tasks/add` | `add()` subtracts | Smoke test: quick, almost always solved. Use it to check a newly added machine |
| `tasks/multi_file` | A bug in `prices.py` **and** one in `cart.py` | The agent edits two files; the commit and the merge preview span both |
| `tasks/perf` | `fib()` is correct but exponential; `check.py` needs `fib(90)` in under 5 s | `--bench`: `bench.py` prints `{"fib90_us": ...}` into the Benchmark column, so strategies can be compared |
| `tasks/new_file` | `slugify.py` does not exist yet (the spec is in `check.py`) | The agent creates a new file, which the worker must commit |
| `tasks/conflict` | `greet()` formats wrongly | Every fix rewrites the same lines: merge one strategy, then another, and the second merge conflicts |

Every check uses the Python standard library only, so workers need nothing beyond Python 3.

## Running a task

Run these from a clone of this repository on the master machine. Set `repo_url` in `~/.hivemind/cluster.json` to this repository, or pass `--repo https://github.com/lakshya076/hive-test`.

Linux workers usually only have `python3`, and Windows workers only `python`. Every command below therefore tries both, and works on Linux (`sh`) and Windows (`cmd`) workers alike.

```bash
# Smoke test, one strategy per worker
hive dispatch "Fix add() in tasks/add/add.py so tasks/add/check.py passes. Only change add.py." \
  --test "python3 tasks/add/check.py || python tasks/add/check.py"

# Two files to fix
hive dispatch "Fix the bugs in tasks/multi_file so tasks/multi_file/check.py passes. Do not edit check.py." \
  --test "python3 tasks/multi_file/check.py || python tasks/multi_file/check.py"

# Competing strategies with a benchmark
hive dispatch "Make fib() in tasks/perf/fib.py fast enough for tasks/perf/check.py. Keep its signature." \
  --strategy iterative --strategy memoized \
  --test "python3 tasks/perf/check.py || python tasks/perf/check.py" \
  --bench "python3 tasks/perf/bench.py || python tasks/perf/bench.py"

# A new file
hive dispatch "Create tasks/new_file/slugify.py as specified in tasks/new_file/check.py. Do not edit check.py." \
  --test "python3 tasks/new_file/check.py || python tasks/new_file/check.py"

# Merge conflict: strategies that write greet() differently
hive dispatch "Fix greet() in tasks/conflict/greet.py so tasks/conflict/check.py passes." \
  --strategy f-string --strategy str-format \
  --test "python3 tasks/conflict/check.py || python tasks/conflict/check.py"
```

Then follow and finish the run:

```bash
hive status --watch                      # until every strategy finishes
hive logs                                # what each worker reported
hive merge                               # merge the winner into your LOCAL main; do not push
hive merge --worker ari:iterative --yes  # same, without prompts
```

With more strategies than workers, strategies wrap round the workers, so a single machine can run several. For the conflict task, merge one strategy, then run `hive merge` again and pick the other; the second merge should stop with a conflict message.

## Testing failure paths

Outcomes such as `failed` don't depend on the model, so force them with the test command:

```bash
hive dispatch "Fix add() in tasks/add/add.py." --test "exit 1"   # ends failed (works in sh and cmd)
hive dispatch "Fix add() in tasks/add/add.py." && hive cancel   # ends cancelled
```

## Adding a machine

1. On the new machine, install and start `hivemind-worker`, then run `hivemind-worker key set` with the master's key.
2. On the master, run `hive discover` (or `--tailscale`), select it, then run `hive check`.
3. Dispatch the `add` task to just that machine: `hive dispatch "…" --workers <new-id> --test "…"`. It should end `succeeded`, with its branch on GitHub.

## Cleaning up

Every run pushes `exp/<run_id>/<worker>-<strategy>` branches here. Delete the branches of a finished run with:

```bash
git push origin --delete $(git ls-remote --heads origin "refs/heads/exp/<run_id>/*" | cut -f2 | sed 's#refs/heads/##')
```

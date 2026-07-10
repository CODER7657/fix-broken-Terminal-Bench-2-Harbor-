# log-report: Apache Access Log Parser

This Harbor task requires the agent to parse an Apache-style access log into a JSON summary report.

## Defects Found & Fixed

| Area | Defect | Why it violated Harbor format | Fix |
|:---|:---|:---|:---|
| **task.toml** | `artifacts` was a string pointing to `/app/out.json`, which the solution never writes. | The evaluation framework would look for the output in the wrong location, causing all runs to fail. | Changed to `artifacts = ["/app/report.json"]` matching the actual output path. |
| **environment** | Unpinned base image (`python:latest`). | Runs could break unexpectedly if a future image version introduces incompatibilities. | Pinned to `python:3.11-slim@sha256:...`. |
| **environment** | Leaked solution (`solution_hint.py` copied into the agent image). | Agents could read the solution directly instead of solving the task, invalidating the benchmark. | Deleted the file and removed the `COPY` line from the Dockerfile. |
| **verifier** | Gameable checks (only checked file existence/non-empty). | An agent could create a fake file and pass, defeating the objective. | Replaced with strict field-level verification, one test per success criterion. |
| **verifier** | Wrong reward/ctrf paths (`/app/reward.txt`, no `ctrf.json`). | Harbor expects output at fixed paths; wrong paths cause silent evaluation failures. | Fixed to write `/logs/verifier/reward.txt` and `/logs/verifier/ctrf.json`. |
| **instruction** | Vague, no numbered criteria. | Ambiguous instructions make it impossible to evaluate agent performance consistently. | Rewrote with 4 numbered, verifier-matching success criteria. |

## How to Run

```bash
harbor run -p log-report -a oracle
harbor run -p log-report --agent nop
```

Expected: oracle → reward 1, nop → reward 0.

## Verifier Design

`tests/test_outputs.py` has 4 independent tests, each mapping to one numbered criterion in `instruction.md`. Each test independently recomputes expected values from `access.log` rather than trusting the agent's output.

## Proof the Verifier Is Honest

A deliberately bugged solution (`total_requests` corrupted with `+ 999`) was tested. The verifier correctly returned reward 0, failing only the test tied to the corrupted field while the other three passed — proving field-level, not just existence-level, validation.

## Status

Fully fixed and validated: oracle = 1, nop = 0, bugged solution = 0.

## Note

Local Harbor run logs (`jobs/`) are excluded from this repo — they're not part of the task definition.

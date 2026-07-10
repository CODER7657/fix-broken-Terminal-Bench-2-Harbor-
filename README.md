# log-report: Apache Access Log Parser

This Harbor task requires the agent to parse an Apache-style access log into a JSON summary report.

## Defects Found & Fixed

| Area | Defect | Why it violated Harbor format | Fix |
| :--- | :--- | :--- | :--- |
| **task.toml** | Mismatched artifact path. | The evaluation framework would look for the output in the wrong location, causing all runs to fail. | Updated `artifacts = ["/app/report.json"]` to match the verifier expectations. |
| **environment** | Unpinned base image. | Runs could break unexpectedly in the future if a newer image version introduces incompatibilities. | Pinned the Docker image to a specific SHA256 digest. |
| **environment** | Leaked solution. | Agents could read the solution directly instead of solving the task, invalidating the benchmark. | Removed the leaked solution file COPY statement from the `Dockerfile`. |
| **verifier** | Gameable checks. | An agent could just create an empty file and pass the task, defeating the objective. | Replaced with strict field-level verification in `test_outputs.py`. |
| **verifier** | Wrong reward/ctrf paths. | Harbor expects specific output files for scoring, and wrong paths cause silent evaluation failures. | Fixed paths in `test.sh`. |
| **instruction** | Vague instructions with no numbered criteria. | Ambiguous instructions make it hard to evaluate agent performance objectively. | Rewrote `instruction.md` to have clear, numbered success criteria. |

## How to Run

To build and test this task locally using Harbor, run the following commands:

```bash
harbor run -p log-report -a oracle
harbor run -p log-report --agent nop
```

Expected results: The `oracle` run should produce a reward of 1, and the `nop` agent should produce a reward of 0.

## Verifier Design

The verifier script (`tests/test_outputs.py`) is designed with 4 independent tests, each mapping to a numbered success criterion in `instruction.md`. Instead of trusting the agent's output, each test independently recomputes the expected values directly from the provided `access.log`. This ensures robust validation.

## Proof the Verifier Is Honest

To verify the test suite's robustness, a deliberately bugged solution (where `total_requests` was corrupted with `+ 999`) was tested. The verifier correctly yielded a reward of 0, failing only the specific test tied to the corrupted field, while unaffected fields still passed. This demonstrates strict, field-level checking rather than simple existence-level validation.

## Status

Fully fixed and validated, oracle=1, nop=0, bugged solution=0.

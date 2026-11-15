# Harness used for experiment 2 (reference copy)
Scripts as run on 2026-11-15; paths are specific to that machine and need editing.
- `spec.example.json` shows the question/fact format (the real fact lists are kept private so test agents cannot read them).
- `gen.py` writes one prompt file per run (question + arm rules) with random run ids and shuffled order.
- Each agent is told: "Read prompts/<id>.txt and follow it", writes its answer to `answers/<id>.md` and replies DONE only.
- `rate.py` builds two grading packets (answers anonymised: method line, tool names stripped; different shuffles) for two independent grader agents, who write `scores/R1.json` and `scores/R2.json`.
- `analyze.py` joins scores with `bin/agent-usage` output and prints per-arm and per-question tables and grader agreement.

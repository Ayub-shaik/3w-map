# Results

## Experiment 1: 2026-11-15, B Studio, six questions
Model: Sonnet 5.5, fresh agent per run. Raw rows: `data/experiments/2026-11-15-bstudio.json`.

| Q | Type | score A / B | context read A / B (tokens) | tool calls A / B |
|---|---|---|---|---|
| Q1 | lineage of a fix | 6/6, 6/6 | 5.6k / 5.5k | 4 / 6 |
| Q2 | history of a UI rule | 4/5, 5/5 | 7.3k / 4.9k | 7 / 5 |
| Q3 | release state | 4/5, 5/5 | 11.9k / 8.6k | 5 / 6 |
| Q4 | reverse dependency | 1/4, 4/4 | 14.3k / 6.8k | 5 / 6 |
| Q5 | open list | 4/6, 6/6 | 14.2k / 13.0k | 6 / 8 |
| Q6 | code lookup (control) | 3/3, 3/3 | 3.7k / 3.4k | 3 / 4 |
| **total** | | **22/29, 29/29** | **57.0k / 42.2k** | **30 / 35** |

Reading: the map helped most where the answer is a *recorded relationship* (who asked, what depends on it) rather than a fact in a commit message. It did not help, and cost extra calls, where git and docs already answered (Q1, Q6). In Q3 the no-map agent found more ledger detail than the map holds.

Limits: 6 questions, 1 run per arm; scorer not blind; Q3-Q5 fact lists follow the map's links; 2 arm B runs re-run after an empty hand-back; 1 arm A agent saw the plan file (treated it as unverified; plan moved out afterwards).

## Trial telemetry: 30 tasks of one project
Map calls: about 1.2% of tokens. Self-rated effect (yes / neutral / no): 7 / 10 / 12 of 30 tasks (1 not yet rated). Use fell after task 20; later tasks were back-filled into the map. See `data/telemetry/bstudio.json` and the report page.

## Next
Repeat each question 3 times; second blind scorer; other repos; a rework-and-rounds comparison on real tasks, consulting the map first versus not.

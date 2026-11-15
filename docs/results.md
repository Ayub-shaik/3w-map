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

## Experiment 2: 2026-11-15, repeats, two graders, second repo
Raw rows: `data/experiments/2026-11-15-exp2.json`. 30 new runs (Sonnet 5.5, fresh agent each), answers written to files, then scored by two independent grader agents in different shuffled orders with arm labels and tool names stripped. The graders agreed on 97.9% of individual facts.

| group | runs | facts found (grader 1 / 2) | tool calls | context read (tokens) |
|---|---|---|---|---|
| B Studio, without map | 12 | 67% / 69% | 7.2 | 9.3k |
| B Studio, with map | 12 | 93% / 97% | 7.0 | 7.2k (-23%) |
| Second repo, without map | 3 | 100% / 100% | 6.0 | 5.9k |
| Second repo, with map | 3 | 100% / 100% | 7.3 | 5.5k |

Per question (mean of both graders): Q1 lineage of a fix 100% vs 100%; Q2 UI-rule history 65% vs 100%; Q3 release state 60% vs 90%; Q4 reverse dependency 12.5% vs 100%; Q5 open list 67% vs 83%; Q6 code lookup (control) 100% vs 100%; the three second-repo questions 100% vs 100%.

Reading: the B Studio result repeats experiment 1 on fresh runs, with the same pattern: the map wins on recorded relationships (what exists because of a rule, who asked) and ties on plain lookups. **On the second repo it did not help at all**: those questions were answerable from git history, and the map there was built by a separate agent from the same history, so it held nothing extra (6 of the 13 relevant commits appear in it) and cost about one more tool call. That is the honest limit of the idea: a map adds value where it records intent or relationships that the commits and docs do not.

Limits: B Studio fact lists for Q3-Q5 follow the map's own links; graders see only the answer text and cannot verify sources; blinding is partial; the B Studio questions are the same ones as experiment 1; three questions on one second repo; one model.

## Experiment 3: 2026-11-15, decisions recorded only in notes
Raw rows: `data/experiments/2026-11-15-exp3.json`. Six questions about owner decisions that exist only in saved project notes (an index plus one file per decision), not in commit messages; the map held almost none of them. Both arms could read the notes folder and the session ledger; arm B also had the map. One run per arm, two grader agents (100% agreement); **human grading is pending**.

| | facts found | tool calls | context read (tokens) |
|---|---|---|---|
| without map | 100% | 5.0 | 7.9k |
| with map | 100% | 7.5 | 7.6k |

Reading: when a decision is written down in readable notes, a notes folder alone answers it perfectly, and an empty map only adds tool calls (+2.5 per question). The map is not a substitute for good notes; it adds value where relationships and intent are *not* already stored in a form an agent can read directly.

## Trial telemetry: 30 tasks of one project
Map calls: about 1.2% of tokens. Self-rated effect (yes / neutral / no): 7 / 10 / 12 of 30 tasks (1 not yet rated). Use fell after task 20; later tasks were back-filled into the map. See `data/telemetry/bstudio.json` and the report page.

## Next
Repeat each question 3 times; second blind scorer; other repos; a rework-and-rounds comparison on real tasks, consulting the map first versus not.

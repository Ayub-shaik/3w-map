# 3w-map

A small **decision map** that an AI coding agent keeps next to the code, plus the **telemetry and experiments** that test whether it is worth using.

The idea: for every decision in a project, record **why** it exists (the goal it serves), **who** demanded it (a rule, spec or owner review) and **when** it came about (the earlier decision that caused it). Links go *up only*; "what depends on this" is computed by reversing them. A decision can only be marked done with a commit and a written proof.

> **Status: a trial with early evidence, not a proven method.** One project, one agent, one owner. See [what the data shows and does not show](#what-the-data-shows-so-far).

## Who built this, and on what
The data comes from **B Studio**, a private web, Android and iOS product for a drama academy. For about two months every line of that project has been written and committed by an AI agent (Claude), directed by a non-coding owner. The map, the tooling in this repo and the experiments were produced the same way. Treat the numbers as one case study, and check them against your own project before relying on them.

## Quick start (5 minutes)
```bash
git clone https://github.com/Ayub-shaik/3w-map && cd 3w-map
export PATH="$PWD/bin:$PATH"            # pmap, pmap-export, agent-usage, agent-final
cd /path/to/your/repo
mkdir -p .claude/map && cp /path/to/3w-map/examples/nodes.example.jsonl .claude/map/nodes.jsonl
pmap . open                              # what is not done
pmap . find dump                         # search nodes
pmap . why EX-002                        # why / who / when / root goal / evidence
pmap . effects EX-001                    # what depends on it (reverse links)
pmap . task "my first task" --effort low # start a measured task
pmap . add '{"id":"X-001","kind":"decision",...}'
pmap . done X-001 --commit <hash> --verified "what you ran and saw"
pmap . check                             # gaps: no driver, no proof, dangling links
```
`pmap` needs only Python 3 and git. A bare repo name (instead of `.`) is looked up under `PMAP_ROOTS` (default `~/projects:~/Desktop:~/src`).

Give your agent the rules in [`examples/OPERATING.snippet.md`](examples/OPERATING.snippet.md) (paste into `CLAUDE.md` or equivalent). A draft skill is in [`skill/SKILL.md`](skill/SKILL.md).

## What is in here
| Path | What |
|---|---|
| `bin/pmap` | the map tool: `find / why / effects / open / add / done / check`, plus the token meter (`task / report / stat / snap`) |
| `bin/pmap-export` | builds the report feed (per-task tokens, time, rounds, commits, map use) from the agent's session transcript, git and the map |
| `bin/agent-usage`, `bin/agent-final` | measure one sub-agent run (tokens, tool calls, time); print its last text |
| `docs/method.md` | node model, rules, per-task routine, what each metric means |
| `docs/experiment-protocol.md` | how to run the with / without comparison, scoring, and the pitfalls we hit |
| `docs/results.md` | results so far, with limits |
| `data/telemetry/` | per-task numbers from the trial (generic labels only) |
| `data/experiments/` | scored runs of each experiment (no raw agent answers) |
| `report/index.html` | static report page: charts, per-task detail, comparison |
| `examples/` | a tiny map and the agent rules snippet |

View the report locally: `python3 -m http.server 8000` in the repo root, then open `http://localhost:8000/report/`.

## What the data shows so far
**Experiment 1 (2026-11-15):** six questions about the project, each answered twice by a fresh Sonnet agent, once with repo + git + docs + session ledger, once with the map as well. Scored against fact lists written beforehand.

| | without map | with map |
|---|---|---|
| facts found | 22/29 (76%) | 29/29 (100%) |
| text read from tool results | 57k tokens | 42k tokens (-26%) |
| tool calls | 30 | 35 |
| total time | 139 s | 140 s |

The map won on "who asked for this / what depends on it" and on a rule that exists only in the map. It tied on plain lookups that commit messages and docs already answered.

**Experiment 2 (2026-11-15, 30 fresh runs, two independent graders, a second repo):** on B Studio the repeat gave 67-69% without the map and 93-97% with it (read volume -23%, same number of tool calls); the graders agreed on 98% of facts. On a **second repo**, whose map was built by a separate agent from git history only, the map made no difference (100% both ways, one extra tool call): those questions were already answerable from commits. The map helps where intent and relationships are recorded; it adds little where git already says it. Full table in [`docs/results.md`](docs/results.md).

**Trial telemetry (30 tasks):** the map's own calls cost about 1.2% of tokens. By the agent's own rating it helped in 7 of 30 tasks, was neutral in 10, made no difference in 12, and 1 is not yet rated; use dropped sharply after task 20 and later tasks were written into the map afterwards.

**What it does not show:** six questions and one run per arm, so one question can swing the totals; the scorer knew which arm was which; the fact lists for three questions follow the map's own links, which favours it; no repeat runs; one project. Details in [`docs/results.md`](docs/results.md).

## Adding evidence
New data is welcome and the aim is to grow it:
1. Run the protocol in `docs/experiment-protocol.md` on a project of your own.
2. Put the scored rows in `data/experiments/<date>-<project>.json` (same shape as the existing file) and the per-task export in `data/telemetry/`.
3. Do not include raw agent answers, secrets or private project details.
Planned next: more questions on other repos with questions whose answers are not in commit messages, a human grader, repeats of the second-repo runs, and a task-level comparison of rounds and rework with versus without a map lookup first.

## License
MIT, see `LICENSE`.

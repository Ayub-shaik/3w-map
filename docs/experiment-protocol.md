# Protocol: the same question with and without the map

**Goal:** see whether the map changes accuracy or cost of recovering project history.

## Setup
1. Pick 6+ questions about your project whose answers are checkable. Mix: lineage of a fix, history of a rule, release state, reverse dependency ("what exists because of rule X"), open list, and one plain code lookup as a control.
2. For each, write a **fact list** *before running anything* and keep it **outside the repo** (an agent that finds it will read the answers). Score: +1 per fact found with a correct source, 0 missing, -1 wrong or invented.
3. Prepare two prompts per question, identical except for the rules block.
   - Arm A: may use git, grep, repo files, and your session notes. Must not read `.claude/map/` or run `pmap`.
   - Arm B: same, plus told to start with `pmap find / why / effects / open`.
   Both: read-only, no memory tools, "one tool call per turn", "do not call SubagentHandback", final report as plain text (max 10 lines, a source per fact, 'not found' instead of guessing).
4. Run each arm in a **fresh agent with no shared context**, same model. Run the two arms of a question at the same time if you can.

## Measure
`bin/agent-usage <agentId>` prints rounds, tool calls, tokens and wall time from the agent's transcript. Use **context growth** (last round's input minus the first round's) as the "how much did it read" number; raw fresh-input is dominated by the cold-start prompt and cache luck.

## Pitfalls we hit
- Some runs returned a literal "placeholder" report because the agent called its hand-back tool in the same turn as its last command. Fix: one tool call per turn, no hand-back tool, report as final text. Re-run and say so.
- One arm A agent found the experiment plan inside the repo. Keep plans and fact lists out of the tree.
- If fact lists follow the map's own links, the map is favoured. Say so, or add questions whose answers live only in git or docs.
- One run per arm is noisy. Repeat 3 times and have a second scorer who does not know the arm.

## Record
Add the rows to `data/experiments/<date>-<project>.json` (see the existing file) and a short entry in `docs/results.md`.

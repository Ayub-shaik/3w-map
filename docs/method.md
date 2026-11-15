# Method

## Node model
Stored in `<repo>/.claude/map/nodes.jsonl`, one JSON object per line, tracked by git.
- **goal** (`G-*`): why the project exists, in a sentence.
- **driver** (`R-*`): a rule, spec, brief or owner review that *demands* something. This is the "who".
- **decision** (`<PREFIX>-NNN`): a piece of work or a choice. Fields: `title`, `status` (`open` / `doing` / `done` / `unverified` / `superseded`), `why`, `serves` (goals), `required_by` (drivers), `triggered_by` (earlier decisions or events: the "when"), `supersedes`, `area`, `links` (`commits`, `files`, `docs`), `verified`, `date`.
Links point **up only**. Effects (what depends on a node) are never stored; `pmap effects <id>` computes them by reversing links, so they cannot go stale.

## Rules the tool enforces
- `done` needs `--commit <hash>` (must exist in the repo) and `--verified "<what you ran and saw>"`.
- `check` reports gaps such as decisions with no driver or no proof, and "why" fields that are only a wish.

## Per-task routine for the agent
1. `pmap <repo> task "<title>" --effort low|medium|high` (starts the measured window).
2. Before touching code: `find` / `why` / `open` for related decisions. Do not re-derive what is recorded.
3. New decision? `add` it linked to a goal, a driver and the decision that triggered it.
4. After the work: `done` with commit and proof, or leave it `open` with the reason.
5. `snap` after each task (optionally exports the report feed, see `PMAP_EXPORT_OUT`).

## Metrics
`pmap <repo> report` joins, per task: wall time (to the next task's start, so it includes waiting for the human), model rounds, fresh input (input + cache-written tokens), cache-read tokens, output and thinking tokens, and the share spent on map calls. Tokens come from the agent's session transcript, de-duplicated by message id.
`pmap-export` adds, per task, commits and files changed in that time window, which of the map commands were used, and a verdict (`yes` / `neutral` / `no`) from a notes file written by the agent: *did the map prevent rework, expose a gap, or answer without reading files?* That verdict is a judgement, not a measurement.
Complexity score on the report = 2 × effort level (low 1, medium 2, high 3) + 0.5 per file changed (max 4).

## Known caveats
- Fresh-input spikes after long idle gaps are cache rebuilds, not harder work.
- Effort for early tasks was guessed.
- Wall time includes waiting for the owner.

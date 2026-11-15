## 3W decision map (paste into CLAUDE.md or OPERATING.md)
This repo keeps a decision map in `.claude/map/nodes.jsonl`. Use `pmap` (see the 3w-map repo).
- Before work: `pmap . find <words>`, `pmap . why <id>`, `pmap . open`. Do not re-derive recorded decisions.
- Start each task with `pmap . task "<title>" --effort low|medium|high`.
- New decision: `pmap . add '<json>'` linked to a goal (`serves`), a driver (`required_by`) and the decision that caused it (`triggered_by`).
- Close with `pmap . done <id> --commit <hash> --verified "<what you ran and saw>"`. No proof, no done.
- After each task: `pmap . snap "<note>"`. Run `pmap . check` before ending a session.
- Never record secrets in nodes.

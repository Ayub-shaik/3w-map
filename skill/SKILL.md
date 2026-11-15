---
name: decision-map
description: Keep and consult a per-repo 3W decision map (why / who / when) with pmap. Use when starting a task in a repo that has .claude/map/nodes.jsonl, when asked why something exists, what depends on a rule, or what is still open, and when closing work that needs a commit and proof.
---
# Decision map (3W)
Draft skill, not yet published. See the repository README for status and evidence.

1. If `.claude/map/nodes.jsonl` exists, run `pmap . open` and `pmap . find <words>` before reading code for history or intent.
2. Questions of the form "why does X exist / who asked / what depends on it": `pmap . why <id>`, `pmap . effects <id>`. Verify against git only where the map is silent.
3. Start measured work with `pmap . task "<title>" --effort <level>`.
4. Record new decisions with `pmap . add` (links up only: serves, required_by, triggered_by).
5. Close with `pmap . done <id> --commit <hash> --verified "<proof>"`. Leave open with the reason if unproven.
6. End of task: `pmap . snap "<note>"`; end of session: `pmap . check`.
Never put secrets in nodes.

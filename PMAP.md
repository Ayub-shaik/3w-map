# PMAP: the rulebook (read this first, it is short)

`pmap` keeps a small decision map for a repo: **why** something was done, **who** required it, **when** (what caused it). Any assistant (Claude, Codex, others) can use it. These five rules are the whole rulebook.

1. **Record a node only if it changes this repo's code or plan, or is pending for it.** A tiny fix needs a node only if someone later asking "why is it like this?" would need the answer; otherwise the commit message is enough.
2. **Link to what really caused it.**
   - `triggered_by` is always required: the real cause (the "when"). Never the task you happen to be doing unless it truly caused this.
   - `serves` is a goal. Inherit the trigger's goal unless the change clearly belongs to another.
   - `required_by` only when a driver exists (a rule, spec or owner brief).
3. **If nothing in this repo changes because of it, do not record it.** A tool or repo you investigated and rejected is not recorded anywhere. Unrelated work stays out of this repo's map.
4. **A good idea with no fitting branch** becomes a pending node (`"status":"open"`) under the right goal.
5. **Look before you add:** `pmap <repo> find <words>`; `pmap <repo> open` lists pending items.

## Commands you need

```bash
pmap <repo> find <words>          # is it already there?
pmap <repo> why <id>              # why / who / when for a node
pmap <repo> open                  # pending items
pmap <repo> add '{"title":"...","why":"...","serves":["G-X"],"triggered_by":["ID"],"status":"open"}'
pmap <repo> done <id> --commit <hash> --verified "how you checked"
pmap <repo> check                 # links resolve, new nodes have a trigger and a goal
```

`add` refuses a decision with no title, why, goal or trigger, or with an unknown id, and prints rule 2.

## Example

While fixing a button shade you learn a database pooler might help. That idea was not caused by the button work. If it is worth doing, add a pending node under the data goal, triggered by whatever really prompted it. If you looked and it is not useful, record nothing.

## Proof is per repo

Telemetry is read per repo and per task family, never pooled across repos. The first mapping of a repo is a one-time setup cost, shown separately. Nodes created before these rules are grandfathered: `check` counts them but only lists newer ones (`PMAP_STRICT_FROM`, default 2026-11-15).

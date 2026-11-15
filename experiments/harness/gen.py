import json, random, secrets, os
S = "/tmp/claude-1000/-home-shaik-Desktop/7f8920f8-a5fc-4996-95de-9ef3946f7273/scratchpad/exp2"
spec = json.load(open("spec.json"))
PM = "/home/shaik/.claude/scripts/pmap"
runs = []
random.seed(20261115)
for q in spec:
    reps = 2 if q["repo"] == "bstudio" else 1
    for arm in "AB":
        for rep in range(reps):
            runs.append(dict(rid=secrets.token_hex(4), q=q["id"], repo=q["repo"], arm=arm, rep=rep + 1))
random.shuffle(runs)
for r in runs:
    q = next(x for x in spec if x["id"] == r["q"])
    path = f"/home/shaik/Desktop/projects/{r['repo']}"
    if r["arm"] == "A":
        rules = "You may use git log, grep, and read files in the repo (docs/, source, CHANGELOG) and, for bstudio only, grep ~/.claude/workspace/session-ledger.md. Do NOT read anything under .claude/map/ or .claude/OPERATING.md, do NOT run `pmap`, do NOT use Mnemosyne/memory tools."
    else:
        rules = f"Start with the project's 3W decision map: run `{PM} {r['repo']} find <words>`, `{PM} {r['repo']} why <id>`, `{PM} {r['repo']} effects <id>` or `{PM} {r['repo']} open` (`{PM} {r['repo']}` with no command prints usage). Then, only where the map is not enough, use git log, grep and repo files and, for bstudio only, grep ~/.claude/workspace/session-ledger.md. Do NOT use Mnemosyne/memory tools."
    ans = f"{S}/answers/{r['rid']}.md"
    txt = f"""Answer one question about the project at {path} (READ-ONLY: edit nothing, deploy nothing, change no state; the only file you may create is your answer file below).

QUESTION: {q['text']}

RULES: {rules}

HOW TO WORK: make ONE tool call per turn and read its result before the next call. Do NOT call SubagentHandback at all.

REPORT (max 10 lines): the answer as short bullets; for each fact give its source (file:line, commit hash or command). If you cannot establish a fact write 'not found'; do not guess. Last line: 'METHOD: <your first 3 tool calls>'.
Write the report with the Write tool to {ans}, then reply with exactly the word DONE.
"""
    open(f"{S}/prompts/{r['rid']}.txt", "w").write(txt)
json.dump(runs, open("runs.json", "w"), indent=1)
print(len(runs), "runs;", sum(r["repo"] == "bstudio" for r in runs), "bstudio,", sum(r["repo"] != "bstudio" for r in runs), "tomorrowtools")
print([ (r["rid"],r["q"],r["arm"]) for r in runs][:6])

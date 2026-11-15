import json, glob, os, re, subprocess, statistics, collections
S = "/tmp/claude-1000/-home-shaik-Desktop/7f8920f8-a5fc-4996-95de-9ef3946f7273/scratchpad/exp2"
spec = {q["id"]: q for q in json.load(open("spec.json"))}
runs = {r["rid"]: r for r in json.load(open("runs.json"))}
sc = {k: json.load(open(f"{S}/scores/{k}.json")) for k in ("R1", "R2") if os.path.exists(f"{S}/scores/{k}.json")}
# agent usage per run id via transcripts
use = {}
for f in glob.glob("/tmp/claude-1000/**/tasks/*.output", recursive=True):
    head = open(f).read(6000)
    m = re.search(r"prompts/([0-9a-f]{8})\.txt", head)
    if m and m.group(1) in runs:
        aid = os.path.basename(f)[:-7]
        use[m.group(1)] = json.loads(subprocess.run(["python3", os.path.expanduser("~/.claude/scripts/agent-usage.py"), aid], capture_output=True, text=True).stdout)
rows = []
for rid, r in runs.items():
    if any(rid not in sc[k] for k in sc): print("unscored", rid); continue
    q = spec[r["q"]]; mx = len(q["facts"])
    s = {k: sum(sc[k][rid]) for k in sc}
    u = use.get(rid, {})
    rows.append(dict(rid=rid, q=r["q"], repo=r["repo"], arm=r["arm"], rep=r["rep"], max=mx, **{f"score_{k}": v for k, v in s.items()},
                     wrong=sum(1 for k in sc for x in sc[k][rid] if x < 0) / len(sc),
                     tool_calls=u.get("tools"), rounds=u.get("rounds"), context_growth=u.get("growth"), out=u.get("out"), wall_s=u.get("wall_s")))
# agreement (per-fact)
agree = tot = 0
if len(sc) == 2:
    for rid in runs:
        for a, b in zip(sc["R1"][rid], sc["R2"][rid]): tot += 1; agree += (a == b)
def mean(xs): xs = [x for x in xs if x is not None]; return sum(xs) / len(xs) if xs else 0
out = dict(raters=list(sc), fact_agreement=round(agree / tot, 3) if tot else None, rows=rows, by_group={})
for repo in ("bstudio", "tomorrowtools"):
    for arm in "AB":
        g = [x for x in rows if x["repo"] == repo and x["arm"] == arm]
        sk = [k for k in sc]
        pct = {k: round(100 * sum(x[f"score_{k}"] for x in g) / sum(x["max"] for x in g), 1) for k in sk}
        out["by_group"][f"{repo}-{arm}"] = dict(n=len(g), pct=pct, tool_calls=round(mean(x["tool_calls"] for x in g), 1), rounds=round(mean(x["rounds"] for x in g), 1),
            context_growth=round(mean(x["context_growth"] for x in g)), wall_s=round(mean(x["wall_s"] for x in g), 1))
# per question
out["by_question"] = {}
for qid in spec:
    d = {}
    for arm in "AB":
        g = [x for x in rows if x["q"] == qid and x["arm"] == arm]
        if g: d[arm] = dict(n=len(g), pct=round(100 * sum(mean([x[f"score_{k}"] for k in sc]) for x in g) / sum(x["max"] for x in g), 1), growth=round(mean(x["context_growth"] for x in g)), calls=round(mean(x["tool_calls"] for x in g), 1))
    out["by_question"][qid] = d
json.dump(out, open("exp2-results.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("raters", "fact_agreement", "by_group")}, indent=1))
for q, d in out["by_question"].items(): print(q, d)

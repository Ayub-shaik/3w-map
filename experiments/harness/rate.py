import json, re, random, os
S = "/tmp/claude-1000/-home-shaik-Desktop/7f8920f8-a5fc-4996-95de-9ef3946f7273/scratchpad/exp2"
spec = {q["id"]: q for q in json.load(open("spec.json"))}
runs = json.load(open("runs.json"))
def clean(t):
    t = re.sub(r"(?im)^.*METHOD:.*$", "", t)
    t = re.sub(r"`?(/home/shaik/\.claude/scripts/)?pmap (bstudio|tomorrowtools)[^`;\n)]*`?", "[command]", t)
    t = re.sub(r"(?i)\b(the )?(3w )?(decision )?map\b", "[source]", t)
    t = re.sub(r"(?i)\bpmap\b", "[tool]", t)
    return t.strip()
missing = [r["rid"] for r in runs if not os.path.exists(f"{S}/answers/{r['rid']}.md")]
print("missing answers:", missing)
for rater, seed in (("R1", 1), ("R2", 2)):
    rr = runs[:]; random.Random(seed).shuffle(rr)
    out = ["You are a strict, independent grader. For each ANSWER below, score it against the numbered FACTS for its question.",
           "Per fact: 1 = the answer states it (or an equivalent) with some source or evidence; 0 = missing or too vague to count; -1 = the answer contradicts it or states something wrong about it. Judge only from the text given; do not use tools except to write your result file.",
           "Do not guess which method produced an answer. Output a JSON object {\"<answer id>\": [score per fact in order], ...} and write it with the Write tool to " + f"{S}/scores/{rater}.json" + ", then reply with exactly DONE.", ""]
    for q in spec.values():
        grp = [r for r in rr if r["q"] == q["id"] and os.path.exists(f"{S}/answers/{r['rid']}.md")]
        if not grp: continue
        out.append(f"=== QUESTION {q['id']}: {q['text']}")
        out += [f"FACT {i+1}: {f}" for i, f in enumerate(q["facts"])]
        for r in grp:
            out.append(f"--- ANSWER {r['rid']}\n{clean(open(S+'/answers/'+r['rid']+'.md').read())}")
        out.append("")
    open(f"{S}/prompts/rater-{rater}.txt", "w").write("\n".join(out))
    print(rater, len("\n".join(out)), "chars")

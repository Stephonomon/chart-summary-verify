"""Cost and speed: Jev vs Claude doing the same verification. -> bench.json
Jev:    the 40 calls in verify.py (21 citation checks + 19 whole-chart checks), 8 in parallel.
Claude: ONE call per model with the whole chart and every citation, structured output with a verdict per citation
        and a whole-chart verdict per sentence (the cheapest realistic way to use an LLM for this job).
Each arm runs RUNS times; latency is the median. Accuracy = errors caught (any non-green citation on a planted
sentence) and false flags (non-green citations on accurate sentences)."""
import json, time, statistics, concurrent.futures as cf, anthropic
from data import CHART
from verify import CRITERIA, check_citation, check_chart

RUNS = 3
PRICE = {"jev-1.13.0": (0.042, 0.0), "claude-opus-5-5": (4, 20), "claude-sonnet-5": (2, 10), "claude-haiku-4-5": (1, 5)}  # USD / 1M tokens (in, out)
R = json.load(open("results.json"))
SENTS = [s for p in R["summary"]["paragraphs"] for s in p]
CITES = R["citations"]
for i, c in enumerate(CITES): c["cid"] = f"C{i+1:02d}"
BY_S = {s["id"]: s for s in SENTS}
VERDICTS = list(CRITERIA)

def cost(model, tin, tout): pi, po = PRICE[model.split()[0]]; return (tin * pi + tout * po) / 1e6

# ---------- Jev: rerun the exact verify.py calls ----------
def run_jev():
    jobs = [(BY_S[c["sentence"]], c["doc"], c["passages"]) for c in CITES]
    t0 = time.time()
    with cf.ThreadPoolExecutor(8) as ex:
        cit = list(ex.map(check_citation, jobs)); ch = list(ex.map(check_chart, SENTS))
    wall = time.time() - t0
    tin = sum(x["usage"]["input_tokens"] for x in cit + ch); tout = sum(x["usage"]["output_tokens"] for x in cit + ch)
    return {"latency_s": wall, "tin": tin, "tout": tout, "calls": len(cit) + len(ch),
            "cite": {c["cid"]: x["verdict"] for c, x in zip(CITES, cit)}, "chart": {x["sentence"]: x["verdict"] for x in ch}}

# ---------- Jev fan-out: the chart sent once, all 40 questions in one request ----------
from verify import jev, CITE_Q, CHART_Q
from data import BY_ID
def run_jev_fanout():
    qs = {}
    for c in CITES:
        s = BY_S[c["sentence"]]; d = BY_ID[c["doc"]]
        qs[c["cid"]] = {**CITE_Q, "instructions": f"Claim: \"{s['text']}\" It cites document [{d['id']}] ({d['kind']}: {d['title']}, {d['date']}). "
                        f"Judge the claim ONLY against document [{d['id']}] in the `chart`, ignoring every other document, and not against clinical plausibility. "
                        "Parts of the claim that this document does not address make it `ambiguous` at best."}
    for s in SENTS:
        qs[s["id"]] = {**CHART_Q, "instructions": f"Claim: \"{s['text']}\" " + CHART_Q["instructions"].replace("The `claim` is", "This claim is")}
    t0 = time.time(); r = jev({"chart": CHART}, qs); wall = time.time() - t0
    a = r["answers"]
    return {"latency_s": wall, "tin": r["usage"]["input_tokens"], "tout": r["usage"]["output_tokens"], "calls": 1,
            "cite": {c["cid"]: a[c["cid"]]["choice"] for c in CITES}, "chart": {s["id"]: a[s["id"]]["choice"] for s in SENTS}}

# ---------- Claude: one structured call ----------
SYSTEM = ("You verify an AI-generated chart-review summary against the patient's chart. Return one entry for every CITATION ID and every SENTENCE ID. For each CITATION, judge the sentence ONLY against "
          "the cited document (not clinical plausibility, not other documents). For each SENTENCE, judge it against the whole chart and name the "
          "single best evidence passage ID (or \"none\"). Verdicts:\n" +
          "\n".join(f"- {k}: {v['what']}" + (f" (not for: {v['not_for']})" if "not_for" in v else "") for k, v in CRITERIA.items()))
_V = {"type": "string", "enum": VERDICTS}
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["citations", "sentences"], "properties": {
  "citations": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["id", "verdict"],
                "properties": {"id": {"type": "string"}, "verdict": _V}}},
  "sentences": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["id", "verdict", "best_passage"],
                "properties": {"id": {"type": "string"}, "verdict": _V, "best_passage": {"type": "string"}}}}}}
TASK = ("SUMMARY SENTENCES\n" + "\n".join(f"{s['id']}: {s['text']}" for s in SENTS) +
        "\n\nCITATIONS TO CHECK (citation ID: sentence ID -> cited document [cited passages])\n" +
        "\n".join(f"{c['cid']}: {c['sentence']} -> {c['doc']} [{', '.join(c['passages'])}]" for c in CITES))
CL = anthropic.Anthropic()

def run_claude(model):
    kw = dict(model=model, max_tokens=16000, system=SYSTEM,
              messages=[{"role": "user", "content": f"CHART\n\n{CHART}\n\n{TASK}"}])
    fmt = {"format": {"type": "json_schema", "schema": SCHEMA}}
    if model != "claude-haiku-4-5": fmt["effort"] = "low"
    t0 = time.time(); r = CL.messages.create(**kw, output_config=fmt); wall = time.time() - t0
    d = json.loads(next(b.text for b in r.content if b.type == "text"))
    cite = {x["id"]: x["verdict"] for x in d["citations"]}; chart = {x["id"]: x["verdict"] for x in d["sentences"]}
    missing = [c["cid"] for c in CITES if c["cid"] not in cite] + [x["id"] for x in SENTS if x["id"] not in chart]
    if missing: raise RuntimeError(f"{model} skipped {missing}")
    return {"latency_s": wall, "tin": r.usage.input_tokens, "tout": r.usage.output_tokens, "calls": 1, "cite": cite, "chart": chart}

def score(run):
    flagged = lambda s: any(run["cite"][c["cid"]] != "supported" for c in CITES if c["sentence"] == s["id"])
    errs = [s for s in SENTS if s["seed"] != "supported"]; clean = [s for s in SENTS if s["seed"] == "supported"]
    return {"caught": sum(flagged(s) for s in errs), "errors": len(errs),
            "false_flag_sentences": [s["id"] for s in clean if flagged(s)],
            "misciting_found": run["chart"]["S14"] == "supported"}   # true fact, wrong source: whole chart should say supported

if __name__ == "__main__":
    out = {}
    arms = [("jev-1.13.0", run_jev), ("jev-1.13.0 fan-out", run_jev_fanout)] + [(m, lambda m=m: run_claude(m)) for m in ("claude-opus-5-5", "claude-sonnet-5", "claude-haiku-4-5")]
    for name, fn in arms:
        runs = [fn() for _ in range(RUNS)]
        lat = [r["latency_s"] for r in runs]; sc = [score(r) for r in runs]
        tin = statistics.mean(r["tin"] for r in runs); tout = statistics.mean(r["tout"] for r in runs)
        ref = runs[0]["cite"]
        out[name] = {"calls": runs[0]["calls"], "latency_median_s": round(statistics.median(lat), 2), "latency_runs": [round(x, 2) for x in lat],
                     "input_tokens": round(tin), "output_tokens": round(tout), "cost_usd": round(cost(name, tin, tout), 5),
                     "scores": sc, "stable_citation_verdicts": all(r["cite"] == ref for r in runs),
                     "citation_verdicts_run1": runs[0]["cite"], "chart_verdicts_run1": runs[0]["chart"]}
        o = out[name]; s0 = sc[0]
        print(f"{name:18} {o['calls']:2} calls  median {o['latency_median_s']:5.1f}s {o['latency_runs']}  {o['input_tokens']:>7} in {o['output_tokens']:>6} out  "
              f"${o['cost_usd']:.4f}  caught {[s['caught'] for s in sc]}/6  false flags {[len(s['false_flag_sentences']) for s in sc]} {s0['false_flag_sentences']}  "
              f"miscite {[s['misciting_found'] for s in sc]}  stable {o['stable_citation_verdicts']}")
    print("\nper-citation verdicts (run 1), planted sentences marked *")
    for c in CITES:
        s_ = BY_S[c["sentence"]]
        print(f"  {c['cid']} {c['sentence']}{'*' if s_['seed'] != 'supported' else ' '} {c['doc']:3} " + "  ".join(f"{out[n]['citation_verdicts_run1'][c['cid']][:6]:6}" for n in out))
    json.dump({"run_at": time.strftime("%Y-%m-%d %H:%M"), "runs": RUNS, "price_per_mtok": PRICE, "arms": out}, open("bench.json", "w"), indent=1)

"""Step 3: Jev checks every citation in summary.json. -> results.json
Citation check  (one call per sentence x cited document): does THIS source support the sentence? + which passage in it is the evidence?
Chart check     (one call per sentence): does ANYTHING in the chart support it? + which passage is the best evidence?
The citation check colours the superscript; the chart check tells a mis-citation (true, wrong source) from a fabrication."""
import json, os, sys, time, urllib.request, concurrent.futures as cf
from data import SOURCES, BY_ID, CHART, PATIENT, render

URL, MODEL = "https://api.typesafe.ai/v1/systemone", "jev-1.13.0"
def _key():
    k = os.environ.get("TYPESAFE_API_KEY")
    if k: return k.strip()
    p = os.path.expanduser("~/.typesafe_api_key")
    if os.path.exists(p): return open(p).read().strip()
    sys.exit("Set TYPESAFE_API_KEY or put your key in ~/.typesafe_api_key (get one at https://console.typesafe.ai)")
KEY = _key()

def jev(state, questions):
    body = json.dumps({"model": MODEL, "state": state, "questions": questions}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "User-Agent": "chart-summary-verify/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)
        except Exception:
            if attempt == 2: raise
            time.sleep(2)

CRITERIA = {
  "supported":    {"what": "The source states everything the claim asserts, or directly implies it, even in different words"},
  "contradicted": {"what": "The source says something that makes the claim false: a different value, dose, date, or person; denies what the claim asserts; "
                           "or the claim turns something conditional, planned, or hypothetical in the source (an instruction for what to do if something happens, "
                           "a plan to consider a change) into something that actually happened"},
  "not_found":    {"what": "The source does not address what the claim asserts; the content would have to have come from somewhere else",
                   "not_for": "Claims the source does address but only partially (that is `ambiguous`)"},
  "ambiguous":    {"what": "The source addresses the claim but supports only part of it, or the evidence is hedged or mixed, so a clinician should look before relying on it"}}
CITE_Q = {"type": "choice", "criteria": CRITERIA, "instructions":
  "The `claim` is one sentence from an AI-generated chart-review summary, and it cites the `source` document. Judge the claim only against this source, "
  "not against clinical plausibility or other parts of the chart. Parts of the claim that this source does not address make it `ambiguous` at best."}
CHART_Q = {"type": "choice", "criteria": CRITERIA, "instructions":
  "The `claim` is one sentence from an AI-generated chart-review summary. Judge it against the whole `chart` (notes, labs, imaging, medications, problem list)."}

def passage_q(segs, scope):
    crit = {g["id"]: {"what": f"Passage {g['id']} ({g['section']}) is the primary evidence for or against the claim"} for g in segs}
    crit["none"] = {"what": f"No passage in the {scope} addresses the claim"}
    return {"type": "choice", "criteria": crit, "instructions": f"Which single passage in the {scope} (by its [ID] tag) is the primary evidence for or against the `claim`?"}

def top(probs, k=3): return [[a, round(p, 3)] for a, p in sorted(probs.items(), key=lambda kv: -kv[1])[:k] if p > 0.04]

def check_citation(job):
    s, doc_id, passages = job; doc = BY_ID[doc_id]; t0 = time.time()
    r = jev({"source": render(doc), "claim": s["text"]}, {"support": CITE_Q, "passage": passage_q(doc["segments"], "source")})
    a, p = r["answers"]["support"], r["answers"]["passage"]
    return {"sentence": s["id"], "doc": doc_id, "passages": passages,
            "verdict": a["choice"], "confidence": round(a["probabilities"][a["choice"]], 3), "probs": {k: round(v, 3) for k, v in a["probabilities"].items()},
            "jev_passage": p["choice"], "jev_passage_conf": round(p["probabilities"][p["choice"]], 3),
            "cited_passage_prob": round(sum(p["probabilities"].get(x, 0) for x in passages), 3), "passage_alts": top(p["probabilities"]),
            "usage": r["usage"], "latency_s": round(time.time() - t0, 2)}

ALL_SEGS = [g for src in SOURCES for g in src["segments"]]
def check_chart(s):
    t0 = time.time()
    r = jev({"chart": CHART, "claim": s["text"]}, {"support": CHART_Q, "best": passage_q(ALL_SEGS, "chart")})
    a, b = r["answers"]["support"], r["answers"]["best"]
    return {"sentence": s["id"], "verdict": a["choice"], "confidence": round(a["probabilities"][a["choice"]], 3),
            "probs": {k: round(v, 3) for k, v in a["probabilities"].items()},
            "best": b["choice"], "best_conf": round(b["probabilities"][b["choice"]], 3), "best_alts": top(b["probabilities"]),
            "usage": r["usage"], "latency_s": round(time.time() - t0, 2)}

if __name__ == "__main__":
    summ = json.load(open("summary.json")); sents = [s for p in summ["paragraphs"] for s in p]
    jobs = []
    for s in sents:
        by_doc = {}
        for c in s["cites"]: by_doc.setdefault(c.split(".")[0], []).append(c)
        jobs += [(s, d, ps) for d, ps in by_doc.items()]
    t0 = time.time()
    with cf.ThreadPoolExecutor(8) as ex:
        cites = list(ex.map(check_citation, jobs)); chart = list(ex.map(check_chart, sents))
    allr = cites + chart
    tin, tout = sum(x["usage"]["input_tokens"] for x in allr), sum(x["usage"]["output_tokens"] for x in allr)
    out = {"patient": PATIENT, "jev_model": MODEL, "run_at": time.strftime("%Y-%m-%d %H:%M"), "wall_s": round(time.time() - t0, 1),
           "calls": len(allr), "input_tokens": tin, "output_tokens": tout, "summary": summ, "citations": cites, "chart": chart}
    json.dump(out, open("results.json", "w"), indent=1)
    print(f"{len(allr)} calls, {out['wall_s']}s wall, {tin} in / {tout} out tokens\n")
    cm = {c["sentence"]: c for c in chart}
    for s in sents:
        cs = [c for c in cites if c["sentence"] == s["id"]]; ch = cm[s["id"]]
        print(f"{s['id']} seed={s['seed']:12} chart={ch['verdict']:12}{ch['confidence']:.2f} best={ch['best']:6} | {s['text'][:70]}")
        for c in cs: print(f"      {c['doc']:3} {c['verdict']:12} {c['confidence']:.2f}  passage={c['jev_passage']}({c['jev_passage_conf']:.2f}) cited={c['passages']} p={c['cited_passage_prob']:.2f}")

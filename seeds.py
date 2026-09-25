"""Step 2: plant known errors in Claude's frozen summary so the demo has ground truth. -> summary.json
Claude's own output (summary_claude.json) was accurate; every error below was written by hand.
`seed` is what a careful reviewer would say about the sentence against the source(s) it cites."""
import json

EDITS = {
  # (paragraph, sentence): replacement
  (0, 2): {"text": "Family history is notable for bipolar I disorder in her father, with no known family history of suicide.",
           "cites": ["N1.11", "N1.12"], "seed": "contradicted", "kind": "Misattribution (the aunt's diagnosis given to the father)"},
  (1, 4): {"text": "Two days later she returned to the ED with a fever and a rapidly spreading rash, and lamotrigine was permanently discontinued and added to her allergy list.",
           "cites": ["N3.15", "N4.3"], "seed": "contradicted", "kind": "Confabulation (a return precaution turned into an event)"},
  (2, 2): {"text": "Her suicidal ideation has resolved, and she denies self-harm since February.",
           "cites": ["N6.3", "N6.4"], "seed": "contradicted", "kind": "Overstatement (passive SI a couple of times this month)"},
  (2, 4): {"text": "Her mother has confirmed there are no firearms in the home and that medications are kept in a locked box.",
           "cites": ["N5.6"], "seed": "not_found", "kind": "Mis-citation (true, but the therapy note doesn't say it; N1.9 does)"},
  (3, 2): {"text": "Sertraline was increased to 100 mg daily at the September visit, and guanfacine ER 2 mg and melatonin 3 mg nightly continue.",
           "cites": ["N6.10", "M1.1"], "seed": "contradicted", "kind": "Plan stated as done (100 mg was only to be considered)"},
}
INSERTS = {
  # insert before (paragraph, sentence)
  (0, 1): {"text": "She had an inpatient psychiatric admission for suicidal ideation in December 2025.",
           "cites": ["P1.1"], "seed": "not_found", "kind": "Fabrication (no admission anywhere in the chart)"},
  (3, 1): {"text": "A February 2026 right-hand X-ray after she punched a wall showed no fracture, only soft-tissue swelling over the fifth knuckle.",
           "cites": ["R1.4", "R1.6"], "seed": "supported", "kind": "Added accurate sentence (so imaging is represented)"},
}

if __name__ == "__main__":
    src = json.load(open("summary_claude.json"))
    paras, n = [], 0
    for pi, p in enumerate(src["paragraphs"]):
        out = []
        for si, s in enumerate(p):
            if (pi, si) in INSERTS: out.append({**INSERTS[(pi, si)], "origin": "inserted"})
            if (pi, si) in EDITS: out.append({**EDITS[(pi, si)], "origin": "edited", "claude_text": s["text"], "claude_cites": s["cites"]})
            else: out.append({**s, "seed": "supported", "kind": "", "origin": "claude"})
        paras.append(out)
    for p in paras:
        for s in p: n += 1; s["id"] = f"S{n:02d}"
    json.dump({"model": src["model"], "usage": src["usage"], "latency_s": src["latency_s"], "paragraphs": paras}, open("summary.json", "w"), indent=1)
    for p in paras:
        for s in p: print(f"{s['id']} {s['origin']:8} {s['seed']:12} {s['text'][:90]}  {s['cites']}")

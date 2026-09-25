"""Step 1: Claude writes the narrative chart-review summary, citing chart passages by segment ID. -> summary_claude.json
Run once; the output is frozen so the seeded errors in seeds.py always land on the same sentences."""
import json, time, anthropic
from data import CHART, SOURCES, PATIENT, TODAY

MODEL = "claude-opus-5-5"
SEG_IDS = [g["id"] for s in SOURCES for g in s["segments"]]
SYSTEM = ("You write the narrative chart-review summary that appears in an EHR sidebar for a clinician about to see a pediatric "
          "behavioral-health patient. Write 3 or 4 short paragraphs of plain clinical prose (no bullets, no headings): "
          "(1) who the patient is and the active diagnoses; (2) the psychiatric course and treatment changes over the past few months, "
          "including any adverse events; (3) current status, risk, and safety; (4) pertinent labs/imaging and the current plan. "
          "Every sentence must cite 1 or 2 chart passages by their segment ID (e.g. N3.7) that directly support it. "
          "Only state what the chart supports. 14 to 20 sentences total.")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["paragraphs"], "properties": {
  "paragraphs": {"type": "array", "items": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["text", "cites"], "properties": {
    "text": {"type": "string"}, "cites": {"type": "array", "items": {"type": "string", "enum": SEG_IDS}}}}}}}}

if __name__ == "__main__":
    t0 = time.time()
    r = anthropic.Anthropic().messages.create(model=MODEL, max_tokens=4000, system=SYSTEM,
        messages=[{"role": "user", "content": f"Patient: {PATIENT['name']}, {PATIENT['age']} {PATIENT['sex']}. Today is {TODAY}.\n\nCHART\n\n{CHART}"}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
    d = json.loads(next(b.text for b in r.content if b.type == "text"))
    out = {"model": MODEL, "run_at": time.strftime("%Y-%m-%d %H:%M"), "latency_s": round(time.time() - t0, 1),
           "usage": {"input": r.usage.input_tokens, "output": r.usage.output_tokens}, "paragraphs": d["paragraphs"]}
    json.dump(out, open("summary_claude.json", "w"), indent=1)
    for p in d["paragraphs"]:
        for s in p: print(f"  {s['text']}  {s['cites']}")
        print()
    print(out["usage"], out["latency_s"], "s")

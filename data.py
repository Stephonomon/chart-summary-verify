"""Fabricated pediatric psychiatry chart. No real patient, clinician, or organization.
Every source is split into short segments with stable IDs (N3.7, L1.4, ...) so a citation can point at a passage,
not just a document."""

PATIENT = {
    "name": "Avery Delgado", "sex": "F", "dob": "03/14/2011", "age": "15 y.o.", "mrn": "E4821705",
    "pcp": "Priya Raman, MD", "psychiatrist": "Dana Whitfield, MD", "therapist": "Marcus Lee, LCSW",
    "allergies": ["Lamotrigine (rash)"], "coverage": "Keystone Kids Health Plan", "code": "Full Code",
    "weight": "58.4 kg (09/16/26)", "height": "163 cm", "language": "English", "guardian": "Elena Delgado (mother)",
}
TODAY = "09/24/2026"

# ---------- Progress notes: (section, [sentences]) ----------
NOTES = [
  {"id": "N1", "kind": "Progress Note", "title": "Psychiatry Med Management", "date": "06/10/2026", "author": "Dana Whitfield, MD", "dept": "Child & Adolescent Psychiatry",
   "body": [
    ("Interval History", [
      "Avery is a 15-year-old with major depressive disorder, generalized anxiety disorder, and ADHD, seen with her mother for medication follow-up.",
      "Since the last visit she reports persistent low mood, irritability, and frequent crying spells, with the irritability worse in the evenings.",
      "She has missed about two school days per week over the past month because of low mood and morning anxiety.",
      "She endorses passive suicidal ideation about once a week (\"wishing I could just disappear\") without plan or intent.",
      "Her last episode of nonsuicidal self-injury (superficial cutting of the forearm) was in February 2026; she denies any since.",
      "She tolerates sertraline 50 mg daily without GI upset or activation."]),
    ("Measures", ["PHQ-A 16 (moderately severe). GAD-7 13 (moderate).", "C-SSRS screen: passive ideation only; no active ideation, plan, intent, or behavior in the past month."]),
    ("Safety", ["Mother confirms there are no firearms in the home and that medications are kept in a locked box.", "Safety plan reviewed and updated with Avery and her mother."]),
    ("Family History", ["Mother reports a maternal aunt with bipolar I disorder.", "Father has ADHD. No known family history of suicide."]),
    ("Assessment & Plan", [
      "Depression remains moderately severe with partial response to sertraline.",
      "Increase sertraline from 50 mg to 75 mg daily.",
      "If mood lability persists at the next visit, will consider adding lamotrigine.",
      "Continue guanfacine ER 2 mg nightly for ADHD.",
      "Continue weekly individual therapy with Marcus Lee, LCSW. Return in 2 weeks."]),
   ]},
  {"id": "N2", "kind": "Progress Note", "title": "Psychiatry Med Management", "date": "06/24/2026", "author": "Dana Whitfield, MD", "dept": "Child & Adolescent Psychiatry",
   "body": [
    ("Interval History", [
      "Two weeks after the sertraline increase to 75 mg, Avery reports slightly better mornings but continued evening irritability and rapid shifts in mood.",
      "Mother describes several explosive arguments at home over the past two weeks; no physical aggression.",
      "Avery also reports fatigue and low energy despite sleeping 9 to 10 hours."]),
    ("Measures", ["PHQ-A 14. GAD-7 12."]),
    ("Assessment & Plan", [
      "Given persistent mood lability and the family history of bipolar disorder, will start lamotrigine as an adjunct (off-label).",
      "Start lamotrigine 25 mg daily for 2 weeks, then 50 mg daily, with slow titration per protocol.",
      "Counseled Avery and her mother on the risk of serious rash, including Stevens-Johnson syndrome, and to stop the medication and seek care for any rash.",
      "Ordered CBC, CMP, TSH with free T4, ferritin, and 25-OH vitamin D to evaluate fatigue.",
      "Continue sertraline 75 mg daily and guanfacine ER 2 mg nightly. Return in 3 weeks."]),
   ]},
  {"id": "N3", "kind": "ED Provider Note", "title": "Pediatric Emergency Department Visit", "date": "07/09/2026", "author": "Samuel Okoye, MD", "dept": "Pediatric Emergency Medicine",
   "body": [
    ("Chief Complaint", ["Rash for 1 day."]),
    ("HPI", [
      "15-year-old female on day 15 of lamotrigine 25 mg daily presents with a pruritic rash that started on her chest yesterday and spread to her back and upper arms.",
      "She denies fever, sore throat, mouth sores, eye pain or redness, and blistering.",
      "Mother stopped the lamotrigine this morning after calling the psychiatry office."]),
    ("Exam", [
      "Temp 37.0 °C, HR 88, BP 112/68, RR 16, SpO2 99% on room air.",
      "Skin: blanching erythematous maculopapular rash over the chest, back, and proximal arms; no vesicles, bullae, target lesions, or skin sloughing; Nikolsky sign negative.",
      "Oral mucosa and conjunctivae are normal."]),
    ("Medical Decision Making", [
      "Presentation is most consistent with a benign morbilliform drug eruption from lamotrigine.",
      "There are no features of Stevens-Johnson syndrome or DRESS at this time: afebrile, no mucosal involvement, no blistering.",
      "CBC and liver enzymes were not indicated given the benign exam."]),
    ("Disposition", [
      "Discharged home in stable condition with her mother.",
      "Hold lamotrigine; do not restart unless directed by her psychiatrist.",
      "Cetirizine 10 mg daily for 7 days for itching.",
      "Follow up with psychiatry within 48 to 72 hours."]),
    ("Discharge Instructions", [
      "Return to the emergency department right away if she develops a fever, blisters, peeling skin, sores in the mouth or eyes, or if the rash spreads quickly.",
      "Keep taking sertraline and guanfacine as prescribed."]),
   ]},
  {"id": "N4", "kind": "Telephone Encounter", "title": "Psychiatry Follow-up Call", "date": "07/14/2026", "author": "Dana Whitfield, MD", "dept": "Child & Adolescent Psychiatry",
   "body": [
    ("Note", [
      "Spoke with Avery's mother by phone for ED follow-up.",
      "The rash is fading and nearly gone; no fever, blistering, or mouth sores at any point.",
      "Lamotrigine discontinued permanently and added to the allergy list; will not rechallenge.",
      "Mood is about the same as at the last visit; continue sertraline 75 mg daily.",
      "Will revisit mood-stabilizer options at the next in-person visit."]),
   ]},
  {"id": "N5", "kind": "Progress Note", "title": "Individual Therapy", "date": "08/19/2026", "author": "Marcus Lee, LCSW", "dept": "Behavioral Health",
   "body": [
    ("Session", [
      "Individual therapy session, 53 minutes, focused on DBT distress-tolerance skills ahead of the start of 10th grade.",
      "Avery reports one strong urge to self-harm after an argument with a friend last week; she used the TIPP skill (cold water) and did not act on it.",
      "She reports no self-harm since February.",
      "She identified returning to school and a group-chat conflict as her main current stressors.",
      "Practiced cognitive restructuring for catastrophic thoughts about school; she completed the between-session diary card on 5 of 7 days."]),
    ("Risk", ["Denies current suicidal ideation, plan, or intent today. Safety plan reviewed; no changes."]),
    ("Plan", ["Continue weekly individual therapy. Mother to join the last 10 minutes of next session to review the home behavior plan."]),
   ]},
  {"id": "N6", "kind": "Progress Note", "title": "Psychiatry Med Management", "date": "09/16/2026", "author": "Dana Whitfield, MD", "dept": "Child & Adolescent Psychiatry",
   "body": [
    ("Interval History", [
      "Avery returns with her mother; she started 10th grade three weeks ago and has attended full days without absences.",
      "Mood is improved; she describes evenings as \"less explosive\" and arguments at home are down to about one a week.",
      "She reports passive suicidal ideation a couple of times in the past month, fleeting, without plan or intent.",
      "She denies any self-harm since February.",
      "Sleep onset still takes about 45 minutes with melatonin 3 mg; she sleeps through the night.",
      "No side effects from sertraline or guanfacine."]),
    ("Measures", ["PHQ-A 9 (mild), improved from 16 in June. GAD-7 8 (mild).", "Weight 58.4 kg, up 2.1 kg since June."]),
    ("Assessment & Plan", [
      "Major depressive disorder, recurrent, moderate, now improving on sertraline; generalized anxiety improving.",
      "Continue sertraline 75 mg daily; will consider an increase to 100 mg at the next visit if improvement plateaus.",
      "Continue guanfacine ER 2 mg nightly and melatonin 3 mg at bedtime.",
      "Ferritin and vitamin D were low on June labs; start ferrous sulfate 325 mg every other day and vitamin D3 2,000 IU daily per PCP recommendation.",
      "No mood stabilizer for now given the improvement. Continue weekly therapy. Return in 4 weeks."]),
   ]},
]

# ---------- Labs ----------
LABS = [
  {"id": "L1", "kind": "Lab Result", "title": "Fatigue Panel", "date": "06/26/2026", "author": "Ordered by Dana Whitfield, MD", "dept": "Laboratory",
   "rows": [
    ("TSH", "2.1", "mIU/L", "0.5 – 4.3", ""), ("Free T4", "1.2", "ng/dL", "0.9 – 1.6", ""),
    ("Hemoglobin", "12.8", "g/dL", "12.0 – 15.5", ""), ("WBC", "6.4", "K/uL", "4.5 – 13.0", ""), ("Platelets", "268", "K/uL", "150 – 400", ""),
    ("Ferritin", "11", "ng/mL", "15 – 150", "L"), ("25-OH Vitamin D", "17", "ng/mL", "20 – 50", "L"),
    ("Sodium", "139", "mmol/L", "135 – 145", ""), ("Creatinine", "0.7", "mg/dL", "0.5 – 1.0", ""), ("ALT", "14", "U/L", "7 – 35", ""), ("Glucose", "88", "mg/dL", "70 – 99", "")]},
]

# ---------- Radiology ----------
RADS = [
  {"id": "R1", "kind": "Imaging", "title": "XR Hand Right, 3 Views", "date": "02/21/2026", "author": "Helen Kwan, MD (Radiology)", "dept": "Radiology",
   "body": [
    ("Indication", ["15-year-old female, punched a wall during an argument; pain and swelling over the right fifth knuckle."]),
    ("Findings", ["No acute fracture or dislocation.", "Soft-tissue swelling over the dorsal fifth metacarpophalangeal joint.", "Growth plates are open and normal in appearance."]),
    ("Impression", ["No fracture. Soft-tissue swelling of the right fifth MCP region."]),
   ]},
]

# ---------- Medications (current + recent) ----------
MEDS = {"id": "M1", "kind": "Medication List", "title": "Medications", "date": "09/16/2026", "author": "Reconciled by Dana Whitfield, MD", "dept": "Medications",
  "rows": [
    ("Sertraline 75 mg tablet", "1 tablet by mouth daily", "Active", "Started 12/2025 at 25 mg; 50 mg 01/2026; 75 mg since 06/10/2026"),
    ("Guanfacine ER 2 mg tablet", "1 tablet by mouth nightly", "Active", "Since 09/2024"),
    ("Melatonin 3 mg tablet (OTC)", "1 tablet by mouth at bedtime", "Active", "Since 03/2026"),
    ("Hydroxyzine HCl 25 mg tablet", "1 tablet by mouth every 8 hours as needed for anxiety", "Active", "Since 03/2026; mother reports use about once a week"),
    ("Ferrous sulfate 325 mg tablet", "1 tablet by mouth every other day", "Active", "Started 09/16/2026"),
    ("Cholecalciferol (vitamin D3) 2,000 IU", "1 capsule by mouth daily", "Active", "Started 09/16/2026"),
    ("Lamotrigine 25 mg tablet", "1 tablet by mouth daily", "Discontinued", "06/24/2026 to 07/09/2026; stopped for drug rash"),
    ("Cetirizine 10 mg tablet", "1 tablet by mouth daily for 7 days", "Completed", "07/09/2026 to 07/16/2026"),
  ]}

# ---------- Problem list ----------
PROBLEMS = {"id": "P1", "kind": "Problem List", "title": "Problem List", "date": "09/16/2026", "author": "Care team", "dept": "Problem List",
  "rows": [
    ("Major depressive disorder, recurrent, moderate", "F33.1", "Active", "Noted 11/2025"),
    ("Generalized anxiety disorder", "F41.1", "Active", "Noted 11/2025"),
    ("Attention-deficit hyperactivity disorder, combined type", "F90.2", "Active", "Noted 2020 (age 9)"),
    ("Nonsuicidal self-injury, history", "Z91.52", "Active", "Last episode 02/2026"),
    ("Iron deficiency without anemia", "E61.1", "Active", "Noted 09/16/2026"),
    ("Vitamin D insufficiency", "E55.9", "Active", "Noted 09/16/2026"),
    ("Drug eruption due to lamotrigine", "L27.0", "Resolved", "07/2026"),
    ("Contusion of right hand", "S60.221A", "Resolved", "02/2026"),
  ]}


def sources():
    """Every source as {id, kind, title, date, author, dept, segments:[{id, section, text}], table?}."""
    out = []
    def seg_body(doc):
        segs, n = [], 0
        for sec, sents in doc["body"]:
            for s in sents:
                n += 1; segs.append({"id": f"{doc['id']}.{n}", "section": sec, "text": s})
        return segs
    for d in NOTES + RADS:
        out.append({k: d[k] for k in ("id", "kind", "title", "date", "author", "dept")} | {"segments": seg_body(d)})
    for d in LABS:
        segs = [{"id": f"{d['id']}.{i+1}", "section": "Results", "text": f"{n}: {v} {u} (reference {r}){' — LOW' if f == 'L' else ' — HIGH' if f == 'H' else ''}",
                 "row": [n, v, u, r, f]} for i, (n, v, u, r, f) in enumerate(d["rows"])]
        out.append({k: d[k] for k in ("id", "kind", "title", "date", "author", "dept")} | {"segments": segs, "table": ["Component", "Value", "Units", "Reference", "Flag"]})
    for d, cols, fmt in ((MEDS, ["Medication", "Sig", "Status", "Dates / notes"], lambda r: f"{r[0]} — {r[1]} — {r[2]} ({r[3]})"),
                         (PROBLEMS, ["Problem", "ICD-10", "Status", "Noted"], lambda r: f"{r[0]} ({r[1]}) — {r[2]}, {r[3]}")):
        segs = [{"id": f"{d['id']}.{i+1}", "section": d["title"], "text": fmt(r), "row": list(r)} for i, r in enumerate(d["rows"])]
        out.append({k: d[k] for k in ("id", "kind", "title", "date", "author", "dept")} | {"segments": segs, "table": cols})
    return out

SOURCES = sources()
BY_ID = {s["id"]: s for s in SOURCES}

def render(src, tagged=True):
    """Plain-text rendering of one source for a model's context."""
    head = f"[{src['id']}] {src['kind']}: {src['title']} — {src['date']} — {src['author']} ({src['dept']})"
    lines, sec = [head], None
    for g in src["segments"]:
        if g["section"] != sec and "table" not in src: lines.append(f"{g['section']}:"); sec = g["section"]
        lines.append(f"  [{g['id']}] {g['text']}" if tagged else f"  {g['text']}")
    return "\n".join(lines)

CHART = "\n\n".join(render(s) for s in SOURCES)

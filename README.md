# Chart Summary Verify

**Can a small, non-generative model check every citation in an AI chart-review summary before a clinician relies on it?**

This is a working mock-up of that idea. An Epic-style EHR shows a pediatric behavioral-health chart (progress notes,
an ED visit, a phone call, labs, imaging, medications, problem list). The right sidebar holds a narrative **chart
summary** written by Claude, with a superscript citation after every sentence. [Jev](https://docs.typesafe.ai) from
TypeSafe AI checks each citation against the source it points to, and the superscript takes on the answer's color:

| Color | Meaning |
|---|---|
| Green | Supported by the cited source |
| Amber | Partly supported, or supported below the confidence threshold |
| Purple | Not in the cited source (may be in another document, or nowhere) |
| Red | Contradicts the cited source |

**Click a citation once** for a preview: the cited passage, Jev's verdict, and its probabilities.
**Click it again** to open the full source in Chart Review, with the cited passage highlighted.
**Advanced** (toggle in the sidebar header) adds a legend with counts and filters, a confidence threshold, a
whole-chart check that tells a wrong citation from a made-up fact, the passage Jev would have cited, and the answer key
for the planted errors.

**Live demo:** https://stephonomon.github.io/chart-summary-verify/ (self-contained page with results embedded; the browser makes no API calls)

![Citation preview: the fever confabulation, not found in the ED note](docs/preview.png)

> Everything here is fabricated: the patient, the clinicians, the chart, and the EHR. "Sandbox EHR" is a mock-up
> styled after the Epic look, and it is not affiliated with Epic Systems. Nothing here is medical advice or a validated clinical tool.

---

## The patient

Avery Delgado, 15, with recurrent major depression, generalized anxiety, ADHD, and a history of nonsuicidal self-injury.
Over the summer her psychiatrist raised sertraline and added lamotrigine for mood lability. On day 15 she came to the
pediatric ED with a benign drug rash. She had no fever and no mucosal involvement. The ED stopped lamotrigine and sent
her home with standard return precautions:

> *Return to the emergency department right away if she develops a fever, blisters, peeling skin, sores in the mouth or eyes, or if the rash spreads quickly.*

The psychiatrist's follow-up call five days later documents that the rash was fading, with no fever at any point.
By September she is better (PHQ-A 16 → 9), with passive suicidal ideation a couple of times a month.

## The confabulation

The planted error at the center of the demo turns the return precaution into an event:

> *Two days later she returned to the ED with a fever and a rapidly spreading rash, and lamotrigine was permanently discontinued and added to her allergy list.* ⁹ ¹⁰

It cites the discharge instructions (⁹) and the follow-up call (¹⁰). The words *fever*, *rash*, and *spreads* all
appear in the cited passage, so a quick glance at the highlighted text can seem to confirm it. Jev reads the source
more closely:

- ⁹ ED note: **not in cited source** (0.69; contradicted 0.26). No return visit is documented.
- ¹⁰ Follow-up call: **contradicts source** (0.96), because "no fever, blistering, or mouth sores at any point."
- Whole chart: **contradicted** (0.99).

![Second click: the full follow-up call, cited passage highlighted, Jev's evidence outlined](docs/full-source.png)

## How it works

```
data.py        the fabricated chart, split into passages with stable IDs (N3.15, L1.6, M1.1 ...)
summarize.py   Claude Opus 5.5 writes the summary; each sentence cites 1-2 passage IDs (structured output) -> summary_claude.json
seeds.py       plants known errors in Claude's frozen output -> summary.json
verify.py      Jev checks every citation, plus every sentence against the whole chart -> results.json
build.py       results + chart -> index.html (Pages) and artifact.html
```

For every **(sentence, cited document)** pair, Jev gets the document as its state and answers two questions:
a Choice over *supported / contradicted / not_found / ambiguous*, and a Choice over the document's passages (which one
is the evidence). The first question sets the superscript color. The second question drives the dashed "Jev's evidence"
outline in the source viewer.

For every **sentence**, Jev also gets the whole chart (~3.5k tokens) and answers the same support question plus
"which passage in the chart is the best evidence". This lets the page separate a *mis-citation* (true, but the cited
document doesn't say it) from a *fabrication* (nothing in the chart says it). Advanced mode shows it as a "Better source"
link.

The `contradicted` criterion names one error class on purpose: *the claim turns something conditional, planned, or
hypothetical in the source (an instruction for what to do if something happens, a plan to consider a change) into
something that actually happened.* That is the confabulation this demo is about, and the same wording catches the
sertraline plan-stated-as-done error.

## Results

Claude wrote 17 sentences and they were accurate. Five were then rewritten by hand to plant errors and two were
inserted, for 19 sentences and 21 citations. Jev marked 11 of the 12 citations on Claude's untouched sentences
supported and one partial. The page opens with "9 of 21 citations need a look": the 8 citations on planted errors plus that partial one.

| Sentence | Planted sentence | Kind | Jev on cited source | Whole chart |
|---|---|---|---|---|
| 2 | Inpatient psychiatric admission in December 2025 | Fabrication | not in source 0.99 | not found 0.95 |
| 4 | Bipolar I disorder in her **father** | Misattribution (it's a maternal aunt) | contradicts 1.00 | contradicted 0.99 |
| 9 | Returned to the ED with a fever and spreading rash | **Confabulation** from return precautions | not in source 0.69 / contradicts 0.96 | contradicted 0.99 |
| 12 | Suicidal ideation has resolved | Overstatement | contradicts 0.89 | ambiguous 0.72 |
| 14 | No firearms in the home (cites the therapy note) | Mis-citation (true; N1.9 says it) | not in source 1.00 | supported 1.00, best N1.9 |
| 18 | Sertraline increased to 100 mg | Plan stated as done | contradicts 1.00 / 0.98 | contradicted 0.99 |
| 16 | Hand X-ray showed no fracture (accurate) | Added so imaging is represented | supported 1.00 | supported 1.00 |

- **6 of 6 planted errors flagged**, each with at least one non-green citation. The mis-citation was the only one the
  whole-chart check marked supported, which is the right answer.
- **1 amber on Claude's own text:** sentence 1 cites the problem list for "followed by child and adolescent psychiatry",
  which the problem list doesn't say (ambiguous 0.83). A reviewer would probably agree that's a partial citation.
- The whole-chart check on #12 came back *ambiguous*, not contradicted: the August therapy note does say she denied
  suicidal ideation *that day*. The cited September note is clear, and the citation check is the one that colors the superscript.
- **Cost and speed:** 40 Jev calls (21 citation + 19 whole-chart), 186k input tokens, 2.2 s wall clock with 8 in parallel.
  The summary itself took Claude 12.5 s.

![Advanced mode: mis-citation, whole-chart check, better source](docs/advanced.png)

## Run it

```bash
export ANTHROPIC_API_KEY=...          # only needed for summarize.py
export TYPESAFE_API_KEY=...           # or put it in ~/.typesafe_api_key
pip install anthropic
python summarize.py   # optional: summary_claude.json is committed, and seeds.py expects its sentence order
python seeds.py
python verify.py
python build.py && open index.html
```

## Caveats

- One fabricated chart, seven planted errors. This is a demonstration, not an evaluation.
- The planted errors were written by the same person who wrote the chart and the Jev criteria.
- Jev's probabilities are shown as it returned them; no calibration was checked here.
- A real deployment would need the full note corpus (dozens of notes, not six), which means retrieval ahead of the
  whole-chart check, and a BAA with any vendor that sees PHI.

## Related

- [Scribe Verify](https://github.com/Stephonomon/scribe-verify): the same idea for ambient-scribe drafts against the encounter transcript.
- [In-basket Triage](https://github.com/Stephonomon/inbasket-triage): Jev classifying patient portal messages.

Code written with Claude (Anthropic). MIT license.

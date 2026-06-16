# Criterion — Cross-Chain Discovery Analysis

**Document type:** PO Advisor analysis  
**Covers:** All three discovery phases (Checklane, Criterion old, Criterion current)  
**Purpose:** Determine whether documents 00–04 of the current chain are complete, what is missing, and what the correct next steps are

---

## The core correction to the previous analysis

The previous analysis stated that the current discovery chain "made a trade-off: it replaced the formal specification layer with a more sophisticated analytical layer." That framing was wrong, and the client correctly identified why.

The current chain is not replacing anything. The current chain is extending the analytical layer by adding three new document types (engagement intake, competitive positioning, persona and MVP hypothesis) that neither previous chain included. The specification layer — solution direction, capability candidates, and architecture constraints — has not been replaced. The specification layer simply has not been written yet, because the current chain's analytical work comes before it in the sequence.

The correct understanding: the current chain is building a longer and more complete discovery sequence, not a compressed one.

---

## The three chains side by side

### Checklane — Phase 1 (9 documents, abandoned after document 01 failed)

```
00 — raw-discovery-notes.md         — 28 signals, 1 role
01 — structured-problem.md          — 5 clusters, missed P6
02 — solution-direction.md          — derived structural direction
03 — capability-candidates.md       — 9 named MVP capabilities (A through I)
04 — architecture-constraints.md    — pytest boundary rules
05 — execution-model.md             — technical blueprint
06 — product-strategy-brief.md      — commercial positioning
07 — product-model-definition.md    — full PRD-level product specification
08 — product-vision.md              — long-term direction
```

**What caused the restart:** Document 01 used a five-cluster model that missed P6 (The Invisible Program). The eight signals that belong in P6 were collapsed into other clusters. Without P6 named, persistence was labelled "Historical Persistence: Next" — a Phase 2 deferral. That was architecturally wrong. Persistence is co-equal with execution, not a future enhancement.

---

### Criterion old — Phase 2 (5 documents written, abandoned before document 05)

```
00 — raw-discovery-notes.md         — 28 signals, 1 role (same as Checklane 00)
01 — structured-problem.md          — 6 clusters P1 through P6 with severity ratings
02 — solution-direction.md          — formally derived two co-equal functions
03 — capability-candidates.md       — 27 named capabilities (E-1 to E-13, P-1 to P-13)
04 — architecture-constraints.md    — 22 numbered constraints with derivation reasoning
[05 — commercial-strategy.md        — planned but never written before restart]
```

**What caused the restart:** Documents 00 through 04 were built on 28 signals from a single automation engineer. QA leads, engineering managers, developers, and compliance officers were not represented. P6 capabilities were based on what the automation engineer inferred those roles needed, not on direct signal from those roles.

**What the Criterion old chain produced correctly:** The two co-equal functions were formally derived. The Shared Run Identity was named. 27 capabilities were formally specified. 22 architectural constraints were numbered and justified. These outputs were correct — the problem was the incomplete signal base they were built from.

---

### Criterion current — Phase 3 (5 documents written, specification layer not yet started)

```
00 — raw-discovery-notes.md         — 47 signals from 5 stakeholder roles ← EXTENDED
01 — engagement-intake-findings.md  — AI company audit of the signal base ← NEW
02 — signal-structuring.md          — signal classification and MVP scope ← ENHANCED
03 — competitive-positioning.md     — gap map, differentiation claims ← NEW
04 — persona-mvp-hypothesis.md      — 5 personas, adoption chain, falsifiable MVP ← NEW
[05 — NOT YET WRITTEN]
[06 — NOT YET WRITTEN]
[07 — NOT YET WRITTEN]
[08 — NOT YET WRITTEN]
...
```

---

## The correct mapping between old and current chain documents

The client identified that when the current chain is compared against the old chains, the current chain is not replacing anything — it is inserting additional documents before the specification layer. The mapping below shows where each document type sits in the extended sequence.

| Old chain position | Document type | Current chain position |
|---|---|---|
| 00 | Raw discovery notes | 00 — same type, extended from 28 to 47 signals across 5 roles |
| — | Engagement intake | 01 — new document type, did not exist in old chains |
| 01 | Structured problem | 02 — same type, renamed "signal structuring," more sophisticated classification |
| — | Competitive positioning | 03 — new document type, did not exist in old chains |
| — | Persona and MVP hypothesis | 04 — new document type, did not exist in old chains |
| 02 | Solution direction | 05 — NOT YET WRITTEN in current chain |
| 03 | Capability candidates | 06 — NOT YET WRITTEN in current chain |
| 04 | Architecture constraints | 07 — NOT YET WRITTEN in current chain |
| 05 | Data model and plugin architecture | 08 — what the AI company called "document 05" |
| 06 | Product model | 09 — pending |
| 07 | Commercial strategy | 10 — pending |
| 08 | Product vision | 11 — pending |

The full current chain, when complete, will be 12 documents (00 through 11), not 9.

---

## Why the AI company's plan to jump to the data model is a problem

The AI company announced in document 04's footer that document 05 would be "Data Model and Plugin Architecture." In the AI company's plan, the sequence goes directly from the analytical layer (docs 00–04) to the technical specification (data model).

This plan skips three documents that must exist before the data model can be derived:

**Missing document 05 — Solution direction.** The solution direction document asks one question per problem cluster: what structural category of response does this cluster require? It then tests whether those responses converge on a shared structural form. The old Criterion chain produced the answer: "a shared platform layer with two co-equal functions — execution and persistence." The current chain's document 02 contains hints of this — Section 5.1 says "the minimum viable design partner version is a data layer" — but the full cluster-by-cluster derivation was never conducted, and the formal direction statement was never produced. Without this formal derivation, the data model has no formally derived architectural foundation to stand on.

**Missing document 06 — Capability candidates.** The capability candidates document translates signals into specific named capabilities — each with an identifier, a definition of the outcome it produces, and a signal trace. The old Criterion chain produced 27 named capabilities. The current chain's document 02, Section 6 maps signals to scope (in-scope, deferred, out of scope) but does not produce named capability identifiers. A signal-to-scope mapping tells you which problems matter. A capability inventory tells you what to build. The data model needs the capability inventory as input — it needs to know what specific things it must store and support, not just which signals motivated building the platform.

**Missing document 07 — Architecture constraints.** The architecture constraints document produces a numbered set of boundaries the architecture must not violate, each with its derivation reasoning. The old Criterion chain produced 22 numbered constraints. The current chain has constraints scattered across documents 02, 03, and 04, but they are never formally stated as a numbered set. Four examples of constraints from the old chain that are not formally stated anywhere in the current chain: the platform must fail visibly and never silently (old C-15); the platform must not introduce new tribal knowledge requirements (old C-17); the platform overhead must not compound the scale ceiling it was designed to analyse (old C-18); existing tests must not require rewriting to adopt the platform (old C-05). Without a formal constraint set, the data model cannot be checked against these boundaries.

---

## Why "not yet written" is not the same as "missing"

An important distinction: the specification documents (05, 06, 07 in the extended sequence) are not missing because someone forgot to write them or because something went wrong. The specification documents have not been written yet because the current chain correctly placed the analytical layer (docs 00–04) first. The analytical layer is now complete. The specification layer is next.

The issue in the previous analysis was the assumption that the current chain had 9 documents total and was halfway done after document 04. The correct understanding is that the current chain will have 12 documents and is approximately one-third done after document 04.

---

## Verdict on the current documents 00 through 04

**Documents 00 through 04 are complete as analytical work.** The signal base (47 signals from 5 roles) is the strongest foundation of the three chains. The competitive positioning, persona modeling, and falsifiable MVP hypothesis add depth that neither previous chain had. No document from 00 through 04 needs to be corrected or restarted. The analytical foundation is sound.

**What is not yet done is the specification work.** The current chain needs documents 05 (solution direction), 06 (capability candidates), and 07 (architecture constraints) before document 08 (data model) can be written. These are not corrections to existing documents — they are the next documents in the sequence.

---

## Three deliberate scope decisions in the current chain

When comparing the current chain's analytical work against the old chains, three scoping decisions appear in the current chain that differ from what previous chains decided. These are not errors — they are deliberate choices made in the current chain. The client should consciously confirm each one before the specification layer is written, because the capability candidates document (06) will reflect these decisions.

**Decision 1 — Secrets handling is out of scope in the current chain.** Both Checklane and Criterion old included secrets handling as a core MVP capability. The current chain's document 02 classifies signal 3.6 (secrets appear in logs and artifacts) as a "Symptom (security)" with addressability marked "Out of scope." The reasoning in document 02: "A security and process problem, not a test platform problem." This is a valid argument. It is also a meaningful reduction in scope relative to what both previous chains included. The client should confirm this is the correct decision.

**Decision 2 — Element resilience (locator management) is deferred in the current chain.** Both Checklane and Criterion old included element resilience as a core MVP capability — specifically addressing the single most frequent source of automation maintenance work (signal 3.3). The current chain's document 02 marks signal 3.3 as "Partial (infrastructure side)" and it is not in the design partner version scope. Again, this is a deliberate and defensible scoping decision, but it is a departure from both previous chains.

**Decision 3 — Historical persistence remains co-equal in the current chain.** This decision is correct and matches the lesson from the first restart. Signal 3.10 is a root cause in the current chain. The foundational capability is described as "Persistent structured run history with 3.46-compliant schema." Persistence is co-equal with execution. This is the lesson the first restart was designed to produce, and the current chain has preserved it correctly.

---

## The quality engineering infrastructure framing

The framing of Criterion as "quality engineering infrastructure" — the tool that converts quality from an organisational problem (requiring TCoEs, Guilds, or dedicated QA functions) into an infrastructure concern that any team can adopt — was developed in PO Advisor sessions but has never been transmitted to the AI company. The AI company has been framing Criterion as a "QA platform" or "test analytics tool" throughout documents 00–04.

This framing has implications for the solution direction document (05), the capability candidates document (06), and especially the commercial strategy document (10). A QA analytics tool is positioned against ReportPortal and Trunk. Quality engineering infrastructure is positioned against the organisational structures teams build when they have no platform to run on. These are different positioning arguments.

The framing should not be transmitted to the AI company as a directive. The AI company should be asked whether this framing is consistent with what documents 00–04 established, and whether the framing should shape how the solution direction is derived.

---

## The correct complete sequence for the current chain

```
00 — raw-discovery-notes.md             ✅ Complete — 47 signals, 5 roles
01 — engagement-intake-findings.md      ✅ Complete — AI company audit
02 — signal-structuring.md              ✅ Complete — classification, MVP scope
03 — competitive-positioning.md         ✅ Complete — gap map, differentiation
04 — persona-mvp-hypothesis.md          ✅ Complete — 5 personas, falsifiable MVP

05 — solution-direction.md              🔑 NEXT — what kind of system solves this?
06 — capability-candidates.md           ⏳ Pending — named inventory of what to build
07 — architecture-constraints.md        ⏳ Pending — numbered boundaries
08 — data-model-plugin-architecture.md  ⏳ Pending — technical specification
09 — product-model.md                   ⏳ Pending — what each persona interacts with
10 — commercial-strategy.md             ⏳ Pending — how it sustains and reaches users
11 — product-vision.md                  ⏳ Pending — long-term direction
```

---

## What each remaining document must answer

**Document 05 — Solution direction.**  
The single question: what structural category of response does each root cause and high-priority symptom in the current chain require? The current chain classifies signals as root cause, symptom, and consequence. The solution direction document asks what structural form the response to each root cause takes, tests whether those forms converge, and produces a formal direction statement. In the old Criterion chain, the answer was "a shared platform layer with two co-equal functions — execution and persistence." The current chain's document must either confirm this direction from the 47-signal base and multi-role analysis, or refine it. The answer cannot be assumed from the previous chain — it must be derived from the current chain's evidence.

**Document 06 — Capability candidates.**  
The single job: produce a named inventory of specific capabilities the platform must provide, derived from the structural direction in document 05 and the MVP scope in document 02. Each capability gets an identifier, a definition of the outcome it produces (not the signal it addresses), and a trace to the source signal. The old Criterion chain produced 27 capabilities. The current chain, with 47 signals from 5 roles, will likely produce a different and possibly longer list. The Shared Run Identity — the connective mechanism that both previous chains named — must be included.

**Document 07 — Architecture constraints.**  
The single job: produce a numbered set of boundaries the architecture must not violate, each with its derivation reasoning. Each constraint must be labelled as either stated (explicitly named in the raw signals) or implied (derived from context with written reasoning that can be challenged). The reasoning column is what makes constraints durable — a constraint without derivation cannot be defended or updated when circumstances change.

**Document 08 — Data model and plugin architecture.**  
This is what the AI company called document 05. With the foundation of solution direction, capability candidates, and architecture constraints now in place, the data model can be derived from those formal inputs rather than from scattered analytical work. The data model's schema fields are determined by which capabilities they support. The architecture choices are checked against the formal constraint set.

---

## How to present this to the AI company

The client's instruction is correct: the AI company should not be told about the two previous restarts or their history. The AI company should be presented with observations and questions, and allowed to reason about them independently.

The following observations and questions should form the briefing before any new document is written:

**Observation 1 (the missing specification layer):** "We have reviewed the current chain carefully and compared it with the structure of similar product discovery processes. We noticed that two types of documents that are typically produced before technical specification have not yet appeared in the current chain: a formal solution direction document that derives what structural category of system is required, and a formal capability candidates document that names what the platform must provide. We believe these should come before the data model. Do you agree? If so, please produce the solution direction as the next document, then the capability candidates, then the architecture constraints, and then the data model — rather than moving to the data model directly."

**Observation 2 (the scope decisions to confirm):** "The current chain placed secrets handling out of scope and element resilience in the deferred category. We want your view on whether these are the correct scoping decisions for the design partner version, given what the signal base and adoption chain established."

**Observation 3 (the framing question):** "A framing has emerged from our review: Criterion as quality engineering infrastructure — the layer that converts quality from an organisational coordination problem into a platform concern any team can run on, in the same way that infrastructure-as-code tools converted server management from an organisational problem into a code-defined concern. Does this framing hold up against what documents 00 through 04 established? If so, how should it shape the solution direction document?"

**Standing requirement (the schema constraint):** "Whatever sequence is agreed, the data model document must include signal 3.46's three fields (feature identifier, release identifier, timestamp) and a stable unique failure record identifier on every record from the first run. These fields are non-deferrable because records collected without them cannot be retroactively updated."

---

## Summary of findings

| Finding | Verdict |
|---|---|
| Documents 00–04 need correction | No — documents 00–04 are analytically complete and sound |
| A restart is needed | No — the current chain is the strongest foundation of the three |
| The AI company's plan (data model as document 05) is correct | No — three specification documents must come first |
| The sequence should have 9 documents | No — the correct total is 12 documents (00 through 11) |
| The current chain made a trade-off by replacing the specification layer | No — the current chain added analytical depth before the specification layer; the specification layer is still coming |
| Documents 05, 06, 07 are missing from the current chain | Yes — solution direction, capability candidates, and architecture constraints have not yet been written |
| The quality engineering infrastructure framing is in the current chain documents | No — this framing was developed in PO Advisor sessions and has not been transmitted to the AI company |

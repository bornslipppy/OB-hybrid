---
title: "AI-Driven Adaptive Questionnaire Workflows for Onboarding — Research Report"
author: "Mary (Business Analyst)"
date: 2026-06-02
status: draft
purpose: "Establish what is known about AI-driven adaptive data-collection workflows, where AI adds measurable value over deterministic decision trees, and the implications for the Guesty Pro onboarding agent PoC."
related:
  - planning-artifacts/guesty-pro-account-creation-schema.md
  - Tahini/knowledge (domains, personas, product-model)
  - OB V2 prototype (wizard.jsx / screens.jsx)
  - conversation_script_financials.md
  - ob_specialist_brief.md
---

# AI-Driven Adaptive Questionnaire Workflows for Onboarding

> **Bottom line up front.** "AI vs. rule-based decision tree" is a false binary. The
> academic record shows an *optimal* adaptive questionnaire **is mathematically a decision
> tree** — so the real question is not *whether* to branch, but **who authors the branching
> and how it handles unbounded, messy, real-world input**. AI earns its place in exactly
> four spots: (1) turning free-text into structured fields, (2) collapsing a combinatorial
> branch space no human wants to hand-author, (3) resolving ambiguity in one turn, and
> (4) synthesising the result into a human-readable brief. Everywhere else — required
> structured fields, dates, file uploads, tax/legal — deterministic rules and plain widgets
> still win, and the existing conversation scripts already encode that boundary correctly.

---

## 1. Scope & method

This report answers the background-research questions from the task brief:

1. What is known about AI-driven questionnaire workflows for onboarding (and adjacent fields)?
2. How can models adapt question sequences based on prior input — conditional branching, NLP intent inference, embedding-based routing?
3. Where does AI add **measurable** value over deterministic decision trees?

**Sources** are graded for confidence using a simple scale, because not all evidence is equal:

| Grade | Meaning | Used here for |
|-------|---------|---------------|
| **A — Peer-reviewed / canonical** | Academic literature, established textbooks | Adaptive-testing theory, slot-filling, dialogue systems |
| **B — Industry-practitioner** | Vendor engineering write-ups, framework docs | Agent-form design patterns, hybrid policies |
| **C — Vendor marketing** | Benchmark blogs with commercial incentive | Directional conversion/completion claims only |
| **I — Internal artifact** | Files supplied for this project | Prototype logic, scripts, schema, personas |

---

## 2. The foundational result: an optimal adaptive questionnaire *is* a decision tree

The strongest and most decision-relevant finding. **Computerized Adaptive Testing (CAT)** — the 40-year-old science behind adaptive exams (GRE, GMAT) — selects each next item based on everything the respondent has answered so far, to reach a confident estimate in the fewest questions. That is precisely the CEO's described behavior ("10 listings → who owns them → … → keep going until we have what we need").

The key result: Delgado-Gómez et al. (2019) **mathematically proved the equivalence** between an IRT-based adaptive test and a decision tree when using the MEPV item-selection criterion, and built **Tree-CAT** on top of that equivalence; **Merged Tree-CAT** (2020) makes it run in seconds on a laptop. *(Grade A.)*

> "creating a CAT with item exposure controls can be understood as the simultaneous construction of several trees" — *Computerized adaptive test and decision trees: A unifying approach* (White Rose / Expert Systems with Applications).

**Implications for us:**

- The user's own framing is correct: at its core this is a deterministic decision tree. That is **not a weakness of the idea — it is the theory.** A well-built adaptive flow *should* be reducible to a tree.
- Therefore "use AI" cannot be justified by "we need adaptivity." Adaptivity is achievable with a hand-built or auto-generated tree. **The PoC must justify AI on grounds a tree cannot satisfy** (Section 5).
- A tree can even be *pre-computed* from the model, giving instant, auditable, repeatable question selection — attractive for the financial/tax fields where the scripts already demand determinism and echo-before-write.

A second strand (Tree-based adaptive classification, *Psychometrika*-adjacent ML work, Grade A) shows decision trees are the *preferred* adaptive method precisely when the construct spans **many distinctive domains** and a single unified model doesn't fit — which is exactly the Guesty profile (6 product domains in `Tahini/knowledge/domains/index.md`, from financials to operations to distribution).

---

## 3. The data-collection backbone: domains, intents, slots, and "frames"

The canonical architecture for goal-oriented data collection is **slot filling** within a **frame**, from task-oriented dialogue systems (Jurafsky & Martin, *Speech and Language Processing*, ch. on dialogue; Louvan & Magnini 2020 survey). *(Grade A.)*

The frame model maps **directly** onto this project:

| Dialogue-systems concept | Guesty onboarding equivalent |
|--------------------------|------------------------------|
| **Frame** | The account-creation schema (the "complete customer profile") |
| **Slot** | A single field (e.g., `payment_split`, `revenue_recognition`) |
| **Domain classification** | Which section the user is talking about (Financials, Operations…) |
| **Intent determination** | What the user is trying to do (answer / ask advice / skip / correct) |
| **Slot filling** | Extracting the value to record (`record_answer`, `add_fee`, `add_tax`) |
| **Dialogue policy** | "ask questions until the slots are full, then act" |

The classic frame-based dialogue policy — *"ask questions until all slots are full, do the query, report back"* — is the textbook description of what the wizard already does, and what the agent should do conversationally. This is well-trodden ground; the PoC is not inventing a new paradigm, it is applying a mature one.

**Three mechanisms for "adapting the next question," from least to most AI:**

1. **Conditional branching (deterministic rules).** Already present in the prototype as `showIf` predicates: `pay_timing === "split"` gates the deposit question; `oauth_status === "success"` gates the Airbnb listing picker (`screens.jsx`). Cheap, auditable, zero variance. The right tool for required structured fields.
2. **Intent / NLP inference.** Classify each utterance into {answer, advice-seeking, skip, correction, out-of-scope} and route accordingly. The financials script is effectively a **hand-written intent policy** today (Paths B–H: advice-seeking → flag+defer; ambiguous → one clarifying question; wrong-fact → record+flag). An NLU/LLM layer generalises this beyond the scripted phrasings. *(Grade A for the technique; I for the script.)*
3. **Embedding-based / semantic routing.** Map a free-text answer to the nearest known branch by semantic similarity (e.g., "I take half up front and half before they arrive" → `payment_split = 50_50`). Useful for normalising unbounded answers onto a fixed slot vocabulary without enumerating every phrasing.

Modern practice (Grade B) increasingly exposes the **schema itself as the contract** the agent reads — stable field IDs, machine-readable validation, structured confirmations (the "Designing Forms an AI Agent Can Actually Submit" pattern; Grid Dynamics "schema is the contract"). This validates building the schema (deliverable 2) as the **first** artifact: the agent is only as good as the frame it fills.

**Production reality — hybrid, not pure-LLM.** The dominant production pattern (Rasa and successors, Grade B) is a **hybrid policy**: deterministic `RulePolicy` for the paths that must be controlled, neural/LLM for generalisation beyond seen paths. Reported viability targets are useful PoC goalposts: **≥70% task-completion** on scripted flows, an **ideal 6–10 turn** path to fill all slots, and a **≥50% help-recovery** rate. *(Grade A/B.)*

---

## 4. Where AI adds *measurable* value over a deterministic tree

This is the crux of the PoC. AI is justified only where a hand-authored or auto-generated tree structurally cannot keep up. Four areas hold up to scrutiny:

### 4.1 Unbounded input → structured field (the strongest case)
A decision tree can only branch on values it enumerated in advance. Real onboarding answers are open-ended:
- *"Depends — Airbnb collects at booking but for direct I take 50% upfront, 50% a week before"* (financials script, **Path C**) → must resolve to `payment_timing` + `payment_split` + a note.
- The "biggest thing slowing you down" free-text (`pain` field) → the OB brief quotes it verbatim and ranks the call agenda around it.
- A messy owner CSV / verbal ownership description → structured `Owner[]` + `ListingOwnership[]` rows.

A tree would need a pre-built option for every phrasing; an LLM extracts the slot value directly. **This is where slot-filling NLP genuinely beats branching.** *(Grade A technique.)*

### 4.2 Combinatorial branch explosion (the CEO's actual pain)
The CEO's complaint is authorial cost: *"instead of me designing every question one by one."* The ownership path illustrates the explosion:

```
listing_count → ownership_model (own / managed-for-others / mixed)
  → if managed/mixed: per-owner records (name, email, listings, share)
    → business model per owner (commission % / fixed fee / revenue split / other)
      → if commission: rate, base, who pays channel fees …
```

Hand-authoring every node, for every domain, and maintaining it as the product changes, is the cost. An LLM reasoning against the **schema + domain knowledge** generates the next relevant question without a human drawing the full tree. **The value is reduced authoring/maintenance effort, not raw capability** — and that is a *measurable* claim (authoring hours, time-to-update when product changes).

### 4.3 One-shot ambiguity resolution
The script's rule is explicit: **one clarifying question, then flag and skip** — never loop (Path C). LLMs are good at "ask the single most informative follow-up," which is the CAT objective (maximise information per question) expressed conversationally. Measurable as **turns-to-complete** and **clarification efficiency**.

### 4.4 Post-collection synthesis (separate, constrained call)
The OB Specialist Brief is generated by a **separate, low-temperature LLM call after** the conversation — constrained to synthesise recorded data into a one-pager, introduce no new facts, quote the user directly, and sort flags financial > legal > operational > other (`ob_specialist_brief.md`). This is a classic, low-risk summarisation task with its own eval suite (~20 scenarios). High reliability, clear value, cleanly separated from the riskier in-conversation agent.

### 4.5 Where AI should **NOT** be used (equally important)
The scripts already draw this line correctly; the schema must preserve it:
- **Required structured fields / dates / counts / file upload** — plain widgets, deterministic. (Forms still win here; even the pro-conversation vendor sources concede this.)
- **Tax & legal** — the agent **records what the user said, flags for the human (Jordan), and never corrects** (Path H). Tax setup is explicitly human-owned.
- **Numeric financial writes** — **echo-before-write**: the agent says the number back and only fires `add_fee` / `add_tax` after confirmation (Path D). Determinism and auditability over cleverness.
- **Advice / recommendations** — consistently deflected to the human, even under pressure (Paths B, G). This protects the high-touch onboarding model.

---

## 5. Evidence on completion & data quality (handle with care)

There is a large body of **vendor-marketing** evidence (Grade C) claiming conversational intake beats static forms. It is directionally consistent but commercially motivated, so treat magnitudes skeptically:

| Claim | Reported range | Grade | Note |
|-------|----------------|-------|------|
| Completion-rate lift, conversational vs. form | "15–40%" (one) to "2–4×" (others) | C | High variance; self-selected case studies |
| Form abandonment baseline | ~67–70% | C (echoes Baymard, B) | Plausible for high-field-count forms |
| "More usable signal per session" | ~2.4× | C | Aligns with §4.1 (richer free-text) |
| Onboarding/KYC intake = highest-friction form | consistent across sources | C | Matches our 18-question, 7-section surface |

**Honest read:** the *direction* (conversational adaptive intake lifts completion and data depth on **high-friction, high-field-count** flows — exactly onboarding intake) is corroborated by independent academic mechanisms (progressive disclosure, reduced cognitive load) and is plausible. The *specific multipliers* are not reliable planning inputs. **The PoC should measure this ourselves rather than import a vendor number.**

---

## 6. Synthesis & implications for the PoC

1. **Build the frame first.** Everything depends on a finite, canonical "complete customer profile." That is deliverable 2 (the account-creation schema). The agent reasons toward filling it; the brief synthesises from it; the tree (baseline) branches over it.
2. **Frame the PoC as a fair head-to-head**, AI-adaptive flow vs. an honestly-built deterministic decision-tree baseline, on the **same** respondent profiles. Given the CAT≡tree equivalence, anything else is not a real test of AI's added value.
3. **Center the hero scenario on the ownership → business-model branch** (§4.2). It is the richest, most combinatorial, currently-missing path, and it is the exact example the CEO used.
4. **Adopt the hybrid architecture explicitly.** Deterministic rules + widgets for required/structured/financial/legal fields; LLM for extraction, branching-generation, one-shot clarification, and the post-hoc brief. Don't let the LLM touch tax/legal/numeric writes except via echo-before-write.
5. **Borrow the viability goalposts** as provisional success thresholds: ≥70% task completion, 6–10 turn ideal path, ≥50% help recovery — plus our own measured completion/data-quality delta vs. the baseline.
6. **Honor the CEO's two structural directions:** Airbnb connection moves **inside the product** (drop the in-wizard OAuth/import screens from the questionnaire frame); the agent reasons toward a **complete profile**, not an authored question list.

### Measurable PoC hypotheses (candidates)
| # | Hypothesis | Primary metric | Beats baseline if… |
|---|------------|----------------|--------------------|
| H1 | AI captures a *more complete* profile on messy inputs | % required slots correctly filled | AI > tree on free-text-heavy profiles |
| H2 | AI needs *fewer turns* for equivalent completeness | turns-to-complete | AI ≤ tree at equal slot accuracy |
| H3 | AI handles inputs the tree *cannot* | % unbounded answers correctly normalised | tree falls back to "other"/skip; AI extracts |
| H4 | AI *reduces authoring effort* | author hours to add/maintain a domain | AI+schema << hand-built tree |
| H5 | The brief is *useful to onboarders* | onboarder "useful" rating (target ≥80%) | per `ob_specialist_brief.md` feedback loop |

---

## 7. Risks & open questions surfaced by the research

- **Determinism vs. variation.** CAT/tree gives identical next-question for identical history; an LLM at temperature does not. For financial/tax slots, prefer the deterministic path or temperature 0 + echo-before-write.
- **Slot/intent error rate is the real KPI**, not "conversation length" or vibe. A misheard "15%" vs "50%" survives to a guest invoice (Path D). Evals must measure slot error rate.
- **Cold-start data.** We need a realistic, varied set of respondent profiles (beyond the single "Pinkie Flamingo / 8 listings / 4 owners" example) to measure adaptivity. Synthesising these is a PoC prerequisite.
- **Out-of-scope handling.** Conditional fees, complex business models, tax — the agent must flag-and-continue, never fake capability (Paths E, H). The schema must mark these `human_handoff`.
- **Vendor stats are not planning inputs.** Measure completion/quality lift in-house.

---

## 8. Source ledger

**Grade A — academic / canonical**
- Delgado-Gómez et al., *Computerized adaptive test and decision trees: A unifying approach* (Expert Systems with Applications) — CAT ≡ decision tree (Tree-CAT).
- Rodríguez-Cuadrado et al., *Merged Tree-CAT* (Expert Systems with Applications, 2020) — fast tree-based CAT; `cat.dt` R package (R Journal 2021).
- *Survey of Computerized Adaptive Testing: A Machine Learning Perspective* (arXiv 2404.00712) — CDM → selection algorithm → question bank → stopping rule.
- ML tree-based adaptive classification (PMC7495791) — trees preferred for multi-domain constructs.
- Jurafsky & Martin, *Speech and Language Processing* (dialogue chapters) — frames, slots, domain/intent/slot-filling, frame-based dialogue policy, slot error rate.
- Louvan & Magnini, *Recent Neural Methods on Slot Filling and Intent Classification* (COLING 2020 survey); joint intent+slot review (Neural Computing & Applications, 2025).

**Grade B — practitioner / framework**
- Rasa hybrid dialogue policy (RulePolicy + neural); intent-based TOD with LLMs (CMC techscience) — viability targets (≥70% completion, 6–10 turns).
- "Designing Forms an AI Agent Can Actually Submit" (DEV) and Grid Dynamics "Adaptive UI" — schema-as-contract, stable semantic field IDs, MCP-exposed form tools.
- FormGym (EACL 2026) — field localisation as the bottleneck in agent form-filling.

**Grade C — vendor marketing (directional only)**
- Perspective AI "State of AI Onboarding 2026" / "Form Replacement Report"; Gnosari "AI vs Forms"; Neomanex — conversational vs. form completion/quality claims.

**Grade I — internal artifacts**
- OB V2 prototype (`wizard.jsx`, `screens.jsx`) — deterministic `showIf` baseline.
- `conversation_script_financials.md` — hand-authored intent policy (Paths A–H), echo-before-write, flag-and-skip.
- `ob_specialist_brief.md` — post-hoc synthesis deliverable + generation logic + evals.
- `Inputs from Salesforce.md` — prefill/seed schema.
- `Tahini/knowledge` — domains, personas, entity model (Owner, ListingOwnerships, BusinessModel).

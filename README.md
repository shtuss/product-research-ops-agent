# Product Research Ops Agent

**Interview-to-Insights Pipeline** — a multi-agent automation that turns raw interview transcripts into prioritized personas and Jobs-to-be-Done, with a human-in-the-loop review and a full evaluation/governance layer.

> Built by a product designer who can also build the tools that make product research faster — without giving up the human review step research quality depends on.

---

## The problem

Interview synthesis is the most repeated, least automated part of product research. This project automates that first pass — classification, theme extraction, cross-interview synthesis — while keeping a researcher in control of every final output before it ships.

## What it does

1. A researcher submits a project brief and interview transcripts via a **Tally** form.
2. An **orchestrator** classifies each submission (new vs. existing project) and routes it to the right sub-workflow — no continuous agent loop, just a one-time classification decision (cheaper, deterministic, and easier to audit).
3. An **Interview Analysis agent** extracts themes, pain points, and quotes from each transcript.
4. A **Synthesis agent** scores themes by frequency *across distinct interviews* (not raw mention count, to avoid one talkative participant skewing results) and groups findings into 2–4 personas with cited Jobs-to-be-Done.
5. A **human approval gate** in Slack — nothing is finalized until a researcher reviews and approves it.
6. An independent **dashboard** renders the final research synthesis on demand.

## Architecture

Six connected n8n workflows, communicating through a shared `project_id`, Google Sheets, and Execute Workflow nodes:

```
Project Setup → Competitive Analysis → Interview Intake → Interview Analysis → Research Synthesis → Dashboard API
```

Full node-by-node breakdown, the security/governance audit, and the scope decisions behind this architecture are documented in [`/docs/case-study.pdf`](./docs/case-study.pdf).

## Tech stack

n8n (workflow orchestration) · Python 3 (n8n Code nodes — cleaning, frequency scoring, output validation) · Groq (LLM) · Tavily via MCP (competitor web search) · Google Sheets API (structured storage) · Tally (form intake) · Slack API (notifications + human approval) · Render (dashboard hosting)

## Data model

A 9-tab Google Sheets schema acts as the system of record: `projects`, `interviews`, `findings`, `theme_scores`, `synthesis_outputs`, `approval_requests`, `source_reviews`, `audit_events`, `evaluation_cases`. Chosen deliberately over a database for the MVP — instantly readable by a non-technical reviewer, no hosting or migrations needed, and already structured to migrate cleanly to a relational database later.

## Governance & evaluation

A structured 5-part audit was run before shipping: execution log review, a 6-case evaluation dataset (normal / ambiguous / adversarial cases, including a live prompt-injection test), system prompt hardening, credential/tool least-privilege review, and written governance documentation (including an EU AI Act risk classification). Full details in `/docs/case-study.pdf`.

## Status

**Delivered (capstone MVP):**
- Working n8n multi-agent workflow, end-to-end from intake to insight synthesis
- 9-tab structured Google Sheets data model
- Human-in-the-loop approval via Slack
- Independent dashboard endpoint
- Full 5-part security & governance audit

**In progress (v2 — see [project brief](./docs/case-study.pdf) for the full roadmap):**
- Migrating orchestration from n8n's AI Agent node to a LangGraph + FastAPI service
- RAG over Supabase/pgvector for cross-project retrieval
- Expanded evaluation set (6 → 15+ cases) with metric-based scoring
- Slack interactive callbacks replacing the current form-based approval
- Authentication and a secure, searchable research repository

## Repository structure

```
/n8n/     — exported n8n workflow JSON (intake, analysis, synthesis, dashboard)
/docs/    — full project write-up, architecture notes, governance documentation
```

*(Additional folders — `/agents`, `/api`, `/rag`, `/dashboard`, `/evaluation` — will be added as the v2 build progresses; see the roadmap above.)*

## Links

- Demo video: _add link_
- Live dashboard: _add link_

---

*AI Agents & Automations Capstone · Natalia Brzhestovska*

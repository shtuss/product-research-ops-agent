"""
State schema for the Product Research Ops Agent LangGraph pipeline.

Note on routing logic (n8n WF-01, WF-03): classification of input_type
does not happen through an AI agent call, as originally described in
the capstone report. Instead, it happens through which Tally form was
submitted — Project Setup and Interview each have a distinct formId,
and each triggers its own dedicated n8n workflow. This schema
deliberately mirrors that same behavior in code: input_type is passed
in as a known fact, not re-derived by an agent.
"""

from typing import TypedDict, Literal, Optional


class ProjectSetupPayload(TypedDict):
    """Matches the fields extracted in WF-01 -> '02 — Normalize Input'."""
    project_id: str
    project_name: str
    research_goal: str
    product_description: str


class InterviewPayload(TypedDict):
    """Matches the fields extracted in WF-03 -> '02 — Normalize Interview Input'."""
    project_id: str
    participant_label: str
    interviewer_name: str
    interview_transcript: str
    interview_id: str


class AgentState(TypedDict):
    # Which kind of request came in — determined by which Tally form
    # was submitted (see module docstring above)
    input_type: Literal["project_setup", "interview"]

    # Shared identifier across both request types — links all data
    # belonging to one research project
    project_id: str

    # Raw form data — the concrete shape depends on input_type
    payload: ProjectSetupPayload | InterviewPayload

    # Processing result (filled in by the agent during execution,
    # empty at the start)
    classification: Optional[str]

    # What to do next — e.g. "run_competitive_analysis" or
    # "run_interview_analysis" (mirrors the Execute Workflow nodes
    # in n8n: '04 — Run Competitive Analysis' in WF-01,
    # '03 — Run Interview Analysis' in WF-03)
    next_action: Optional[str]

    # Bookkeeping — creation time, analysis version, etc.
    metadata: dict


# --- Manual test examples (Week 2, Day 2 checklist item) ---
# Two hand-built state examples, using real field values from the
# exported n8n workflows, to sanity-check that the schema's shape
# actually matches what the workflows produce.

# Example 1 — project setup (matches WF-01)
example_project_setup: AgentState = {
    "input_type": "project_setup",
    "project_id": "therapy-platform-2026",
    "payload": {
        "project_id": "therapy-platform-2026",
        "project_name": "MindMatch – Therapist Discovery Platform",
        "research_goal": "Understand how people search for psychotherapists",
        "product_description": "MindMatch is an online platform that helps people find licensed psychologists and psychotherapists through intelligent matching.",
    },
    "classification": None,
    "next_action": "run_competitive_analysis",
    "metadata": {"created_at": "2026-07-13T14:38:45.889Z"},
}

# Example 2 — interview intake (matches WF-03)
example_interview: AgentState = {
    "input_type": "interview",
    "project_id": "therapy-platform-2026",
    "payload": {
        "project_id": "therapy-platform-2026",
        "participant_label": "P-001",
        "interviewer_name": "Natalia",
        "interview_transcript": "I don't want to judge therapists by their profile picture. I want confidence that they are actually qualified.",
        "interview_id": "therapy-platform-2026-int-1784269821835",
    },
    "classification": None,
    "next_action": "run_interview_analysis",
    "metadata": {"submitted_at": "2026-07-17T02:30:25.341-04:00"},
}
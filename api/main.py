from typing import Literal, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agents.orchestrator import build_orchestrator_graph

app = FastAPI(title="Product Research Ops Agent API")
orchestrator = build_orchestrator_graph()


# --- Request model ---
# Only the raw intake data goes in here — classification and next_action
# are OUTPUTS of the orchestrator, not something the caller (n8n) should
# be supplying. input_type is a Literal, not a bare str, so an invalid
# value is rejected by FastAPI/Pydantic with a 422 before it ever reaches
# the graph.
class OrchestrateRequest(BaseModel):
    input_type: Literal["project_setup", "interview"]
    project_id: str
    payload: dict
    metadata: dict = Field(default_factory=dict)


# --- Response model ---
# Mirrors AgentState, but documents the shape that actually comes back
# to the caller once the graph has run.
class OrchestrateResponse(BaseModel):
    input_type: str
    project_id: str
    payload: dict
    classification: Optional[str]
    next_action: Optional[str]
    metadata: dict


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Product Research Ops Agent API is running"}


@app.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(request: OrchestrateRequest):
    # Build a fresh AgentState — classification/next_action always start
    # empty, since only the graph is allowed to set them.
    state = {
        "input_type": request.input_type,
        "project_id": request.project_id,
        "payload": request.payload,
        "classification": None,
        "next_action": None,
        "metadata": request.metadata,
    }
    result = orchestrator.invoke(state)
    return result
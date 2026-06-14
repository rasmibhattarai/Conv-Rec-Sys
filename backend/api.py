import uuid
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import src.tools  # Important to register tools
from src.agent import agent
from src.state import AppliancePreferences

app = FastAPI(title="Appliance Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str


sessions = {}


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    if session_id not in sessions:
        sessions[session_id] = {"deps": AppliancePreferences(), "history": []}

    session = sessions[session_id]

    result = await agent.run(
        req.message, deps=session["deps"], message_history=session["history"]
    )

    session["history"] = result.all_messages()

    return {
        "session_id": session_id,
        "response": result.output,
        "state": session["deps"].model_dump(),
    }

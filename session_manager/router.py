from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4

from .models import Session, SessionCreateRequest, AddMessageRequest, SessionStatus, Message
from .session_store import get_session, save_session

router = APIRouter()

@router.post("/session/", response_model=Session)
def create_session(req: SessionCreateRequest):
    session_id = f"sess_{uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    initial_msg = Message(from_user=True, text=req.user_input, timestamp=now)
    session = Session(
        session_id=session_id,
        created_at=now,
        messages=[initial_msg],
        assigned_agents=req.assigned_agents,
        status=SessionStatus(status={agent: "pending" for agent in req.assigned_agents})
    )
    save_session(session)
    return session

@router.get("/session/{session_id}", response_model=Session)
def fetch_session(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/session/{session_id}/message", response_model=Session)
def append_message(session_id: str, req: AddMessageRequest):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    msg = Message(
        from_user=req.from_user,
        text=req.text,
        agent=req.agent,
        timestamp=datetime.utcnow().isoformat()
    )
    session.messages.append(msg)
    save_session(session)
    return session

@router.put("/session/{session_id}/status", response_model=Session)
def update_status(session_id: str, status: SessionStatus):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.status = status
    save_session(session)
    return session

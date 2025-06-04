from typing import Dict
from .models import Session

sessions: Dict[str, Session] = {}

def get_session(session_id: str) -> Session | None:
    return sessions.get(session_id)

def save_session(session: Session):
    sessions[session.session_id] = session

from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class Message(BaseModel):
    from_user: bool
    text: str
    agent: Optional[str] = None
    timestamp: str = datetime.utcnow().isoformat()

class SessionStatus(BaseModel):
    status: Dict[str, str]

class Session(BaseModel):
    session_id: str
    messages: List[Message]
    assigned_agents: List[str]
    status: SessionStatus
    created_at: str

class SessionCreateRequest(BaseModel):
    user_input: str
    assigned_agents: List[str]

class AddMessageRequest(BaseModel):
    from_user: bool
    text: str
    agent: Optional[str] = None

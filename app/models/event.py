from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum

class EventType(str, Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PRODUCT_VIEW = "PRODUCT_VIEW"

class UserEventRequest(BaseModel):
    userId: str = Field(..., description="Identifier of the user")
    eventType: EventType
    payload: Dict[str, Any] = {}

class UserEvent(BaseModel):
    eventId: str
    userId: str
    eventType: EventType
    timestamp: str
    payload: Dict[str, Any]
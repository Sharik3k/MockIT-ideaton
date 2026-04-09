from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum

class InviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"

class InviteRole(str, Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
    VIEWER = "viewer"

class InviteCreateRequest(BaseModel):
    email: EmailStr
    role: InviteRole = InviteRole.RECRUITER
    message: Optional[str] = Field(None, max_length=500)

class InviteResponse(BaseModel):
    id: str
    workspaceId: str
    email: str
    role: str
    status: str
    message: Optional[str] = None
    invitedBy: str
    createdAt: str
    expiresAt: str

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class LinkStage(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    TECHNICAL = "technical"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class LinkCreateRequest(BaseModel):
    candidateId: str = Field(..., min_length=1)
    vacancyId: str = Field(..., min_length=1)
    currentStage: LinkStage = LinkStage.APPLIED

class LinkResponse(BaseModel):
    id: str
    workspaceId: str
    candidateId: str
    vacancyId: str
    currentStage: str
    appliedAt: str

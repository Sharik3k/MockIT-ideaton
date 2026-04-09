from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum

class CandidateStage(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    TECHNICAL = "technical"
    OFFER = "offer"
    REJECTED = "rejected"
    HIRED = "hired"

class CandidateCreateRequest(BaseModel):
    fullName: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    linkedinUrl: Optional[HttpUrl] = None
    githubUrl: Optional[HttpUrl] = None
    portfolioUrl: Optional[HttpUrl] = None
    notes: Optional[str] = Field(None, max_length=1000)
    stage: CandidateStage = CandidateStage.APPLIED
    skills: List[str] = Field(default_factory=list)

class CandidateUpdateRequest(BaseModel):
    fullName: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    linkedinUrl: Optional[HttpUrl] = None
    githubUrl: Optional[HttpUrl] = None
    portfolioUrl: Optional[HttpUrl] = None
    notes: Optional[str] = Field(None, max_length=1000)
    stage: Optional[CandidateStage] = None
    skills: Optional[List[str]] = None

class CandidateResponse(BaseModel):
    id: str
    workspaceId: str
    fullName: str
    email: str
    phone: Optional[str] = None
    linkedinUrl: Optional[str] = None
    githubUrl: Optional[str] = None
    portfolioUrl: Optional[str] = None
    notes: Optional[str] = None
    stage: str
    skills: List[str]
    createdAt: str
    updatedAt: str

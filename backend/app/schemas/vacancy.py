from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"

class WorkModel(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"

class Seniority(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"

class VacancyStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"

class VacancyCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    department: str = Field(..., min_length=1, max_length=100)
    seniority: Seniority
    employmentType: EmploymentType
    workModel: WorkModel
    location: str = Field(..., min_length=1, max_length=200)
    descriptionRaw: str = Field(..., min_length=1)
    mustHaveSkills: List[str] = Field(default_factory=list)
    niceToHaveSkills: List[str] = Field(default_factory=list)

class VacancyUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    seniority: Optional[Seniority] = None
    employmentType: Optional[EmploymentType] = None
    workModel: Optional[WorkModel] = None
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    descriptionRaw: Optional[str] = Field(None, min_length=1)
    mustHaveSkills: Optional[List[str]] = None
    niceToHaveSkills: Optional[List[str]] = None
    status: Optional[VacancyStatus] = None

class VacancyResponse(BaseModel):
    id: str
    workspaceId: str
    title: str
    department: str
    seniority: str
    employmentType: str
    workModel: str
    location: str
    descriptionRaw: str
    mustHaveSkills: List[str]
    niceToHaveSkills: List[str]
    status: str
    createdAt: str
    updatedAt: str

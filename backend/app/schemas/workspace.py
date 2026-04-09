from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class HiringRoleType(str, Enum):
    ENGINEERING = "engineering"
    DESIGN = "design"
    PRODUCT = "product"
    MARKETING = "marketing"
    SALES = "sales"
    HR = "hr"
    OPERATIONS = "operations"
    FINANCE = "finance"
    OTHER = "other"

class HiringVolume(str, Enum):
    SMALL = "small"  # 1-5 hires
    MEDIUM = "medium"  # 6-20 hires
    LARGE = "large"  # 21-50 hires
    ENTERPRISE = "enterprise"  # 50+ hires

class OnboardingStep(str, Enum):
    PROFILE = "profile"
    TEAM = "team"
    PREFERENCES = "preferences"
    INTEGRATION = "integration"
    COMPLETED = "completed"

class WorkspaceUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=100)
    companySize: Optional[str] = Field(None, max_length=50)
    hiringGoals: Optional[str] = Field(None, max_length=500)
    hiringRoleTypes: Optional[List[HiringRoleType]] = None
    hiringVolume: Optional[HiringVolume] = None
    onboardingStep: Optional[OnboardingStep] = None
    onboardingCompleted: Optional[bool] = None

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    companySize: Optional[str] = None
    hiringGoals: Optional[str] = None
    hiringRoleTypes: Optional[List[str]] = None
    hiringVolume: Optional[str] = None
    onboardingStep: Optional[str] = None
    onboardingCompleted: Optional[bool] = None
    createdAt: str
    updatedAt: str

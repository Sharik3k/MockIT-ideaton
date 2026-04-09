from pydantic import BaseModel, Field
from typing import List, Optional

class MockMatchRequest(BaseModel):
    candidateId: str = Field(..., min_length=1)
    vacancyId: str = Field(..., min_length=1)

class MockMatchResponse(BaseModel):
    overallMatchScore: int = Field(..., ge=0, le=100)
    matchedSkills: List[str]
    missingSkills: List[str]
    partialSkills: Optional[List[str]] = None
    risks: List[str]

class MockQuestionsRequest(BaseModel):
    candidateId: str = Field(..., min_length=1)
    vacancyId: str = Field(..., min_length=1)

class QuestionItem(BaseModel):
    category: str
    question: str
    whyGenerated: str

class MockQuestionsResponse(BaseModel):
    questions: List[QuestionItem]

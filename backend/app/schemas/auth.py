from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegisterRequest(BaseModel):
    fullName: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    companyName: str = Field(..., min_length=1, max_length=100)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: str
    fullName: str
    email: str
    createdAt: str
    updatedAt: str

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    companySize: Optional[str] = None
    createdAt: str
    updatedAt: str

class AuthResponse(BaseModel):
    user: UserResponse
    workspace: WorkspaceResponse
    token: str

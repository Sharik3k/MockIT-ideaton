from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from ..schemas.auth import UserRegisterRequest, UserLoginRequest, AuthResponse, UserResponse, WorkspaceResponse
from ..services.auth_service import register_user, login_user, get_current_user, logout_user
from ..core.store import store

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

async def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current user from token."""
    token = credentials.credentials
    user = get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

def get_user_workspace(user: Dict[str, Any]) -> Dict[str, Any]:
    """Get user's workspace."""
    for workspace in store.WORKSPACES.values():
        if workspace.get("userId") == user["id"]:
            return workspace
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Workspace not found"
    )

@router.post("/register", response_model=AuthResponse)
async def register(request: UserRegisterRequest):
    """Register a new user."""
    try:
        result = register_user(
            full_name=request.fullName,
            email=request.email,
            password=request.password,
            company_name=request.companyName
        )
        
        return AuthResponse(
            user=UserResponse(**result["user"]),
            workspace=WorkspaceResponse(**result["workspace"]),
            token=result["token"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=AuthResponse)
async def login(request: UserLoginRequest):
    """Login user."""
    try:
        result = login_user(
            email=request.email,
            password=request.password
        )
        
        if not result["workspace"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )
        
        return AuthResponse(
            user=UserResponse(**result["user"]),
            workspace=WorkspaceResponse(**result["workspace"]),
            token=result["token"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me")
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user_dependency)):
    """Get current user and workspace."""
    workspace = get_user_workspace(current_user)
    
    return {
        "user": UserResponse(**current_user),
        "workspace": WorkspaceResponse(**workspace)
    }

@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user_dependency)):
    """Logout user."""
    # In a real implementation, you'd get the token from the request
    # For now, we'll just return success
    return {"message": "Logged out successfully"}

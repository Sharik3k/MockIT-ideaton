from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from ..schemas.workspace import WorkspaceResponse, WorkspaceUpdateRequest
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace, update_workspace

router = APIRouter(prefix="/workspace", tags=["workspace"])

@router.get("", response_model=WorkspaceResponse)
async def get_workspace(current_user: Dict[str, Any] = Depends(get_current_user_dependency)):
    """Get current user's workspace."""
    workspace = get_user_workspace(current_user["id"])
    return WorkspaceResponse(**workspace)

@router.patch("", response_model=WorkspaceResponse)
async def update_workspace_endpoint(
    request: WorkspaceUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Update workspace."""
    workspace = get_user_workspace(current_user["id"])
    
    # Filter out None values
    updates = {k: v for k, v in request.dict().items() if v is not None}
    
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        updated_workspace = update_workspace(workspace["id"], updates)
        return WorkspaceResponse(**updated_workspace)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

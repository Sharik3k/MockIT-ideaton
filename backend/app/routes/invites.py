from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from ..schemas.invite import InviteCreateRequest, InviteResponse
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace
from ..services.invite_service import create_invite, get_workspace_invites, update_invite_status

router = APIRouter(prefix="/workspace/invites", tags=["invites"])

def get_workspace_from_user(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """Get workspace from current user."""
    return get_user_workspace(current_user["id"])

@router.post("", response_model=InviteResponse)
async def create_invite_endpoint(
    request: InviteCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Create a new team invite."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        invite = create_invite(
            workspace_id=workspace["id"],
            email=request.email,
            role=request.role,
            message=request.message,
            invited_by=current_user["id"]
        )
        return InviteResponse(**invite)
    except ValueError as e:
        if "already exists" in str(e).lower() or "already sent" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

@router.get("", response_model=List[InviteResponse])
async def get_invites_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get all invites for current workspace."""
    workspace = get_workspace_from_user(current_user)
    
    invites = get_workspace_invites(workspace["id"])
    return [InviteResponse(**invite) for invite in invites]

@router.patch("/{invite_id}", response_model=InviteResponse)
async def update_invite_endpoint(
    invite_id: str,
    status: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Update invite status (accept/decline)."""
    workspace = get_workspace_from_user(current_user)
    
    if status not in ["accepted", "declined", "expired"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be 'accepted', 'declined', or 'expired'"
        )
    
    try:
        invite = update_invite_status(invite_id, workspace["id"], status)
        return InviteResponse(**invite)
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )

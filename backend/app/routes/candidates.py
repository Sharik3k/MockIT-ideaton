from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from ..schemas.candidate import (
    CandidateCreateRequest, CandidateUpdateRequest, CandidateResponse
)
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace
from ..services.candidate_service import (
    create_candidate, get_candidate, get_workspace_candidates, update_candidate
)

router = APIRouter(prefix="/candidates", tags=["candidates"])

def get_workspace_from_user(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """Get workspace from current user."""
    return get_user_workspace(current_user["id"])

@router.post("", response_model=CandidateResponse)
async def create_candidate_endpoint(
    request: CandidateCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Create a new candidate."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        candidate = create_candidate(
            workspace_id=workspace["id"],
            candidate_data=request.dict()
        )
        return CandidateResponse(**candidate)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("", response_model=List[CandidateResponse])
async def get_candidates_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get all candidates for current workspace."""
    workspace = get_workspace_from_user(current_user)
    
    candidates = get_workspace_candidates(workspace["id"])
    return [CandidateResponse(**candidate) for candidate in candidates]

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate_endpoint(
    candidate_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get candidate by ID."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        candidate = get_candidate(candidate_id, workspace["id"])
        return CandidateResponse(**candidate)
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

@router.patch("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate_endpoint(
    candidate_id: str,
    request: CandidateUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Update candidate."""
    workspace = get_workspace_from_user(current_user)
    
    # Filter out None values
    updates = {k: v for k, v in request.dict().items() if v is not None}
    
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        candidate = update_candidate(candidate_id, workspace["id"], updates)
        return CandidateResponse(**candidate)
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

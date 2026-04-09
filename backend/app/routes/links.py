from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from ..schemas.link import LinkCreateRequest, LinkResponse
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace
from ..services.link_service import (
    create_link, get_vacancy_links, get_candidate_links
)

router = APIRouter(prefix="/links", tags=["links"])

def get_workspace_from_user(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """Get workspace from current user."""
    return get_user_workspace(current_user["id"])

@router.post("", response_model=LinkResponse)
async def create_link_endpoint(
    request: LinkCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Create a new candidate-vacancy link."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        link = create_link(
            workspace_id=workspace["id"],
            candidate_id=request.candidateId,
            vacancy_id=request.vacancyId,
            current_stage=request.currentStage
        )
        return LinkResponse(**link)
    except ValueError as e:
        if "already linked" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

@router.get("/vacancies/{vacancy_id}/candidates", response_model=List[LinkResponse])
async def get_vacancy_candidates_endpoint(
    vacancy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get all linked candidates for a vacancy."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        links = get_vacancy_links(vacancy_id, workspace["id"])
        return [LinkResponse(**link) for link in links]
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vacancy not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

@router.get("/candidates/{candidate_id}/vacancies", response_model=List[LinkResponse])
async def get_candidate_vacancies_endpoint(
    candidate_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get all linked vacancies for a candidate."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        links = get_candidate_links(candidate_id, workspace["id"])
        return [LinkResponse(**link) for link in links]
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

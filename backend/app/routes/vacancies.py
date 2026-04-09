from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from ..schemas.vacancy import (
    VacancyCreateRequest, VacancyUpdateRequest, VacancyResponse
)
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace
from ..services.vacancy_service import (
    create_vacancy, get_vacancy, get_workspace_vacancies, update_vacancy
)

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

def get_workspace_from_user(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """Get workspace from current user."""
    return get_user_workspace(current_user["id"])

@router.post("", response_model=VacancyResponse)
async def create_vacancy_endpoint(
    request: VacancyCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Create a new vacancy."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        vacancy = create_vacancy(
            workspace_id=workspace["id"],
            vacancy_data=request.dict()
        )
        return VacancyResponse(**vacancy)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("", response_model=List[VacancyResponse])
async def get_vacancies_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get all vacancies for current workspace."""
    workspace = get_workspace_from_user(current_user)
    
    vacancies = get_workspace_vacancies(workspace["id"])
    return [VacancyResponse(**vacancy) for vacancy in vacancies]

@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def get_vacancy_endpoint(
    vacancy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get vacancy by ID."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        vacancy = get_vacancy(vacancy_id, workspace["id"])
        return VacancyResponse(**vacancy)
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

@router.patch("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy_endpoint(
    vacancy_id: str,
    request: VacancyUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Update vacancy."""
    workspace = get_workspace_from_user(current_user)
    
    # Filter out None values
    updates = {k: v for k, v in request.dict().items() if v is not None}
    
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        vacancy = update_vacancy(vacancy_id, workspace["id"], updates)
        return VacancyResponse(**vacancy)
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

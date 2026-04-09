from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.analysis import MockMatchRequest, MockMatchResponse, MockQuestionsRequest, MockQuestionsResponse
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace
from ..services.analysis_service import mock_match_analysis, mock_questions_analysis

router = APIRouter(prefix="/analysis", tags=["analysis"])

def get_workspace_from_user(current_user: dict) -> dict:
    """Get workspace from current user."""
    return get_user_workspace(current_user["id"])

@router.post("/mock-match", response_model=MockMatchResponse)
async def mock_match_endpoint(
    request: MockMatchRequest,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Generate mock match analysis between candidate and vacancy."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        result = mock_match_analysis(
            candidate_id=request.candidateId,
            vacancy_id=request.vacancyId,
            workspace_id=workspace["id"]
        )
        return result
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

@router.post("/mock-questions", response_model=MockQuestionsResponse)
async def mock_questions_endpoint(
    request: MockQuestionsRequest,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Generate mock interview questions for candidate-vacancy pair."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        result = mock_questions_analysis(
            candidate_id=request.candidateId,
            vacancy_id=request.vacancyId,
            workspace_id=workspace["id"]
        )
        return result
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

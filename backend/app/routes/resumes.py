from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Dict, Any, List

from ..schemas.resume import ResumeResponse
from ..routes.auth import get_current_user_dependency
from ..services.workspace_service import get_user_workspace
from ..services.candidate_service import get_candidate
from ..services.resume_service import (
    validate_file_type, save_uploaded_file, create_resume, get_candidate_resumes
)
from ..core.config import settings

router = APIRouter(prefix="/candidates/{candidate_id}/resumes", tags=["resumes"])

def get_workspace_from_user(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """Get workspace from current user."""
    return get_user_workspace(current_user["id"])

@router.post("", response_model=ResumeResponse)
async def upload_resume(
    candidate_id: str,
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Upload a resume for a candidate."""
    workspace = get_workspace_from_user(current_user)
    
    # Verify candidate exists and belongs to workspace
    try:
        get_candidate(candidate_id, workspace["id"])
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
    
    # Validate file type
    if not validate_file_type(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Allowed types: {settings.ALLOWED_RESUME_TYPES}"
        )
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Save file
        stored_filename = save_uploaded_file(
            file_content, file.filename, file.content_type
        )
        
        # Create resume record
        resume = create_resume(
            candidate_id=candidate_id,
            workspace_id=workspace["id"],
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type,
            file_size=len(file_content)
        )
        
        return ResumeResponse(**resume)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload resume"
        )

@router.get("", response_model=List[ResumeResponse])
async def get_candidate_resumes_endpoint(
    candidate_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get all resumes for a candidate."""
    workspace = get_workspace_from_user(current_user)
    
    try:
        resumes = get_candidate_resumes(candidate_id, workspace["id"])
        return [ResumeResponse(**resume) for resume in resumes]
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

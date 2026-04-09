import os
import uuid
from typing import Dict, Any, List
from ..core.store import store
from ..core.utils import generate_id
from ..core.config import settings

def ensure_upload_dir():
    """Ensure upload directory exists."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

def validate_file_type(mime_type: str) -> bool:
    """Validate file type."""
    return mime_type in settings.ALLOWED_RESUME_TYPES

def save_uploaded_file(file_content: bytes, original_filename: str, mime_type: str) -> str:
    """Save uploaded file and return stored filename."""
    ensure_upload_dir()
    
    # Generate unique filename
    file_extension = os.path.splitext(original_filename)[1]
    stored_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, stored_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return stored_filename

def create_resume(candidate_id: str, workspace_id: str, original_filename: str, 
                 stored_filename: str, mime_type: str, file_size: int) -> Dict[str, Any]:
    """Create a new resume record."""
    resume_id = generate_id()
    file_path = os.path.join(settings.UPLOAD_DIR, stored_filename)
    
    resume_data = {
        "id": resume_id,
        "candidateId": candidate_id,
        "workspaceId": workspace_id,
        "originalFilename": original_filename,
        "storedFilename": stored_filename,
        "filePath": file_path,
        "mimeType": mime_type,
        "fileSize": file_size
    }
    
    return store.create_resume(resume_data)

def get_candidate_resumes(candidate_id: str, workspace_id: str) -> List[Dict[str, Any]]:
    """Get all resumes for a candidate."""
    # First verify candidate belongs to workspace
    candidate = store.get_candidate_by_id(candidate_id)
    if not candidate or candidate.get("workspaceId") != workspace_id:
        raise ValueError("Candidate not found or access denied")
    
    return store.get_resumes_by_candidate(candidate_id)

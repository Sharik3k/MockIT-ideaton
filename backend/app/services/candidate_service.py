from typing import Dict, Any, List
from ..core.store import store
from ..core.utils import generate_id

def create_candidate(workspace_id: str, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new candidate."""
    candidate_id = generate_id()
    
    full_candidate_data = {
        "id": candidate_id,
        "workspaceId": workspace_id,
        **candidate_data
    }
    
    return store.create_candidate(full_candidate_data)

def get_candidate(candidate_id: str, workspace_id: str) -> Dict[str, Any]:
    """Get candidate by ID."""
    candidate = store.get_candidate_by_id(candidate_id)
    if not candidate:
        raise ValueError("Candidate not found")
    
    if candidate.get("workspaceId") != workspace_id:
        raise ValueError("Access denied")
    
    return candidate

def get_workspace_candidates(workspace_id: str) -> List[Dict[str, Any]]:
    """Get all candidates for a workspace."""
    return store.get_candidates_by_workspace(workspace_id)

def update_candidate(candidate_id: str, workspace_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update candidate."""
    # First check if candidate exists and belongs to workspace
    candidate = get_candidate(candidate_id, workspace_id)
    
    updated_candidate = store.update_candidate(candidate_id, updates)
    if not updated_candidate:
        raise ValueError("Failed to update candidate")
    
    return updated_candidate

from typing import Dict, Any, List
from ..core.store import store
from ..core.utils import generate_id

def create_link(workspace_id: str, candidate_id: str, vacancy_id: str, current_stage: str) -> Dict[str, Any]:
    """Create a new candidate-vacancy link."""
    # Check if link already exists
    existing_link = store.get_link_by_candidate_and_vacancy(candidate_id, vacancy_id)
    if existing_link:
        raise ValueError("Candidate is already linked to this vacancy")
    
    # Verify candidate and vacancy belong to workspace
    candidate = store.get_candidate_by_id(candidate_id)
    if not candidate or candidate.get("workspaceId") != workspace_id:
        raise ValueError("Candidate not found or access denied")
    
    vacancy = store.get_vacancy_by_id(vacancy_id)
    if not vacancy or vacancy.get("workspaceId") != workspace_id:
        raise ValueError("Vacancy not found or access denied")
    
    link_id = generate_id()
    
    link_data = {
        "id": link_id,
        "workspaceId": workspace_id,
        "candidateId": candidate_id,
        "vacancyId": vacancy_id,
        "currentStage": current_stage
    }
    
    return store.create_link(link_data)

def get_vacancy_links(vacancy_id: str, workspace_id: str) -> List[Dict[str, Any]]:
    """Get all links for a vacancy."""
    # Verify vacancy belongs to workspace
    vacancy = store.get_vacancy_by_id(vacancy_id)
    if not vacancy or vacancy.get("workspaceId") != workspace_id:
        raise ValueError("Vacancy not found or access denied")
    
    return store.get_links_by_vacancy(vacancy_id)

def get_candidate_links(candidate_id: str, workspace_id: str) -> List[Dict[str, Any]]:
    """Get all links for a candidate."""
    # Verify candidate belongs to workspace
    candidate = store.get_candidate_by_id(candidate_id)
    if not candidate or candidate.get("workspaceId") != workspace_id:
        raise ValueError("Candidate not found or access denied")
    
    return store.get_links_by_candidate(candidate_id)

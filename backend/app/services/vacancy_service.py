from typing import Dict, Any, List
from ..core.store import store
from ..core.utils import generate_id

def create_vacancy(workspace_id: str, vacancy_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new vacancy."""
    vacancy_id = generate_id()
    
    full_vacancy_data = {
        "id": vacancy_id,
        "workspaceId": workspace_id,
        **vacancy_data,
        "status": vacancy_data.get("status", "active")
    }
    
    return store.create_vacancy(full_vacancy_data)

def get_vacancy(vacancy_id: str, workspace_id: str) -> Dict[str, Any]:
    """Get vacancy by ID."""
    vacancy = store.get_vacancy_by_id(vacancy_id)
    if not vacancy:
        raise ValueError("Vacancy not found")
    
    if vacancy.get("workspaceId") != workspace_id:
        raise ValueError("Access denied")
    
    return vacancy

def get_workspace_vacancies(workspace_id: str) -> List[Dict[str, Any]]:
    """Get all vacancies for a workspace."""
    return store.get_vacancies_by_workspace(workspace_id)

def update_vacancy(vacancy_id: str, workspace_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update vacancy."""
    # First check if vacancy exists and belongs to workspace
    vacancy = get_vacancy(vacancy_id, workspace_id)
    
    updated_vacancy = store.update_vacancy(vacancy_id, updates)
    if not updated_vacancy:
        raise ValueError("Failed to update vacancy")
    
    return updated_vacancy

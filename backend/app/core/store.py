from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

# In-memory data stores
USERS: Dict[str, Dict[str, Any]] = {}
WORKSPACES: Dict[str, Dict[str, Any]] = {}
SESSIONS: Dict[str, str] = {}  # token -> user_id
VACANCIES: Dict[str, Dict[str, Any]] = {}
CANDIDATES: Dict[str, Dict[str, Any]] = {}
RESUMES: Dict[str, Dict[str, Any]] = {}
LINKS: Dict[str, Dict[str, Any]] = {}
INVITES: Dict[str, Dict[str, Any]] = {}

class InMemoryStore:
    """Central in-memory data store for the hackathon MVP."""
    
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        user_id = user_data["id"]
        USERS[user_id] = {
            **user_data,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        return USERS[user_id]
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        for user in USERS.values():
            if user.get("email") == email:
                return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        return USERS.get(user_id)
    
    @staticmethod
    def create_session(token: str, user_id: str) -> None:
        """Create a new session."""
        SESSIONS[token] = user_id
    
    @staticmethod
    def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
        """Get user by session token."""
        user_id = SESSIONS.get(token)
        if user_id:
            return USERS.get(user_id)
        return None
    
    @staticmethod
    def delete_session(token: str) -> None:
        """Delete a session."""
        SESSIONS.pop(token, None)
    
    @staticmethod
    def create_workspace(workspace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workspace."""
        workspace_id = workspace_data["id"]
        WORKSPACES[workspace_id] = {
            **workspace_data,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        return WORKSPACES[workspace_id]
    
    @staticmethod
    def get_workspace_by_id(workspace_id: str) -> Optional[Dict[str, Any]]:
        """Get workspace by ID."""
        return WORKSPACES.get(workspace_id)
    
    @staticmethod
    def update_workspace(workspace_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update workspace."""
        if workspace_id in WORKSPACES:
            WORKSPACES[workspace_id].update({
                **updates,
                "updatedAt": datetime.utcnow().isoformat()
            })
            return WORKSPACES[workspace_id]
        return None
    
    @staticmethod
    def create_vacancy(vacancy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new vacancy."""
        vacancy_id = vacancy_data["id"]
        VACANCIES[vacancy_id] = {
            **vacancy_data,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        return VACANCIES[vacancy_id]
    
    @staticmethod
    def get_vacancy_by_id(vacancy_id: str) -> Optional[Dict[str, Any]]:
        """Get vacancy by ID."""
        return VACANCIES.get(vacancy_id)
    
    @staticmethod
    def get_vacancies_by_workspace(workspace_id: str) -> List[Dict[str, Any]]:
        """Get all vacancies for a workspace."""
        return [v for v in VACANCIES.values() if v.get("workspaceId") == workspace_id]
    
    @staticmethod
    def update_vacancy(vacancy_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update vacancy."""
        if vacancy_id in VACANCIES:
            VACANCIES[vacancy_id].update({
                **updates,
                "updatedAt": datetime.utcnow().isoformat()
            })
            return VACANCIES[vacancy_id]
        return None
    
    @staticmethod
    def create_candidate(candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new candidate."""
        candidate_id = candidate_data["id"]
        CANDIDATES[candidate_id] = {
            **candidate_data,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        return CANDIDATES[candidate_id]
    
    @staticmethod
    def get_candidate_by_id(candidate_id: str) -> Optional[Dict[str, Any]]:
        """Get candidate by ID."""
        return CANDIDATES.get(candidate_id)
    
    @staticmethod
    def get_candidates_by_workspace(workspace_id: str) -> List[Dict[str, Any]]:
        """Get all candidates for a workspace."""
        return [c for c in CANDIDATES.values() if c.get("workspaceId") == workspace_id]
    
    @staticmethod
    def update_candidate(candidate_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update candidate."""
        if candidate_id in CANDIDATES:
            CANDIDATES[candidate_id].update({
                **updates,
                "updatedAt": datetime.utcnow().isoformat()
            })
            return CANDIDATES[candidate_id]
        return None
    
    @staticmethod
    def create_resume(resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new resume record."""
        resume_id = resume_data["id"]
        RESUMES[resume_id] = {
            **resume_data,
            "uploadedAt": datetime.utcnow().isoformat()
        }
        return RESUMES[resume_id]
    
    @staticmethod
    def get_resumes_by_candidate(candidate_id: str) -> List[Dict[str, Any]]:
        """Get all resumes for a candidate."""
        return [r for r in RESUMES.values() if r.get("candidateId") == candidate_id]
    
    @staticmethod
    def create_link(link_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new candidate-vacancy link."""
        link_id = link_data["id"]
        LINKS[link_id] = {
            **link_data,
            "appliedAt": datetime.utcnow().isoformat()
        }
        return LINKS[link_id]
    
    @staticmethod
    def get_links_by_vacancy(vacancy_id: str) -> List[Dict[str, Any]]:
        """Get all links for a vacancy."""
        return [l for l in LINKS.values() if l.get("vacancyId") == vacancy_id]
    
    @staticmethod
    def get_links_by_candidate(candidate_id: str) -> List[Dict[str, Any]]:
        """Get all links for a candidate."""
        return [l for l in LINKS.values() if l.get("candidateId") == candidate_id]
    
    @staticmethod
    def get_link_by_candidate_and_vacancy(candidate_id: str, vacancy_id: str) -> Optional[Dict[str, Any]]:
        """Get link by candidate and vacancy."""
        for link in LINKS.values():
            if link.get("candidateId") == candidate_id and link.get("vacancyId") == vacancy_id:
                return link
        return None
    
    @staticmethod
    def create_invite(invite_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new team invite."""
        invite_id = invite_data["id"]
        INVITES[invite_id] = invite_data
        return INVITES[invite_id]
    
    @staticmethod
    def get_workspace_invites(workspace_id: str) -> List[Dict[str, Any]]:
        """Get all invites for a workspace."""
        return [invite for invite in INVITES.values() if invite.get("workspaceId") == workspace_id]
    
    @staticmethod
    def get_invite_by_id(invite_id: str) -> Optional[Dict[str, Any]]:
        """Get invite by ID."""
        return INVITES.get(invite_id)
    
    @staticmethod
    def update_invite(invite_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update invite."""
        if invite_id in INVITES:
            INVITES[invite_id].update(updates)
            return INVITES[invite_id]
        return None

# Global store instance
store = InMemoryStore()

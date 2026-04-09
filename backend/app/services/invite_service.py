from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..core.store import store
from ..core.utils import generate_id

def create_invite(workspace_id: str, email: str, role: str, message: str, invited_by: str) -> Dict[str, Any]:
    """Create a new team invite."""
    # Check if user already exists
    existing_user = store.get_user_by_email(email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Check if invite already exists
    existing_invites = store.get_workspace_invites(workspace_id)
    for invite in existing_invites:
        if invite.get("email") == email and invite.get("status") == "pending":
            raise ValueError("Invite already sent to this email")
    
    invite_id = generate_id()
    expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
    
    invite_data = {
        "id": invite_id,
        "workspaceId": workspace_id,
        "email": email,
        "role": role,
        "status": "pending",
        "message": message,
        "invitedBy": invited_by,
        "createdAt": datetime.utcnow().isoformat(),
        "expiresAt": expires_at
    }
    
    return store.create_invite(invite_data)

def get_workspace_invites(workspace_id: str) -> List[Dict[str, Any]]:
    """Get all invites for a workspace."""
    return store.get_workspace_invites(workspace_id)

def update_invite_status(invite_id: str, workspace_id: str, status: str) -> Dict[str, Any]:
    """Update invite status."""
    invite = store.get_invite_by_id(invite_id)
    if not invite:
        raise ValueError("Invite not found")
    
    if invite.get("workspaceId") != workspace_id:
        raise ValueError("Access denied")
    
    updated_invite = store.update_invite(invite_id, {"status": status})
    if not updated_invite:
        raise ValueError("Failed to update invite")
    
    return updated_invite

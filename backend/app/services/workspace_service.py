from typing import Dict, Any, List
from ..core.store import store

def get_user_workspace(user_id: str) -> Dict[str, Any]:
    """Get user's workspace."""
    for workspace in store.WORKSPACES.values():
        if workspace.get("userId") == user_id:
            return workspace
    raise ValueError("Workspace not found")

def update_workspace(workspace_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update workspace."""
    updated_workspace = store.update_workspace(workspace_id, updates)
    if not updated_workspace:
        raise ValueError("Workspace not found")
    return updated_workspace

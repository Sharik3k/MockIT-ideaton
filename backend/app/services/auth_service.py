from typing import Optional, Dict, Any
import hashlib
from ..core.store import store
from ..core.utils import generate_id, generate_token

def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == hashed

def register_user(full_name: str, email: str, password: str, company_name: str) -> Dict[str, Any]:
    """Register a new user and create workspace."""
    # Check if user already exists
    existing_user = store.get_user_by_email(email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Create user
    user_id = generate_id()
    hashed_password = hash_password(password)
    
    user_data = {
        "id": user_id,
        "fullName": full_name,
        "email": email,
        "password": hashed_password
    }
    
    user = store.create_user(user_data)
    
    # Create workspace
    workspace_id = generate_id()
    workspace_data = {
        "id": workspace_id,
        "name": company_name,
        "userId": user_id,  # Link workspace to user
        "hiringGoals": None,
        "hiringRoleTypes": [],
        "hiringVolume": None,
        "onboardingStep": "profile",
        "onboardingCompleted": False
    }
    
    workspace = store.create_workspace(workspace_data)
    
    # Create session token
    token = generate_token()
    store.create_session(token, user_id)
    
    return {
        "user": user,
        "workspace": workspace,
        "token": token
    }

def login_user(email: str, password: str) -> Dict[str, Any]:
    """Login user and return token."""
    user = store.get_user_by_email(email)
    if not user:
        raise ValueError("Invalid email or password")
    
    if not verify_password(password, user["password"]):
        raise ValueError("Invalid email or password")
    
    # Create session token
    token = generate_token()
    store.create_session(token, user["id"])
    
    # Get user's workspace
    workspace = None
    for ws in store.WORKSPACES.values():
        if ws.get("userId") == user["id"]:
            workspace = ws
            break
    
    return {
        "user": user,
        "workspace": workspace,
        "token": token
    }

def get_current_user(token: str) -> Optional[Dict[str, Any]]:
    """Get current user from token."""
    return store.get_user_by_token(token)

def logout_user(token: str) -> None:
    """Logout user by deleting session."""
    store.delete_session(token)

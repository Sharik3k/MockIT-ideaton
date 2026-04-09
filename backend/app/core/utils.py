import uuid
import secrets
from datetime import datetime
from typing import Any, Dict

def generate_id() -> str:
    """Generate a unique ID using UUID4."""
    return str(uuid.uuid4())

def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)

def get_timestamp() -> str:
    """Get current ISO timestamp."""
    return datetime.utcnow().isoformat()

def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary."""
    return data.get(key, default)

def validate_email(email: str) -> bool:
    """Simple email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

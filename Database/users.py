# database/users.py
from typing import Optional, Dict, Any, Tuple
from .supabase_client import get_supabase_client, unwrap_response

def sign_up(email: str, password: str, display_name: Optional[str] = None) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Register a new user. Optional display_name will be stored in user_metadata.
    Returns (data, error). "data" typically contains { "user": ..., "session": ... } (or user only if email confirm required).
    """
    supabase = get_supabase_client()
    payload = {"email": email, "password": password}
    if display_name:
        payload["options"] = {"data": {"display_name": display_name}}
    res = supabase.auth.sign_up(payload)
    return unwrap_response(res)

def sign_in(email: str, password: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Sign in a user using email+password.
    Returns (data, error). data usually contains 'user' and 'session' depending on project settings.
    """
    supabase = get_supabase_client()
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return unwrap_response(res)

def sign_out() -> Tuple[Optional[Dict], Optional[Dict]]:
    """Sign the currently authenticated user out on the client instance."""
    supabase = get_supabase_client()
    res = supabase.auth.sign_out()
    return unwrap_response(res)

def get_user(access_token: Optional[str] = None) -> Optional[Dict]:
    """
    Get user info. If access_token provided, uses it; otherwise uses local client session.
    Returns user dict or None.
    """
    supabase = get_supabase_client()
    if access_token:
        res = supabase.auth.get_user(access_token)
    else:
        res = supabase.auth.get_user()
    data, error = unwrap_response(res)
    if not data:
        return None
    # data may be { "user": {...} } or the user itself depending on the client; handle both.
    if isinstance(data, dict) and "user" in data:
        return data["user"]
    return data

def update_user_metadata(attributes: Dict[str, Any]) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Update the currently signed-in user's attributes (e.g. user_metadata).
    Example: update_user_metadata({"data": {"display_name": "New Name"}})
    Note: the user needs to be signed in for this to work.
    """
    supabase = get_supabase_client()
    res = supabase.auth.update_user(attributes)
    return unwrap_response(res)

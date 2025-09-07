# database/messages.py
from typing import Optional, List, Dict, Tuple
from .supabase_client import get_supabase_client, unwrap_response

TABLE = "messages"

def save_message(case_id: str, role: str, message: str) -> Tuple[Optional[List[Dict]], Optional[Dict]]:
    """
    Insert a message (role is 'user' or 'assistant').
    """
    supabase = get_supabase_client()
    payload = {"case_id": case_id, "role": role, "message": message}
    res = supabase.table(TABLE).insert(payload).execute()
    return unwrap_response(res)

def get_case_messages(case_id: str) -> Optional[List[Dict]]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).select("*").eq("case_id", case_id).order("created_at").execute()
    data, err = unwrap_response(res)
    return data

def get_latest_messages(case_id: str, limit: int = 50) -> Optional[List[Dict]]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).select("*").eq("case_id", case_id).order("created_at", desc=True).limit(limit).execute()
    data, err = unwrap_response(res)
    # result currently desc; reverse to chronological if you want ascending
    if data:
        return list(reversed(data))
    return data

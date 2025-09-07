# database/cases.py
from typing import Optional, List, Dict, Tuple
from .supabase_client import get_supabase_client, unwrap_response

TABLE = "cases"

def create_case(case_id: str, user_id: str, title: str = "New Case") -> Tuple[Optional[List[Dict]], Optional[Dict]]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).insert({"id": case_id, "user_id": user_id, "title": title}).execute()
    return unwrap_response(res)

def get_user_cases(user_id: str) -> Optional[List[Dict]]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).select("*").eq("user_id", user_id).order("created_at").execute()
    data, err = unwrap_response(res)
    return data

def get_case(case_id: str) -> Optional[Dict]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).select("*").eq("id", case_id).single().execute()
    data, err = unwrap_response(res)
    return data

def update_case_title(case_id: str, new_title: str) -> Tuple[Optional[List[Dict]], Optional[Dict]]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).update({"title": new_title}).eq("id", case_id).execute()
    return unwrap_response(res)

def delete_case(case_id: str) -> Tuple[Optional[List[Dict]], Optional[Dict]]:
    supabase = get_supabase_client()
    res = supabase.table(TABLE).delete().eq("id", case_id).execute()
    return unwrap_response(res)

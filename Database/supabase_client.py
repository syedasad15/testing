# database/supabase_client.py
import os
from typing import Any, Tuple, Optional
import streamlit as st
from supabase import create_client
from supabase import Client
from dotenv import load_dotenv

# Path to key1.env (same folder as gpt_client.py)
# module-level cached client
_supabase: Optional[Client] = None
def get_supabase_client() -> Client:
    """Return a cached Supabase client. Reads creds from keys.env."""
    global _supabase
    if _supabase is None:
        
        env_path = os.path.join(os.path.dirname(__file__), "keys.env")
        load_dotenv(env_path)

        url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
        key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

        if not url or not key:
            raise RuntimeError("Supabase credentials not found in keys.env.")

        _supabase = create_client(url, key)

    return _supabase


def unwrap_response(res: Any) -> Tuple[Optional[Any], Optional[Any]]:
    """
    Normalize supabase-py response shapes.
    Returns (data, error) if present; otherwise (None, None).
    """
    if res is None:
        return None, None
    # dict-like shape: { "data": ..., "error": ... }
    if isinstance(res, dict):
        return res.get("data"), res.get("error")
    # object with .data/.error attributes
    data = getattr(res, "data", None)
    error = getattr(res, "error", None)
    return data, error

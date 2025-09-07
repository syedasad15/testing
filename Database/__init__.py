# database/__init__.py
from . import supabase_client  # ensures client utilities available
from . import users
from . import cases
from . import messages

__all__ = ["supabase_client", "users", "cases", "messages"]

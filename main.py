
# import streamlit as st
# from prompt_router import handle_user_input
# from utils import intent_classifier
# from Agents import download_agent
# from Agents.title_generator import generate_chat_title
# from Agents.ocrapp import extract_pdf_text_with_vision
# from PyPDF2 import PdfReader
# from io import BytesIO
# import uuid, hashlib, re
# from Database.supabase_client import get_supabase_client

# import streamlit as st

# # ---------- PAGE CONFIG ----------
# st.set_page_config(
#     page_title="JudiciaryGPT",
#     page_icon="⚖️",
#     layout="wide"
# )
# supabase = get_supabase_client()
# # ---------- Top-right Sign Out ----------

# def get_user_cases_with_messages(user_id: str):
#     """
#     Fetch all cases for a user, including messages for each case.
#     """
#     # Step 1: Get all cases belonging to the user
#     res_cases = supabase.table("cases").select("*").eq("user_id", user_id).order("created_at").execute()
#     cases = res_cases.data if res_cases.data else []

#     # Step 2: For each case, get its messages
#     for case in cases:
#         case_id = case["id"]
#         res_messages = supabase.table("messages").select("*").eq("case_id", case_id).order("created_at").execute()
#         case["messages"] = res_messages.data if res_messages.data else []

#     return cases

# def create_new_case(user_id: str, title: str = "New Case"):
#     case_id = str(uuid.uuid4())
#     data = {
#         "id": case_id,
#         "user_id": user_id,
#         "title": title
#     }
#     res = supabase.table("cases").insert(data).execute()

#     if not res.data or len(res.data) == 0:
#         raise Exception(f"Failed to create case. Response: {res.data}")

#     case = res.data[0]
#     case["messages"] = []
#     return case

# def add_message_to_case(case_id: str, role: str, message: str):
#     """
#     Add a message to a specific case in Supabase.
#     """
#     message_id = str(uuid.uuid4())
#     data = {
#         "id": message_id,
#         "case_id": case_id,
#         "role": role,
#         "message": message
#     }

#     res = supabase.table("messages").insert(data).execute()

#     if not res.data or len(res.data) == 0:
#         raise Exception(f"Failed to add message. Response: {res.data}")

#     return res.data[0]


# # ---------- session ----------
# # ---------- session ----------
# if "websearch_enabled" not in st.session_state:
#     st.session_state.websearch_enabled = False

# if "user" not in st.session_state:
#     # Try to restore user from Supabase session
#     st.session_state.user = None
#     supabase_session = supabase.auth.get_session()
#     if supabase_session and supabase_session.user:
#         st.session_state.user = supabase_session.user


# # ---------- AUTHENTICATION ----------
# def sign_up(email, password, display_name):
#     try:
#         response = supabase.auth.sign_up({
#             "email": email,
#             "password": password,
#             "options": {"data": {"display_name": display_name}}
#         })
#         if response.user:
#             return {"user": response.user, "error": None}
#         else:
#             return {"user": None, "error": "Signup failed. Please try again."}
#     except Exception as e:
#         return {"user": None, "error": f"❌ Signup failed: {str(e)}"}

# def sign_in(email, password):
#     try:
#         response = supabase.auth.sign_in_with_password({"email": email, "password": password})
#         if response.user:
#             st.session_state.user = response.user
#             return {"user": response.user, "error": None}
#         else:
#             return {"user": None, "error": "Login failed. Please check your credentials."}
#     except Exception as e:
#         msg = str(e)
#         if "Email not confirmed" in msg:
#             friendly_msg = "⚠️ Your email is not confirmed. Please check your inbox for the confirmation link."
#         else:
#             friendly_msg = f"❌ Login failed: {msg}"
#         return {"user": None, "error": friendly_msg}

# # ---------- LOGIN/SIGNUP UI ----------
# if st.session_state.user is None:
#     st.sidebar.title("🔑 User Authentication")
#     auth_mode = st.sidebar.radio("Choose mode", ["Sign In", "Sign Up"])

#     email = st.sidebar.text_input("Email")
#     password = st.sidebar.text_input("Password", type="password")
#     display_name = st.sidebar.text_input("Display Name") if auth_mode == "Sign Up" else None

#     if st.sidebar.button(auth_mode):
#         if auth_mode == "Sign Up":
#             result = sign_up(email, password, display_name)
#             if result["error"]:
#                 st.sidebar.error(result["error"])
#             else:
#                 st.sidebar.success("✅ Signed up! Please log in.")
#         else:
#             result = sign_in(email, password)
#             if result["error"]:
#                 st.sidebar.error(result["error"])
#             else:
#                 st.session_state.user = result["user"]
#                 st.sidebar.success(f"✅ Welcome, {st.session_state.user.user_metadata.get('display_name')}")
#                 st.session_state["rerun_trigger"] = not st.session_state.get("rerun_trigger", False)
#                 st.rerun()

#     st.stop() 
# user_id = st.session_state.user.id
# if "cases" not in st.session_state:
#     user_cases = get_user_cases_with_messages(user_id)
#     st.session_state.cases = {
#         case["id"]: {**case, "messages": case.get("messages", [])} for case in user_cases
#     }
#     st.session_state.current_case = list(st.session_state.cases.keys())[0] if user_cases else None

# if "uploaded_case_text" not in st.session_state:
#     st.session_state.uploaded_case_text = ""
# if "last_uploaded_file_hash" not in st.session_state:
#     st.session_state.last_uploaded_file_hash = None

# # # # ---------- css ----------
# st.markdown(
#     """
# <style>
# /* --- root variables --- */
# :root {
#     --brand: #2E3B55;
#     --brand-light: #3f4f70;
#     --accent: #FFD700;
#     --bg-chat: #fafbfc;
#     --bg-sidebar: #ffffff;
#     --radius: 12px;
#     --shadow: 0 2px 8px rgba(0,0,0,.08);
#     --shadow-hover: 0 4px 16px rgba(0,0,0,.12);
# }

# /* --- global --- */
# html, body, .main {
#     background-color: var(--bg-chat);
# }
# .block-container {
#     padding-top: 3rem;
#     padding-bottom: 8rem;
# }

# /* --- sidebar --- */
# [data-testid="stSidebar"] {
#     background-color: var(--bg-sidebar);
#     border-right: 1px solid #e5e7eb;
# }
# .sidebar-card {
#     background: #ffffff;
#     border-radius: var(--radius);
#     box-shadow: var(--shadow);
#     margin-bottom: .6rem;
#     transition: .25s;
# }
# .sidebar-card:hover {
#     box-shadow: var(--shadow-hover);
#     transform: translateY(-1px);
# }

# /* --- chat bubbles --- */
# .chat-user, .chat-assistant {
#     max-width: 80%;
#     padding: .8rem 1.1rem;
#     border-radius: var(--radius);
#     margin-bottom: .7rem;
#     animation: fadeIn .4s ease-in-out;
#     word-wrap: break-word;
# }


# .chat-user {
#     background: #e6f0fa;
#     border-left: 4px solid var(--accent);
#     margin-left: auto;
# }
# .chat-assistant {
#     background: #f6f8fa;
#     border-left:4px solid var(--brand) ;
#     margin-right: auto;
# }
# @keyframes fadeIn {
#     from {opacity: 0; transform: translateY(8px);}
#     to   {opacity: 1; transform: translateY(0);}
# }

# /* --- sticky bottom bar --- */
# .chat-bar {
#     position: fixed;
#     bottom: 0;
#     left: 0;
#     right: 0;
#     background: #ffffff;
#     border-top: 4px solid var(--brand);
#     box-shadow: 0 -2px 8px rgba(0,0,0,.05);
#     z-index: 1000;
#     padding: .8rem 2rem 1.2rem;
# }
# .chat-bar textarea {
#     border: 2px solid var(--brand);
#     border-radius: var(--radius);
#     font-size: 1rem;
# }
# .chat-bar textarea:focus {
#     border-color: var(--accent);
#     box-shadow: 0 0 0 .15rem rgba(255,215,0,.35);
# }
# .stButton>button {
#     border-radius: var(--radius);
#     font-weight: 600;
#     background: var(--brand);
#     border: none;
#     color: #fff;
#     transition: .25s;
# }
# .stButton>button:hover {
#     background: var(--brand-light);
#     transform: translateY(-1px);
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ---------- Sidebar ----------
# with st.sidebar:
#     st.markdown(
#         """
#         <div style="margin-top:-60px; font-size:32px; font-weight:bold;">⚖️ JudiciaryGPT</div>
#         """,
#         unsafe_allow_html=True
#     )
#     if st.session_state.user:
#         cols = st.columns([3, 1])  # name left, sign out right
#         with cols[0]:
#             st.markdown(
#                 f'<div style="font-size:20px; font-weight:bold;">👤 {st.session_state.user.user_metadata.get("display_name")}</div>',
#                 unsafe_allow_html=True
#             )
#         with cols[1]:
#             if st.button("Sign Out"):
#                 supabase.auth.sign_out()  # log out from Supabase session
#                 st.session_state.user = None
#                 st.session_state.cases = {}
#                 st.session_state.current_case = None
#                 st.session_state.uploaded_case_text = ""
#                 st.session_state.last_uploaded_file_hash = None
#                 st.rerun()

#     st.markdown("### 📁 Case Files")
#     if st.button("➕ New Case", use_container_width=True):
#         new_case = create_new_case(user_id)
#         st.session_state.current_case = new_case["id"]
#         st.session_state.cases[new_case["id"]] = new_case
#         st.session_state.uploaded_case_text = ""
#         st.session_state.last_uploaded_file_hash = None
#         st.rerun()

#     for cid, case in st.session_state.cases.items():
#         title = case.get("title", f"Case {cid[:8]}")
#         if st.button(title, key=f"case_{cid}", use_container_width=True):
#             st.session_state.current_case = cid
#             st.rerun()

# # ---------- Header ----------
# # st.title("⚖️ JudiciaryGPT")
# # st.caption("Interactive legal assistant for Pakistan’s judicial system.")

# # ---------- Chat Display ----------
# st.markdown("### 📜 Case Discussion & Judgments")
# current_case_id = st.session_state.current_case
# current_case = st.session_state.cases.get(current_case_id, {"messages": []})
# chat_area = st.container()
# with chat_area:
#     for idx, msg in enumerate(current_case["messages"]):
#         if msg["role"] == "user":
#             st.markdown(
#                 f'<div class="chat-user"><strong>🧑 {st.session_state.user.user_metadata.get("display_name")}:</strong><br>{msg["message"]}</div>',
#                 unsafe_allow_html=True,
#             )
#         else:
#             html_msg = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\1:</strong>", msg["message"])
#             html_msg = html_msg.replace("\n", "<br>")
#             st.markdown(
#                 f'<div class="chat-assistant"><strong>⚖️ JudiciaryGPT:</strong><br>{html_msg}</div>',
#                 unsafe_allow_html=True,
#             )

#             download_agent.show_download_if_applicable(idx, current_case["messages"], intent_classifier.classify_prompt_intent)
#     st.markdown(
#         """
#         <script>
#         const chatContainers = window.parent.document.querySelectorAll('.stContainer div[role="list"]');
#         if (chatContainers.length > 0) {
#             const lastContainer = chatContainers[chatContainers.length-1];
#             lastContainer.scrollTop = lastContainer.scrollHeight;
#         }
#         </script>
#         """,
#         unsafe_allow_html=True
#     )
# # ---------- Chat Input ----------
# with st.container():
#     st.markdown('<div class="chat-bar">', unsafe_allow_html=True)

#     with st.form(key="chat_form", clear_on_submit=True):
#         c1, c2 = st.columns([4, 1])

#         with c1:
#             user_input = st.text_area(
#                 "Enter your judicial query:",
#                 key="user_input",
#                 label_visibility="collapsed",
#                 height=100,
#                 placeholder="Type your legal query here or upload a .txt / .pdf case …",
#             )

#             col_limit, col_toggle = st.columns([3, 2])
#             with col_limit:
#                 st.markdown("<small style='color: #666;'>Limit: 10MB per file • Max 30 pages • TXT, PDF</small>", unsafe_allow_html=True)
#             with col_toggle:
#                 st.session_state.websearch_enabled = st.toggle(
#                     "Enable Web Search", value=st.session_state.websearch_enabled
#                 )

#             uploaded_file = st.file_uploader("📎 Upload Case File (.txt or .pdf)", type=["txt", "pdf"], label_visibility="collapsed")
#             if uploaded_file:
#                 max_mb = 10
#                 if uploaded_file.size > max_mb * 1024 * 1024:
#                     st.error(f"❌ File too large. Max {max_mb} MB allowed.")
#                 else:
#                     file_bytes = uploaded_file.read()
#                     file_hash = hashlib.md5(file_bytes).hexdigest()
#                     if st.session_state.last_uploaded_file_hash != file_hash:
#                         st.session_state.last_uploaded_file_hash = file_hash
#                         try:
#                             if uploaded_file.name.lower().endswith(".txt"):
#                                 st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
#                                 st.success("✅ Text file loaded.")
#                             else:
#                                 reader = PdfReader(BytesIO(file_bytes))
#                                 if len(reader.pages) > 30:
#                                     st.error("❌ PDF too long. Max 30 pages.")
#                                 else:
#                                     txt = extract_pdf_text_with_vision(file_bytes)
#                                     if not txt or len(txt.strip()) < 50:
#                                         st.error("❌ No meaningful text extracted.")
#                                     else:
#                                         st.session_state.uploaded_case_text = txt[:10_000]
#                                         st.success("✅ PDF processed.")

#                         except Exception as e:
#                             st.error(f"❌ Could not read file: {e}")

#         with c2:
#             submitted = st.form_submit_button("Submit", use_container_width=True)

#     st.markdown("</div>", unsafe_allow_html=True)

# # ---------- Query Handler ----------
# if submitted and (user_input or st.session_state.uploaded_case_text):
#     query = user_input.strip() or "Generate legal judgment"

#     current_case_id = st.session_state.current_case
#     if not current_case_id:
#         new_case = create_new_case(user_id)
#         current_case_id = new_case["id"]
#         st.session_state.current_case = current_case_id
#         st.session_state.cases[current_case_id] = new_case
#         current_case = new_case

#     with st.spinner("Processing …"):
#         response = handle_user_input(query)

#     if uploaded_file and uploaded_file.size <= 10 * 1024 * 1024:
#         add_message_to_case(current_case_id, "user", f"[📎 Uploaded: {uploaded_file.name}]")
#         current_case["messages"].append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.name}]"})

#     add_message_to_case(current_case_id, "user", query)
#     current_case["messages"].append({"role": "user", "message": query})

#     add_message_to_case(current_case_id, "assistant", response)
#     current_case["messages"].append({"role": "assistant", "message": response})

#     current_case["title"] = generate_chat_title(query) or "Untitled Case"
#     supabase.table("cases").upsert({
#         "id": current_case_id,
#         "user_id": user_id,
#         "title": current_case["title"]
#     }).execute()

#     st.rerun()



import streamlit as st
from prompt_router import handle_user_input
from utils import intent_classifier
from Agents import download_agent
from Agents.title_generator import generate_chat_title
from Agents.ocrapp import extract_pdf_text_with_vision
from PyPDF2 import PdfReader
from io import BytesIO
import uuid, hashlib, re
from Database.supabase_client import get_supabase_client
import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="JudiciaryGPT",
    page_icon="⚖️",
    layout="wide"
)

supabase = get_supabase_client()

# ================= Custom CSS (dark UI) =================
st.markdown(
    """
    <style>
    body, html, .main {
        background-color: #0e1117 !important;
        color: white !important;
    }
    .block-container {
        padding-top: 2.6rem !important;
        padding-bottom: 6rem !important;
    }
    .user-msg {
        text-align: right;
        background: rgba(59,130,246,0.2);
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        color: white;
        max-width: 70%;
        margin-left: auto;
    }
    .assistant-msg {
        text-align: left;
        background: rgba(255,255,255,0.08);
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        color: white;
        max-width: 70%;
    }
    .chatbox-container {
        position: sticky;
        bottom: 0;
        background: #0e1117;
        padding: 12px 16px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    .chatbox-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .chatbox-textarea {
        flex: 1;
        height: 70px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(255,255,255,0.05);
        color: white;
        resize: none;
        font-size: 14px;
    }
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: .15s !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DB Functions ----------
def get_user_cases_with_messages(user_id: str):
    res_cases = supabase.table("cases").select("*").eq("user_id", user_id).order("created_at").execute()
    cases = res_cases.data if res_cases.data else []
    for case in cases:
        case_id = case["id"]
        res_messages = supabase.table("messages").select("*").eq("case_id", case_id).order("created_at").execute()
        case["messages"] = res_messages.data if res_messages.data else []
    return cases

def create_new_case(user_id: str, title: str = "New Case"):
    case_id = str(uuid.uuid4())
    data = {"id": case_id, "user_id": user_id, "title": title}
    res = supabase.table("cases").insert(data).execute()
    if not res.data or len(res.data) == 0:
        raise Exception(f"Failed to create case. Response: {res.data}")
    case = res.data[0]
    case["messages"] = []
    return case

def add_message_to_case(case_id: str, role: str, message: str):
    message_id = str(uuid.uuid4())
    data = {"id": message_id, "case_id": case_id, "role": role, "message": message}
    res = supabase.table("messages").insert(data).execute()
    if not res.data or len(res.data) == 0:
        raise Exception(f"Failed to add message. Response: {res.data}")
    return res.data[0]

# ---------- Session Defaults ----------
if "websearch_enabled" not in st.session_state:
    st.session_state.websearch_enabled = False

if "user" not in st.session_state:
    st.session_state.user = None
    supabase_session = supabase.auth.get_session()
    if supabase_session and getattr(supabase_session, "user", None):
        st.session_state.user = supabase_session.user

if "attached_files" not in st.session_state:
    st.session_state.attached_files = []
if "is_web_search" not in st.session_state:
    st.session_state.is_web_search = False
if "show_add_options" not in st.session_state:
    st.session_state.show_add_options = False
if "chat_search" not in st.session_state:
    st.session_state.chat_search = ""

# ---------- AUTH ----------
def sign_up(email, password, display_name):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"display_name": display_name}}
        })
        if response.user:
            return {"user": response.user, "error": None}
        else:
            return {"user": None, "error": "Signup failed"}
    except Exception as e:
        return {"user": None, "error": f"❌ Signup failed: {str(e)}"}

def sign_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            st.session_state.user = response.user
            return {"user": response.user, "error": None}
        else:
            return {"user": None, "error": "Login failed"}
    except Exception as e:
        msg = str(e)
        return {"user": None, "error": f"❌ Login failed: {msg}"}

# ---------- LOGIN/SIGNUP ----------
if st.session_state.user is None:
    st.sidebar.title("🔑 User Authentication")
    auth_mode = st.sidebar.radio("Choose mode", ["Sign In", "Sign Up"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    display_name = st.sidebar.text_input("Display Name") if auth_mode == "Sign Up" else None

    if st.sidebar.button(auth_mode):
        if auth_mode == "Sign Up":
            result = sign_up(email, password, display_name)
            if result["error"]:
                st.sidebar.error(result["error"])
            else:
                st.sidebar.success("✅ Signed up! Please log in.")
        else:
            result = sign_in(email, password)
            if result["error"]:
                st.sidebar.error(result["error"])
            else:
                st.session_state.user = result["user"]
                st.rerun()
    st.stop()

# ---------- Load Cases ----------
user_id = st.session_state.user.id
if "cases" not in st.session_state:
    user_cases = get_user_cases_with_messages(user_id)
    st.session_state.cases = {case["id"]: {**case, "messages": case.get("messages", [])} for case in user_cases}
    st.session_state.current_case = list(st.session_state.cases.keys())[0] if user_cases else None

if "uploaded_case_text" not in st.session_state:
    st.session_state.uploaded_case_text = ""
if "last_uploaded_file_hash" not in st.session_state:
    st.session_state.last_uploaded_file_hash = None

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⚖️ JudiciaryGPT")
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown(f"👤 {st.session_state.user.user_metadata.get('display_name')}")
    with cols[1]:
        if st.button("Sign Out"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.cases = {}
            st.session_state.current_case = None
            st.session_state.uploaded_case_text = ""
            st.session_state.last_uploaded_file_hash = None
            st.rerun()
    st.markdown("### 📁 Case Files")
    if st.button("➕ New Case", use_container_width=True):
        new_case = create_new_case(user_id)
        st.session_state.current_case = new_case["id"]
        st.session_state.cases[new_case["id"]] = new_case
        st.session_state.uploaded_case_text = ""
        st.session_state.last_uploaded_file_hash = None
        st.rerun()
    for cid, case in st.session_state.cases.items():
        title = case.get("title", f"Case {cid[:8]}")
        if st.button(title, key=f"case_{cid}", use_container_width=True):
            st.session_state.current_case = cid
            st.rerun()

# ---------- Chat Display ----------
st.markdown("### 📜 Case Discussion & Judgments")
current_case_id = st.session_state.current_case
current_case = st.session_state.cases.get(current_case_id, {"messages": []})

for idx, msg in enumerate(current_case["messages"]):
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'><strong>🧑 You:</strong><br>{msg['message']}</div>", unsafe_allow_html=True)
    else:
        html_msg = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\\1:</strong>", msg["message"])
        html_msg = html_msg.replace("\n", "<br>")
        st.markdown(f"<div class='assistant-msg'><strong>⚖️ JudiciaryGPT:</strong><br>{html_msg}</div>", unsafe_allow_html=True)
        download_agent.show_download_if_applicable(idx, current_case["messages"], intent_classifier.classify_prompt_intent)

# ---------- Chat Input ----------
with st.form(key="chat_form", clear_on_submit=True):
    st.markdown('<div class="chatbox-container"><div class="chatbox-row">', unsafe_allow_html=True)
    user_input = st.text_area("Enter your judicial query:", key="user_input", label_visibility="collapsed", height=80, placeholder="✍️ Type your legal query here…")
    submitted = st.form_submit_button("📨 Send")
    st.markdown('</div></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📎 Upload Case File (.txt or .pdf)", type=["txt", "pdf"])
if uploaded_file:
    max_mb = 10
    if uploaded_file.size > max_mb * 1024 * 1024:
        st.error(f"❌ File too large. Max {max_mb} MB allowed.")
    else:
        file_bytes = uploaded_file.read()
        file_hash = hashlib.md5(file_bytes).hexdigest()
        if st.session_state.last_uploaded_file_hash != file_hash:
            st.session_state.last_uploaded_file_hash = file_hash
            try:
                if uploaded_file.name.lower().endswith(".txt"):
                    st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
                    st.success("✅ Text file loaded.")
                else:
                    reader = PdfReader(BytesIO(file_bytes))
                    if len(reader.pages) > 30:
                        st.error("❌ PDF too long. Max 30 pages.")
                    else:
                        txt = extract_pdf_text_with_vision(file_bytes)
                        if not txt or len(txt.strip()) < 50:
                            st.error("❌ No meaningful text extracted.")
                        else:
                            st.session_state.uploaded_case_text = txt[:10_000]
                            st.success("✅ PDF processed.")
            except Exception as e:
                st.error(f"❌ Could not read file: {e}")

st.session_state.websearch_enabled = st.checkbox("🌐 Enable Web Search", value=st.session_state.websearch_enabled)

# ---------- Query Handler ----------
if submitted and (user_input or st.session_state.uploaded_case_text):
    query = user_input.strip() or "Generate legal judgment"
    if not current_case_id:
        new_case = create_new_case(user_id)
        current_case_id = new_case["id"]
        st.session_state.current_case = current_case_id
        st.session_state.cases[current_case_id] = new_case
        current_case = new_case
    with st.spinner("Processing …"):
        response = handle_user_input(query)
    if uploaded_file and uploaded_file.size <= 10 * 1024 * 1024:
        add_message_to_case(current_case_id, "user", f"[📎 Uploaded: {uploaded_file.name}]")
        current_case["messages"].append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.name}]"})
    add_message_to_case(current_case_id, "user", query)
    current_case["messages"].append({"role": "user", "message": query})
    add_message_to_case(current_case_id, "assistant", response)
    current_case["messages"].append({"role": "assistant", "message": response})
    current_case["title"] = generate_chat_title(query) or "Untitled Case"
    supabase.table("cases").upsert({"id": current_case_id, "user_id": user_id, "title": current_case["title"]}).execute()
    st.rerun()

# # api.py
# from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from io import BytesIO
# from PyPDF2 import PdfReader
# import hashlib, uuid, re

# from prompt_router import handle_user_input, generate_title_from_prompt
# from utils import intent_classifier
# from Agents import download_agent

# app = FastAPI(title="PakLaw Judicial Assistant API")

# # Allow all CORS for frontend testing
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------- In-memory session store ----------
# sessions = {}

# MAX_FILE_MB = 10
# MAX_PDF_PAGES = 30
# MAX_UPLOADED_TEXT_LENGTH = 10_000


# def get_session(session_id: str):
#     if session_id not in sessions:
#         sessions[session_id] = {
#             "chats": [],
#             "chat_title": "New Case",
#             "uploaded_case_text": "",
#             "last_uploaded_file_hash": None,
#         }
#     return sessions[session_id]


# # ---------- Utility to process uploaded files ----------
# def process_uploaded_file(file: UploadFile):
#     file_bytes = file.file.read()
#     file_hash = hashlib.md5(file_bytes).hexdigest()

#     if len(file_bytes) > MAX_FILE_MB * 1024 * 1024:
#         raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_FILE_MB} MB allowed.")

#     # TXT file
#     if file.filename.lower().endswith(".txt"):
#         text = file_bytes.decode("utf-8")
#         if len(text.strip()) < 10:
#             raise HTTPException(status_code=400, detail="TXT file is empty or too short.")
#         return text, file_hash

#     # PDF file
#     elif file.filename.lower().endswith(".pdf"):
#         reader = PdfReader(BytesIO(file_bytes))
#         if len(reader.pages) > MAX_PDF_PAGES:
#             raise HTTPException(status_code=400, detail=f"PDF too long. Max {MAX_PDF_PAGES} pages.")
#         from Agents.ocrapp import extract_pdf_text_with_vision
#         text = extract_pdf_text_with_vision(file_bytes)
#         if not text or len(text.strip()) < 50:
#             raise HTTPException(status_code=400, detail="No meaningful text extracted from PDF.")
#         return text[:MAX_UPLOADED_TEXT_LENGTH], file_hash

#     else:
#         raise HTTPException(status_code=400, detail="Unsupported file type. Only TXT and PDF allowed.")


# # ---------- API Endpoints ----------

# @app.post("/chat")
# async def chat(
#     session_id: str = Form(...),
#     user_input: str = Form(None),
#     uploaded_file: UploadFile = File(None),
# ):
#     """
#     Main chat endpoint.
#     Mirrors Streamlit behavior: uploads, text, routing, and intent handling.
#     """
#     session = get_session(session_id)

#     # Process uploaded file if present
#     if uploaded_file:
#         try:
#             text, file_hash = process_uploaded_file(uploaded_file)
#         except HTTPException as e:
#             return JSONResponse(status_code=e.status_code, content={"error": e.detail})

#         if session["last_uploaded_file_hash"] != file_hash:
#             session["last_uploaded_file_hash"] = file_hash
#             session["uploaded_case_text"] = text

#         session["chats"].append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.filename}]"})


#     # Combine uploaded case text if present
#     case_text = session.get("uploaded_case_text", "")
#     final_input = user_input or "Generate legal judgment"
#     if case_text:
#         final_input = f"The following case has been uploaded:\n\n{case_text}\n\nNow respond to the user's request:\n{final_input}"

#     # Handle the user input using prompt routing
#     response = handle_user_input(final_input)

#     # Append chat messages
#     if user_input:
#         session["chats"].append({"role": "user", "message": user_input})
#     session["chats"].append({"role": "assistant", "message": response})

#     # Update chat title
#     session["chat_title"] = generate_title_from_prompt(final_input) or "Untitled Case"

#     return {
#         "session_id": session_id,
#         "chat_title": session["chat_title"],
#         "chats": session["chats"],
#     }


# @app.post("/new_session")
# async def new_session():
#     """
#     Create a new chat session (mirrors 'New Case' button in Streamlit).
#     """
#     session_id = str(uuid.uuid4())
#     get_session(session_id)  # initializes session
#     return {"session_id": session_id}


# @app.get("/sessions/{session_id}")
# async def get_session_data(session_id: str):
#     """
#     Retrieve chat and session data for a given session.
#     """
#     if session_id not in sessions:
#         raise HTTPException(status_code=404, detail="Session not found.")
#     return sessions[session_id]
 

# # api.py
# from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from io import BytesIO
# from PyPDF2 import PdfReader
# import hashlib, uuid, re

# from prompt_router import handle_user_input, generate_title_from_prompt
# from utils import intent_classifier
# from Agents import download_agent

# app = FastAPI(title="PakLaw Judicial Assistant API")

# # ---------- CORS Configuration ----------
# # CORS configuration
# origins = [
#     "*"  # Allow all origins
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

# # ---------- In-memory session store ----------
# sessions = {}

# MAX_FILE_MB = 10
# MAX_PDF_PAGES = 30
# MAX_UPLOADED_TEXT_LENGTH = 10_000


# def get_session(session_id: str):
#     if session_id not in sessions:
#         sessions[session_id] = {
#             "chats": [],
#             "chat_title": "New Case",
#             "uploaded_case_text": "",
#             "last_uploaded_file_hash": None,
#         }
#     return sessions[session_id]


# # ---------- Utility to process uploaded files ----------
# def process_uploaded_file(file: UploadFile):
#     file_bytes = file.file.read()
#     file_hash = hashlib.md5(file_bytes).hexdigest()

#     if len(file_bytes) > MAX_FILE_MB * 1024 * 1024:
#         raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_FILE_MB} MB allowed.")

#     # TXT file
#     if file.filename.lower().endswith(".txt"):
#         text = file_bytes.decode("utf-8")
#         if len(text.strip()) < 10:
#             raise HTTPException(status_code=400, detail="TXT file is empty or too short.")
#         return text, file_hash

#     # PDF file
#     elif file.filename.lower().endswith(".pdf"):
#         reader = PdfReader(BytesIO(file_bytes))
#         if len(reader.pages) > MAX_PDF_PAGES:
#             raise HTTPException(status_code=400, detail=f"PDF too long. Max {MAX_PDF_PAGES} pages.")
#         from Agents.ocrapp import extract_pdf_text_with_vision
#         text = extract_pdf_text_with_vision(file_bytes)
#         if not text or len(text.strip()) < 50:
#             raise HTTPException(status_code=400, detail="No meaningful text extracted from PDF.")
#         return text[:MAX_UPLOADED_TEXT_LENGTH], file_hash

#     else:
#         raise HTTPException(status_code=400, detail="Unsupported file type. Only TXT and PDF allowed.")


# # ---------- API Endpoints ----------

# @app.post("/chat")
# async def chat(
#     session_id: str = Form(...),
#     user_input: str = Form(None),
#     uploaded_file: UploadFile = File(None),
# ):
#     """
#     Main chat endpoint.
#     Mirrors Streamlit behavior: uploads, text, routing, and intent handling.
#     """
#     session = get_session(session_id)

#     # Process uploaded file if present
#     if uploaded_file:
#         try:
#             text, file_hash = process_uploaded_file(uploaded_file)
#         except HTTPException as e:
#             return JSONResponse(status_code=e.status_code, content={"error": e.detail})

#         if session["last_uploaded_file_hash"] != file_hash:
#             session["last_uploaded_file_hash"] = file_hash
#             session["uploaded_case_text"] = text

#         session["chats"].append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.filename}]"})

#     # Combine uploaded case text if present
#     case_text = session.get("uploaded_case_text", "")
#     final_input = user_input or "Generate legal judgment"
#     if case_text:
#         final_input = f"The following case has been uploaded:\n\n{case_text}\n\nNow respond to the user's request:\n{final_input}"

#     # Handle the user input using prompt routing
#     response = handle_user_input(final_input)

#     # Append chat messages
#     if user_input:
#         session["chats"].append({"role": "user", "message": user_input})
#     session["chats"].append({"role": "assistant", "message": response})

#     # Update chat title
#     session["chat_title"] = generate_title_from_prompt(final_input) or "Untitled Case"

#     return {
#         "session_id": session_id,
#         "chat_title": session["chat_title"],
#         "chats": session["chats"],
#     }


# @app.post("/new_session")
# async def new_session():
#     """
#     Create a new chat session (mirrors 'New Case' button in Streamlit).
#     """
#     session_id = str(uuid.uuid4())
#     get_session(session_id)  # initializes session
#     return {"session_id": session_id}


# @app.get("/sessions/{session_id}")
# async def get_session_data(session_id: str):
#     """
#     Retrieve chat and session data for a given session.
#     """
#     if session_id not in sessions:
#         raise HTTPException(status_code=404, detail="Session not found.")
#     return sessions[session_id]   BESTTTTTTTTTT


from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PyPDF2 import PdfReader
import hashlib, uuid, os
import tempfile
from prompt_router import handle_user_input
from Agents import download_agent
from Agents.ocrapp import extract_pdf_text_with_vision, extract_text_with_vision
from Agents.websearch import websearch_with_citations  # <- new import

app = FastAPI(title="PakLaw Judicial Assistant API")

# ---------- CORS Configuration ----------
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ---------- In-memory session store ----------
sessions = {}

MAX_FILE_MB = 10
MAX_PDF_PAGES = 30
MAX_UPLOADED_TEXT_LENGTH = 10_000


def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "chats": [],
            "chat_title": "New Case",
            "uploaded_case_text": "",
            "last_uploaded_file_hash": None,
        }
    return sessions[session_id]



def process_uploaded_file(file: UploadFile):
    file_bytes = file.file.read()
    file_hash = hashlib.md5(file_bytes).hexdigest()

    if len(file_bytes) > MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_FILE_MB} MB allowed.")

    filename_lower = file.filename.lower()

    if filename_lower.endswith(".txt"):
        text = file_bytes.decode("utf-8")
        if len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="TXT file is empty or too short.")
        return text, file_hash

    elif filename_lower.endswith(".pdf"):
        # PDF page count check
        print("HEllo1")
        reader = PdfReader(BytesIO(file_bytes))
        print("HEllo2")     
        if len(reader.pages) > MAX_PDF_PAGES:
            raise HTTPException(status_code=400, detail=f"PDF too long. Max {MAX_PDF_PAGES} pages.")

        # Extract text using Google Vision-based OCR
        try:
            text = extract_pdf_text_with_vision(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract text from PDF: {e}")

        if not text or len(text.strip()) < 50:
            raise HTTPException(status_code=400, detail="No meaningful text extracted from PDF.")

        return text[:MAX_UPLOADED_TEXT_LENGTH], file_hash

    elif filename_lower.endswith((".png", ".jpg", ".jpeg")):
        try:
            text = extract_text_with_vision(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract text from image: {e}")

        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="No meaningful text extracted from image.")

        return text[:MAX_UPLOADED_TEXT_LENGTH], file_hash

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only TXT, PDF, JPG, PNG allowed.")

# ---------- API Endpoints ----------

from Agents.title_generator import generate_chat_title  # <-- import this

@app.post("/chat")
async def chat(
    session_id: str = Form(...),
    user_input: str = Form(None),
    uploaded_file: UploadFile = File(None),
):
    session = get_session(session_id)

    if uploaded_file:
        try:
            text, file_hash = process_uploaded_file(uploaded_file)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})

        if session["last_uploaded_file_hash"] != file_hash:
            session["last_uploaded_file_hash"] = file_hash
            session["uploaded_case_text"] = text

        session["chats"].append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.filename}]"})

    case_text = session.get("uploaded_case_text", "")
    final_input = user_input or "Generate legal judgment"
    if case_text:
        final_input = f"The following case has been uploaded:\n\n{case_text}\n\nNow respond to the user's request:\n{final_input}"

    response = handle_user_input(final_input)

    if user_input:
        session["chats"].append({"role": "user", "message": user_input})
    session["chats"].append({"role": "assistant", "message": response})

    # ✅ use generate_chat_title here
    session["chat_title"] = generate_chat_title(final_input) or "Untitled Case"

    return {
        "session_id": session_id,
        "chat_title": session["chat_title"],
        "chats": session["chats"],
    }


@app.post("/new_session")
async def new_session():
    session_id = str(uuid.uuid4())
    get_session(session_id)
    return {"session_id": session_id}


@app.get("/sessions/{session_id}")
async def get_session_data(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    return sessions[session_id]



@app.get("/download/{session_id}")
async def download_generated_document(session_id: str):
    session = get_session(session_id)  # assume you have this function
    if not session.get("chats"):
        raise HTTPException(status_code=400, detail="No chats to generate document from.")

    # Take the last message (or modify logic to pick relevant one)
    last_idx = len(session["chats"]) - 1
    user_msg = session["chats"][last_idx - 1]["message"] if last_idx > 0 else ""
    intent = download_agent.intent_func(user_msg)  # assume you have intent_func

    # Determine filename
    if any(keyword in user_msg.lower() for keyword in ["petition", "draft petition", "generate petition"]):
        filename = "petition.txt"
    else:
        filename = f"{intent.replace(' ', '_').lower()}.txt" if intent in download_agent.DOWNLOADABLE_COMMANDS else "response.txt"

    # Get the content for download
    content = session["chats"][last_idx]["message"]

    # Save to a temporary file
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return FileResponse(file_path, filename=filename, media_type="text/plain")


@app.post("/batch_upload")
async def batch_upload(session_id: str = Form(...), uploaded_files: list[UploadFile] = File(...)):
    session = get_session(session_id)
    combined_text = ""
    for f in uploaded_files:
        try:
            text, _ = process_uploaded_file(f)
            combined_text += text + "\n\n"
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": f"{f.filename}: {e.detail}"})
    session["uploaded_case_text"] = combined_text[:MAX_UPLOADED_TEXT_LENGTH]
    return {"message": "Batch files processed successfully."}


# ---------- Web Search Endpoint ----------
@app.get("/websearch")
async def websearch_endpoint(query: str = Query(..., min_length=3, description="Search query")):
    """
    Perform a web search and return a GPT-based summary with citations.
    """
    try:
        summary = websearch_with_citations(query)
        return {"query": query, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from pydantic import BaseModel

class RenameRequest(BaseModel):
    session_id: str
    user_prompt: str

@app.post("/rename_all_chats")
async def rename_chat(req: RenameRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    new_title = generate_chat_title(req.user_prompt) or "Untitled Case"
    sessions[req.session_id]["chat_title"] = new_title

    return {
        "session_id": req.session_id,
        "new_name": new_title,
    }






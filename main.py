# main.py
from fastapi import FastAPI, Form, File, UploadFile
from construction import reply
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(
    question: str = Form(...),
    conversation_history: str = Form("[]"),   # still needed for state
    file: Optional[UploadFile] = File(None)
):
    try:
        # Parse history from frontend
        history = json.loads(conversation_history)

        # Optional file info
        file_info = ""
        if file and file.filename:
            file_info = f"\n\n[Attached file: {file.filename}]"

        full_question = question + file_info

        # Get answer — history is updated inside reply()
        answer = reply(full_question, history)

        # Return ONLY the reply
        return {"reply": answer}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uploader import save_uploaded_files

app = FastAPI(title="Folder Upload API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what to skip — can later be read from config or environment
EXCLUDED_EXTENSIONS = [".pdf", ".doc", ".docx"]

@app.post("/files/upload-folder")
async def upload_folder(files: List[UploadFile] = File(...)):
    """
    Accept multiple files (folder upload).
    Preserves folder structure and skips unwanted extensions.
    """
    try:
        result = await save_uploaded_files(
            files=files,
            upload_root="app/uploads",
            excluded_exts=EXCLUDED_EXTENSIONS
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

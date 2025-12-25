import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend from anywhere
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "Uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/search/")
async def search(image: UploadFile = File(...)):
    file_ext = os.path.splitext(image.filename)[-1]
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return JSONResponse({
        "query_filename": image.filename,
        "google_search_url": "https://www.google.com/imghp"
    })

app.mount("/Uploads", StaticFiles(directory=UPLOAD_DIR), name="Uploads")

import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.post("/search/")
async def search(image: UploadFile = File(...)):
    ext = os.path.splitext(image.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(image.file, f)

    return JSONResponse({
        "filename": image.filename,
        "google_lens_url": "https://lens.google.com/upload",
        "google_images_url": "https://www.google.com/imghp",
        "note": "Upload the same image to view results"
    })

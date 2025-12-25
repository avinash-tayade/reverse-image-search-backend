import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Reverse Image Search Backend is running 🚀"}


# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "Uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Render will inject this
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@app.post("/search/")
async def search(image: UploadFile = File(...)):
    try:
        ext = os.path.splitext(image.filename)[-1]
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"{BASE_URL}/Uploads/{filename}"

        google_link = f"https://lens.google.com/uploadbyurl?url={image_url}"

        return JSONResponse({
            "query_filename": image.filename,
            "query_image_url": image_url,
            "google_search_url": google_link,
            "status": "success"
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Serve uploaded images
app.mount("/Uploads", StaticFiles(directory=UPLOAD_DIR), name="Uploads")

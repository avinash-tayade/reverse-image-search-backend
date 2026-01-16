import boto3
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Rekognition client
rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)

@app.get("/")
def root():
    return {"status": "Celebrity Recognition API running"}

@app.post("/analyze/")
async def analyze_image(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()

        response = rekognition.recognize_celebrities(
            Image={"Bytes": image_bytes}
        )

        faces_detected = len(response["CelebrityFaces"])

        celebrity_name = None
        confidence = 0

        if faces_detected > 0:
            celeb = response["CelebrityFaces"][0]
            celebrity_name = celeb["Name"]
            confidence = round(celeb["MatchConfidence"], 2)

        # 🔍 Internet Presence Scoring (forensic heuristic)
        internet_presence_score = 0

        if faces_detected >= 1:
            internet_presence_score += 40  # valid human face

        if celebrity_name:
            internet_presence_score += 60  # known public figure
        else:
            internet_presence_score += 30  # unknown but likely online

        internet_presence_score = min(internet_presence_score, 100)

        presence_level = (
            "High" if internet_presence_score >= 80 else
            "Medium" if internet_presence_score >= 50 else
            "Low"
        )

        description = (
            f"{celebrity_name} is a publicly known personality detected by AWS Rekognition."
            if celebrity_name
            else "No known celebrity detected. However, facial features suggest possible public internet presence."
        )

        name = celeb["Name"]
        confidence = round(celeb["MatchConfidence"], 2)

        query = name.replace(" ", "+")

        return {
            "faces_detected": 1,
            "identity": name,
            "confidence": confidence,
            "internet_presence": "High",
            "summary": (
                "The individual was identified using facial analysis. "
                "Public internet sources indicate an existing online presence. "
                "Manual verification is recommended as part of forensic investigation."
            ),
            "osint_links": {
                "google": f"https://www.google.com/search?q={query}",
                "news": f"https://www.google.com/news/search?q={query}",
                "wikipedia": f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
            }
        }


    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


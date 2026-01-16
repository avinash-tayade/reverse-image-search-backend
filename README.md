# Reverse Image Search – Forensic Celebrity Recognition (Backend)

This backend service is a sub-module of a forensic sketch investigation system.

It analyzes uploaded images and identifies whether the face belongs to a known public figure using AWS Rekognition.

---

## 🚀 Features
- Face detection
- Celebrity identification
- Confidence score
- Forensic-style analysis output
- Secure AWS credential handling

---

## 🧠 Technology Stack
- Python 3.12.4
- FastAPI
- AWS Rekognition
- Boto3

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/avinash-tayade/reverse-image-search-backend.git
cd reverse-image-search-backend/backend-old/app

### 2️⃣ Install Dependencies
pip install -r requirements.txt

### 3️⃣ Set AWS Credentials (DO NOT COMMIT)

PowerShell (temporary, safe):

$env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
$env:AWS_DEFAULT_REGION="us-east-1"


These variables exist only for the current session and are never stored in code or GitHub.

### 4️⃣ Run Backend
uvicorn main:app --reload


Backend runs at:

http://127.0.0.1:8000

🧪 Sample Output
{
  "faces_detected": 1,
  "celebrity": "Elon Musk",
  "confidence": 99.87,
  "description": "Publicly known personality detected"
}

⚠️ Notes

AWS Rekognition may occasionally produce false positives.

This module assists investigation; it is not a legal identification system.
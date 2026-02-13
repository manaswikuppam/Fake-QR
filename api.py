from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn

# --- 1. SETUP & LOAD MODEL ---
app = FastAPI()

# Allow frontend to access the API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a root endpoint for browser testing
@app.get("/")
def home():
    return {"message": "✅ QR Shield AI Backend is Running! Use /scan endpoint."}

# Load the trained model
try:
    model = joblib.load('qr_fraud_model.pkl')
    print("✅ Brain loaded successfully!")
except:
    print("❌ Error: 'qr_fraud_model.pkl' not found.")
    model = None

# Define the data format we expect from the Mobile App
class URLRequest(BaseModel):
    url: str

# --- TRUSTED DOMAINS (Whitelist) ---
# The AI might get confused by simple HTTP links, so we verify known safe sites first.
WHITELIST = [
    "google.com", "www.google.com", 
    "youtube.com", "www.youtube.com",
    "facebook.com", "instagram.com",
    "wikipedia.org", "amazon.com"
]

# Feature Extraction (MUST match your training logic)
def get_url_features(url):
    features = [
        len(url), url.count('.'), url.count('-'), url.count('@'),
        url.count('?'), 1 if "https" in url else 0,
        sum(c.isdigit() for c in url),
        1 if ".xyz" in url or ".top" in url else 0
    ]
    return np.array(features).reshape(1, -1)

# --- 2. THE ENDPOINT (The Doorway) ---
@app.post("/scan")
def scan_qr(request: URLRequest):
    if model is None:
        return {"error": "Model not loaded"}

    # 1. Check Whitelist (Hybrid Security)
    domain_safe = any(domain in request.url.lower() for domain in WHITELIST)
    if domain_safe:
        return {
            "url": request.url,
            "status": "SAFE",
            "confidence": 100.0,
            "color": "green"
        }

    # 2. Extract features & predict
    features = get_url_features(request.url)
    prob_fake = model.predict_proba(features)[0][1]
    
    # Logic
    is_dangerous = prob_fake > 0.5
    confidence = prob_fake * 100 if is_dangerous else (1 - prob_fake) * 100
    
    print(f"📲 Received: {request.url} | Verdict: {'🚨 FAKE' if is_dangerous else '✅ SAFE'}")

    return {
        "url": request.url,
        "status": "MALICIOUS" if is_dangerous else "SAFE",
        "confidence": round(confidence, 1),
        "color": "red" if is_dangerous else "green"
    }

# --- 3. RUN SERVER AUTOMATICALLY ---
if __name__ == "__main__":
    # Host 0.0.0.0 makes it visible to your phone on the same WiFi
    print("\n✅ Server starting!")
    print("👉 Open this link in your browser: http://127.0.0.1:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
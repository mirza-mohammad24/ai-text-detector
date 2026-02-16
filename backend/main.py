# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rabin_karp import RabinKarpDetector 

# Initializing the app
app = FastAPI()

# CORS Setup (allowing frontend to contact this backend)
origins = [
    "http://localhost:5173",                      # For local testing
    "http://127.0.0.1:5173",                      # Alternative local address
    "https://ai-text-detector-one.vercel.app",    # Vercel Deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining the Schema
# We expect the body to be JSON with a 'text' string
class TextRequest(BaseModel):
    text: str

# Initializing our Logic Class
detector = RabinKarpDetector()

# Defining the Routes
@app.get("/")
def home():
    return {"message": "AI Detector API is running"}

# "request: TextRequest" validates the req.body
# If the user sends a number instead of string this fails automatically.
@app.post("/analyze")
def analyze_text(request: TextRequest):
    # Calling our logic function in rabin_karp
    result = detector.analyze(request.text)
    return result
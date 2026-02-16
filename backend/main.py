# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rabin_karp import RabinKarpDetector 

# Initializing the app
app = FastAPI()

# CORS Setup (allowing frontend to contact this backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Currently allowing any frontend to talk 
    allow_methods=["*"], #Allows GET, POST, PUT, DELETE
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
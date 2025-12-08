from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize OpenAI client lazily - only when needed
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
@app.get("/api")
@app.get("/api/")
def root():
    return {"status": "ok", "message": "API is running"}

@app.get("/health")
@app.get("/api/health")
def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}

@app.post("/chat")
@app.post("/api/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    try:
        client = get_openai_client()
        user_message = request.message
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive mental coach."},
                {"role": "user", "content": user_message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

# Catch-all route for debugging - helps identify if function is being called
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def catch_all(path: str):
    """Catch-all route to help debug routing issues."""
    return {
        "error": "Route not found",
        "path": path,
        "message": "This endpoint exists but the specific route was not matched. Check your route definitions."
    }

# Vercel serverless function handler
# Mangum adapts FastAPI (ASGI) to AWS Lambda/Vercel's serverless format
# When Vercel routes /api/(.*) to api/index.py, it passes the full path including /api
# We support both /chat and /api/chat routes to handle different path formats
handler = Mangum(app, lifespan="off")
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client instance. Raises HTTPException if API key is not configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured. Please set it in Vercel environment variables."
        )
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
    """
    Chat endpoint that handles user messages and returns AI responses.
    Supports both /chat and /api/chat paths for compatibility.
    """
    try:
        # Validate message
        user_message = request.message
        if not user_message or not user_message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )
        
        # Get OpenAI client (will raise HTTPException if API key is missing)
        client = get_openai_client()
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive mental coach."},
                {"role": "user", "content": user_message}
            ]
        )
        
        if not response.choices or len(response.choices) == 0:
            raise HTTPException(
                status_code=500,
                detail="No response from OpenAI API"
            )
        
        return {"reply": response.choices[0].message.content}
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        error_trace = traceback.format_exc()
        print(f"Error in chat endpoint: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error calling OpenAI API: {str(e)}"
        )

# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler to prevent function invocation failures.
    This ensures all errors are properly formatted and returned.
    """
    error_trace = traceback.format_exc()
    print(f"Unhandled exception: {str(exc)}")
    print(f"Traceback: {error_trace}")
    print(f"Request path: {request.url.path}")
    print(f"Request method: {request.method}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )

# Vercel serverless function handler
# Vercel's Python runtime natively supports ASGI applications (like FastAPI)
# No need for Mangum adapter - Vercel handles it automatically
# When Vercel routes /api/(.*) to api/index.py, it passes the full path including /api
# We support both /chat and /api/chat routes to handle different path formats
# Export the app - Vercel will automatically detect and use it as an ASGI application
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import traceback
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

app = FastAPI()

# Add middleware to handle path normalization and error handling
@app.middleware("http")
async def path_normalization_middleware(request: Request, call_next):
    """
    Normalize paths to handle Vercel's routing.
    Vercel may pass /api/chat or /chat depending on configuration.
    """
    try:
        # Get the original path
        path = request.url.path
        
        # If path starts with /api, strip it for internal routing
        # (since our routes are defined without /api prefix)
        if path.startswith("/api") and path != "/api":
            # Create a new request with normalized path
            # Note: We can't modify the request path directly, but FastAPI routes
            # handle both /chat and /api/chat, so this should work
            pass
        
        response = await call_next(request)
        return response
    except Exception as e:
        # Log the full error for debugging
        error_trace = traceback.format_exc()
        print(f"Error in middleware: {str(e)}")
        print(f"Traceback: {error_trace}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(e),
                "type": type(e).__name__
            }
        )

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
    """
    Chat endpoint that handles user messages and returns AI responses.
    Supports both /chat and /api/chat paths for compatibility.
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="OPENAI_API_KEY not configured. Please set it in Vercel environment variables."
            )
        
        client = get_openai_client()
        if not client:
            raise HTTPException(
                status_code=500,
                detail="Failed to initialize OpenAI client"
            )
        
        user_message = request.message
        if not user_message or not user_message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )
        
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
            "type": type(exc).__name__,
            "path": request.url.path
        }
    )

# Catch-all route for debugging - helps identify if function is being called
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def catch_all(path: str):
    """Catch-all route to help debug routing issues."""
    return {
        "error": "Route not found",
        "path": path,
        "message": "This endpoint exists but the specific route was not matched. Check your route definitions.",
        "available_routes": ["/", "/api", "/api/", "/health", "/api/health", "/chat", "/api/chat"]
    }

# Vercel serverless function handler
# Mangum adapts FastAPI (ASGI) to AWS Lambda/Vercel's serverless format
# When Vercel routes /api/(.*) to api/index.py, it passes the full path including /api
# We support both /chat and /api/chat routes to handle different path formats
handler = Mangum(app, lifespan="off")
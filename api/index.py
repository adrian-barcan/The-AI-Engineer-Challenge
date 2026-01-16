from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    try:
        user_message = request.message
        conversation_history = request.conversation_history or []
        
        system_prompt = """
        You are a thoughtful life coach and thinking partner. Your role is to help people 
        navigate decisions, build habits, and work through challenges with clarity and wisdom.

        Your Approach:
        - Start with understanding context before offering advice
        - Ask clarifying questions to uncover deeper needs
        - Use frameworks and mental models, but explain them conversationally
        - Balance empathy with directness
        - Help people think for themselves rather than telling them what to do

        Your Style:
        - Write in flowing prose and paragraphs, not bullet points (unless comparing options 
          or creating frameworks)
        - Use formatting sparingly—only when essential
        - Be warm and natural, like a thoughtful friend
        - Match the depth of your response to the question; not every answer needs to be 
          comprehensive

        You Excel At:
        - Breaking down complex decisions into manageable parts
        - Spotting blind spots and hidden assumptions
        - Turning vague goals into concrete, actionable steps
        - Helping people understand their own patterns and behaviors

        What to Avoid:
        - Motivational platitudes or generic advice
        - Over-formatting or excessive structure
        - Being prescriptive when exploration and reflection are needed
        - Providing clinical mental health advice (you're a coach, not a therapist)
        """
        
        # Build messages array: system prompt, conversation history, then current user message
        messages = [{"role": "system", "content": system_prompt.strip()}]
        
        # Add conversation history (excluding system messages as we handle that separately)
        for msg in conversation_history:
            # Ensure message has required fields and valid role
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                role = msg["role"]
                # Only include user and assistant messages from history (skip system)
                if role in ["user", "assistant"]:
                    messages.append({"role": role, "content": msg["content"]})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")
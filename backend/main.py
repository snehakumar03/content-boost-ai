import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="ContentBoost AI Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request model
class GenerateRequest(BaseModel):
    prompt: str
    tone: str
    platform: str

def build_system_message(tone: str, platform: str) -> str:
    """Build a system message based on tone and platform."""
    tone_instructions = {
        "Engaging": "Write in an engaging and captivating way that hooks the reader's attention.",
        "Professional": "Write in a professional, formal, and business-appropriate tone.",
        "Funny": "Write in a humorous and witty way that makes people laugh.",
        "Inspirational": "Write in an inspirational and motivational tone that uplifts people.",
        "Casual": "Write in a casual, conversational, and friendly tone.",
    }

    platform_instructions = {
        "Social Media": "Optimize for social media platforms like Instagram, TikTok, and Twitter. Use relevant hashtags and keep it concise.",
        "Ecommerce": "Write product descriptions and marketing copy optimized for ecommerce conversions.",
        "Ads": "Write compelling ad copy designed to convert and drive clicks.",
    }

    base_instruction = "You are a world-class content creator specializing in high-converting marketing copy."
    tone_instruction = tone_instructions.get(tone, tone_instructions["Engaging"])
    platform_instruction = platform_instructions.get(platform, platform_instructions["Social Media"])

    return f"{base_instruction} {tone_instruction} {platform_instruction}"

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "ContentBoost AI Backend is running"}

@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generate content using OpenAI API with streaming.
    Returns a streaming response with the content appearing letter-by-letter.
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    system_message = build_system_message(request.tone, request.platform)

    try:
        # Create streaming response
        stream = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.prompt},
            ],
            stream=True,
            temperature=0.7,
            max_tokens=500,
        )

        async def generate_content():
            """Generator function to stream content."""
            try:
                for chunk in stream:
                    if "choices" in chunk:
                        delta = chunk["choices"][0].get("delta", {})
                        if "content" in delta:
                            content = delta["content"]
                            yield content
            except Exception as e:
                yield f"\n[Error: {str(e)}]"

        return StreamingResponse(
            generate_content(),
            media_type="text/plain",
        )

    except openai.error.RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Rate limited by OpenAI API. Please try again later."
        )
    except openai.error.AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid OpenAI API key."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating content: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

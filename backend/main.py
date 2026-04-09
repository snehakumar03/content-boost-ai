import os
import asyncio
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI, RateLimitError, AuthenticationError
import json

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    logger.info(f"Received generate request: prompt='{request.prompt}', tone='{request.tone}', platform='{request.platform}'")
    
    if not request.prompt:
        logger.warning("Empty prompt provided")
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "" or api_key == "your_api_key_here":
        logger.info("No OpenAI API key found, using demo mode")
        # Demo mode - return sample content if no API key
        async def demo_generator():
            sample_response = f"✨ Demo Mode (No OpenAI Key)\n\nYour prompt: '{request.prompt}'\nPlatform: {request.platform}\nTone: {request.tone}\n\n📝 In production, this would be AI-generated content from OpenAI.\n\n💡 To enable AI generation:\n1. Get API key: https://platform.openai.com/account/api-keys\n2. Edit backend/.env with your key\n3. Restart the backend\n\nThis demo mode allows you to test the UI without an API key!"
            for char in sample_response:
                yield char
                await asyncio.sleep(0.01)  # Simulate streaming
        
        return StreamingResponse(demo_generator(), media_type="text/plain")

    try:
        logger.info("Calling OpenAI API")
        # Create streaming response
        stream = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": build_system_message(request.tone, request.platform)},
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
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if delta.content:
                            content = delta.content
                            yield content
            except Exception as e:
                logger.error(f"Error in streaming generator: {str(e)}")
                yield f"\n[Error: {str(e)}]"

        return StreamingResponse(
            generate_content(),
            media_type="text/plain",
        )

    except RateLimitError as e:
        logger.error(f"OpenAI RateLimitError: {str(e)}")
        raise HTTPException(
            status_code=429,
            detail="Rate limited by OpenAI API. Please try again later."
        )
    except AuthenticationError as e:
        logger.error(f"OpenAI AuthenticationError: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid OpenAI API key."
        )
    except Exception as e:
        logger.error(f"Unexpected error in generate: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating content: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

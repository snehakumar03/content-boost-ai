# Backend - ContentBoost AI

FastAPI server for ContentBoost AI with OpenAI integration and streaming responses.

## 🚀 Features

- **FastAPI**: High-performance Python web framework
- **Streaming**: Real-time text generation
- **OpenAI Integration**: Uses GPT-3.5-turbo for content generation
- **CORS Enabled**: Works with frontend on localhost:5173
- **Error Handling**: Comprehensive error responses

## 🛠️ Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

Get your key at: https://platform.openai.com/account/api-keys

### 4. Start Server
```bash
python main.py
```

or with auto-reload:
```bash
uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**

Health check: **http://localhost:8000/health**

## 📚 API Endpoints

### Check Server Status
```
GET /health
Response: { "status": "ok", "message": "..." }
```

### Generate Content (Streaming)
```
POST /generate

Headers:
  Content-Type: application/json

Body:
{
  "prompt": "Write a caption for our new product",
  "tone": "Engaging",
  "platform": "Social Media"
}

Response: Plain text stream (character by character)
```

### Example cURL Request
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a funny caption for pizza",
    "tone": "Funny",
    "platform": "Social Media"
  }'
```

## 🔧 Customization

### Change AI Model

Edit `main.py`, line ~100:
```python
stream = openai.ChatCompletion.create(
    model="gpt-4",  # Change from gpt-3.5-turbo to gpt-4
    ...
)
```

### Adjust Creativity (Temperature)

```python
# Lower = more deterministic, Higher = more creative
temperature=0.7,  # Range: 0.0 to 2.0
```

### Change Max Output

```python
# Maximum tokens per response
max_tokens=500,  # Increase for longer outputs
```

### Add More Tones

Edit `build_system_message()` function:
```python
tone_instructions = {
    "Engaging": "...",
    "Professional": "...",
    # Add more tones here
    "Sarcastic": "Write in a sarcastic and witty tone...",
}
```

### Modify System Prompts

Update platform and tone instructions in `build_system_message()`:
```python
platform_instructions = {
    "Social Media": "...",
    # Add more platforms
    "Blog": "Write blog post content...",
}
```

## 📦 Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **openai**: OpenAI API client
- **python-dotenv**: Environment variable management
- **aiofiles**: Async file operations

## 🌐 CORS Configuration

By default, CORS is enabled for:
- http://localhost:5173 (frontend)
- http://localhost:3000 (alternative)
- Wildcard "*" for development

For production, update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Your domain
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `OpenAI API key not found` | Add `OPENAI_API_KEY` to `.env` |
| `Connection refused` | Ensure server is running on port 8000 |
| Rate limit errors | OpenAI API rate limit reached - wait or upgrade plan |
| 500 errors | Check server logs for detailed error messages |

## 📊 Monitoring

View server logs to debug:
```bash
# With auto-reload
uvicorn main:app --reload --log-level debug
```

## 🚀 Production Deployment

Deploy with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

Or with Docker:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

**Built with FastAPI + OpenAI API**

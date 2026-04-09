# Frontend-Backend Connection Guide

## 🔗 How the Two Sides Connect

The ContentBoost AI application uses a **client-server architecture** where:
- **Frontend** (React on localhost:5173) sends requests to the backend
- **Backend** (FastAPI on localhost:8000) processes requests and returns streamed responses

## 📡 Request Flow

```
User Interface (React)
    ↓ User enters prompt and clicks "Generate"
    ↓ Frontend fetches from backend
    ↓
Backend (FastAPI)
    ↓ Receives POST request with prompt, tone, platform
    ↓ Builds system message based on tone and platform
    ↓
OpenAI API
    ↓ Generates text response (streaming)
    ↓
Backend
    ↓ Streams response back to frontend
    ↓
Frontend
    ↓ Displays text character-by-character
    ↓
User sees result!
```

## 🔌 Connection Point: The API Call

### Frontend Code (App.jsx)

```javascript
const handleGenerate = async () => {
  setIsLoading(true);
  setGeneratedContent('');

  try {
    // Step 1: Send POST request to backend
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt,           // User's prompt
        tone,            // Selected tone
        platform,        // Selected platform
      }),
    });

    // Step 2: Read streaming response
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      // Step 3: Append each chunk to state (character-by-character)
      const chunk = decoder.decode(value);
      setGeneratedContent((prev) => prev + chunk);
    }
  } catch (error) {
    console.error('Generate error:', error);
    setGeneratedContent('Error generating content...');
  } finally {
    setIsLoading(false);
  }
};
```

### Backend Code (main.py)

```python
@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Receives: {prompt, tone, platform}
    Returns: Streaming text response
    """
    # Step 1: Build system message based on tone and platform
    system_message = build_system_message(request.tone, request.platform)

    # Step 2: Call OpenAI API with streaming
    stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": request.prompt},
        ],
        stream=True,  # IMPORTANT: Enable streaming
    )

    # Step 3: Stream response back to frontend
    async def generate_content():
        for chunk in stream:
            if "choices" in chunk:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    yield delta["content"]  # Send each character

    return StreamingResponse(generate_content(), media_type="text/plain")
```

## 🚀 Starting Both Servers

### Terminal 1: Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Edit .env with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

python main.py
```

✅ Backend will run at: `http://localhost:8000`

### Terminal 2: Frontend
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend will run at: `http://localhost:5173`

## ⚙️ CORS Configuration

**CORS** (Cross-Origin Resource Sharing) allows the frontend to communicate with the backend across different ports.

### Currently Enabled Origins (backend/main.py):
```python
allow_origins=[
    "http://localhost:5173",  # Frontend dev server
    "http://localhost:3000",  # Alternative frontend
    "*",                      # All origins (development only!)
]
```

### For Production:
Update `allow_origins` to your actual domain:
```python
allow_origins=["https://contentboost.yourdomain.com"]
```

## 🧪 Testing the Connection

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
# Expected response: {"status":"ok","message":"..."}
```

### 2. Check Frontend Loads
Open http://localhost:5173 in browser - should see the UI

### 3. Test API Endpoint
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a caption for pizza",
    "tone": "Funny",
    "platform": "Social Media"
  }'
```

Expected: Text response streams character by character

### 4. Full Integration Test
1. Open frontend at http://localhost:5173
2. Enter a prompt
3. Click "Generate Content"
4. Watch the AI response appear letter-by-letter

## 🔄 Data Flow Diagram

```
┌─────────────────┐
│  React Browser  │
│  - User Input   │
│  - Display Text │
└────────┬────────┘
         │
         │ POST /generate
         │ {prompt, tone, platform}
         ↓
┌─────────────────┐
│  FastAPI Server │
│  - Build prompt │
│  - Call OpenAI  │
│  - Stream back  │
└────────┬────────┘
         │
         │ Streaming Response
         │ "Hello... world..."
         ↓
┌─────────────────┐
│  Frontend Reads │
│  - getReader()  │
│  - Append text  │
│  - Update state │
└─────────────────┘
```

## 🔐 Environment Variables

### Backend `.env`
```ini
OPENAI_API_KEY=sk-...        # Your OpenAI API key
BACKEND_HOST=0.0.0.0         # Backend address
BACKEND_PORT=8000            # Backend port
FRONTEND_URL=http://localhost:5173  # Frontend URL (for CORS)
```

### Frontend `src/App.jsx`
```javascript
// Hardcoded for now:
const API_URL = 'http://localhost:8000/generate';

// For production, use environment variable:
// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/generate';
```

## 🚨 Common Connection Issues

### ❌ "Failed to fetch" Error
**Cause**: Backend not running or wrong URL
**Solution**: 
- Ensure backend is running: `python main.py`
- Check backend is on port 8000
- Verify URL in `App.jsx` is correct

### ❌ "CORS policy" Error
**Cause**: Backend CORS not allowing frontend origin
**Solution**:
- Confirm frontend is on `http://localhost:5173`
- Verify backend has `allow_origins` set correctly
- Restart backend after changing CORS

### ❌ "Invalid API key" Error
**Cause**: OpenAI API key not set or invalid
**Solution**:
- Add key to `.env`: `OPENAI_API_KEY=sk-...`
- Verify key is from https://platform.openai.com/account/api-keys
- Restart backend after updating `.env`

### ❌ No Content Appearing
**Cause**: Stream not connecting properly
**Solution**:
- Check browser console (F12) for errors
- Verify backend returns 200 status
- Test endpoint with `curl` command above

## 📊 API Request/Response Example

### Request (Frontend → Backend)
```json
{
  "prompt": "Write a caption for our new sneaker sale!",
  "tone": "Engaging",
  "platform": "Social Media"
}
```

### System Message Built by Backend
```
You are a world-class content creator specializing in high-converting marketing copy. 
Write in an engaging and captivating way that hooks the reader's attention. 
Optimize for social media platforms like Instagram, TikTok, and Twitter. 
Use relevant hashtags and keep it concise.
```

### Response (Backend → Frontend, Streamed)
```
"Step up your shoe game without breaking the bank!

Our sneaker sale is on – grab your favorite kicks at unbeatable prices! 👟

Don't miss out on premium styles at unbeatable prices! #SneakerDeals #SaleTime"
```

## 🔧 To Modify the Connection

### Change Backend URL
Edit `frontend/src/App.jsx`, line ~59:
```javascript
const response = await fetch('YOUR_NEW_URL/generate', {
```

### Change Streaming Behavior
Edit `backend/main.py`, in `generate()` function:
```python
async def generate_content():
    for chunk in stream:
        # Add custom logic here
        yield chunk
```

### Add Request Validation
Edit `backend/main.py`, in `GenerateRequest` class:
```python
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    tone: str
    platform: str
```

## 📝 Checklist for Production

- [ ] Update CORS `allow_origins` to production domain
- [ ] Set `OPENAI_API_KEY` as environment variable (not in code)
- [ ] Update backend URL in frontend `.env` or code
- [ ] Use `gpt-4` instead of `gpt-3.5-turbo` (or keep current)
- [ ] Add rate limiting to prevent abuse
- [ ] Add authentication if needed
- [ ] Test streaming on production setup
- [ ] Monitor OpenAI API costs and usage

---

**The frontend and backend communicate via HTTP POST requests with streaming responses. Make sure both are running on their respective ports!**

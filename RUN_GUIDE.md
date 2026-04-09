# 🚀 Complete Step-by-Step Run Guide

This guide walks you through running the ContentBoost AI application from scratch, step by step.

---

## 📋 Prerequisites

Before you start, ensure you have:
- ✅ Node.js 16+ (Check: `node --version`)
- ✅ npm 7+ (Check: `npm --version`)
- ✅ Python 3.8+ (Check: `python --version` or `python3 --version`)
- ✅ OpenAI API Key (Get from: https://platform.openai.com/account/api-keys)
- ✅ Git (Check: `git --version`)

---

## 🎯 Quick Overview

This project has two parts that run independently:
- **Backend** (Python FastAPI) - Generates content using OpenAI API
- **Frontend** (React) - User interface to interact with the backend

We'll run them in **two separate terminals**.

---

## 📚 Terminal 1: Setting Up & Running the Backend

### Step 1: Navigate to Backend Directory

```bash
cd /home/sneha/personal-work/ai-content-gen/backend
```

**Expected Output:**
```
$ pwd
/home/sneha/personal-work/ai-content-gen/backend
```

### Step 2: Create Python Virtual Environment

```bash
python -m venv venv
```

or if you have both Python 2 and 3:

```bash
python3 -m venv venv
```

**What this does:** Creates isolated Python environment in `venv/` folder

**Expected:** Folder `venv/` appears in backend directory

### Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

**Expected Output:** Your prompt should change to show `(venv)`:
```
(venv) $ 
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What this installs:**
- `fastapi` - Web framework
- `uvicorn` - Server
- `openai` - OpenAI API client
- `python-dotenv` - Environment variables

**Expected Output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 openai-1.3.8 python-dotenv-1.0.0 ...
```

### Step 5: Configure API Key

Open the `.env` file in the backend directory:

```bash
# View the file
cat .env
```

You should see:
```
OPENAI_API_KEY=your_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173
```

**Edit the file** - Open `.env` with your editor and replace:
```
OPENAI_API_KEY=your_api_key_here
```

with your actual OpenAI API key:
```
OPENAI_API_KEY=sk-proj-abc123def456...
```

⚠️ **Important:** 
- Your key must start with `sk-`
- Don't share this key with anyone
- Don't commit it to GitHub

### Step 6: Test Backend Setup

```bash
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 7: Verify Backend is Running

**In a new terminal** (keep the backend running), test if it's working:

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"ok","message":"ContentBoost AI Backend is running"}
```

If you get a response, backend is ✅ **ready!**

### Step 8: Keep Backend Running

Leave this terminal open with the backend running. You'll use it to generate content.

The backend will stay running and ready to receive requests from the frontend.

---

## 🎨 Terminal 2: Setting Up & Running the Frontend

### Step 1: Open New Terminal Window

Open a **brand new terminal** (keep the first one with backend still running).

### Step 2: Navigate to Frontend Directory

```bash
cd /home/sneha/personal-work/ai-content-gen/frontend
```

**Expected Output:**
```
$ pwd
/home/sneha/personal-work/ai-content-gen/frontend
```

### Step 3: Install Frontend Dependencies

```bash
npm install
```

**What this does:** Downloads React, Tailwind CSS, Framer Motion, and other packages

**Expected Output:**
```
added 135 packages in 24s
```

(Takes 20-30 seconds first time)

### Step 4: Start Development Server

```bash
npm run dev
```

**Expected Output:**
```
  VITE v4.4.5  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Step 5: Open in Browser

Copy the URL from the output (usually `http://localhost:5173/`) and open it in your browser.

**Expected:** You should see the ContentBoost AI interface with:
- Purple/dark background
- Navigation bar at top
- Hero section with "Generate High-Converting Content"
- Form on left, response area on right
- Feature grid at bottom

---

## ✅ Verify Everything Works

### Test 1: Check Backend Connection

In the frontend, you should see no console errors (press F12 to open developer tools).

### Test 2: Generate Content

1. Fill in the form:
   - **Platform:** Select "Social Media"
   - **Content Type:** Select "Caption"
   - **Tone:** Select "Engaging"
   - **Prompt:** "Write a caption for my new coffee shop"

2. Click **"Generate Content"** button

3. Watch the text appear letter-by-letter!

### Test 3: Copy & Regenerate

- Click **"Copy"** button - should copy text to clipboard
- Click **"Regenerate"** button - should generate new content

---

## 🔄 Typical Workflow During Development

### Terminal 1 (Backend - Keep Running)
```bash
$ cd backend
$ source venv/bin/activate
$ python main.py
# Output: Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 (Frontend - Keep Running)
```bash
$ cd frontend
$ npm run dev
# Output: Local: http://localhost:5173/
```

### Browser
```
Open: http://localhost:5173/
Test the application
```

---

## 🛑 Stopping the Application

### Stop Frontend
In Terminal 2, press `Ctrl+C`:
```
KeyboardInterrupt
```

### Stop Backend
In Terminal 1, press `Ctrl+C`:
```
KeyboardInterrupt
```

---

## 🚨 Troubleshooting

### Issue: "Connection refused" or "Cannot reach backend"

**Solution:**
1. Make sure backend is running: `python main.py` (Terminal 1)
2. Check backend is on port 8000: You should see `Uvicorn running on http://0.0.0.0:8000`
3. Test health endpoint: `curl http://localhost:8000/health`

### Issue: "Invalid API key"

**Solution:**
1. Check `.env` file has correct OpenAI key
2. Key must start with `sk-`
3. Restart backend after changing `.env`

### Issue: Frontend shows blank page

**Solution:**
1. Check browser console (F12) for errors
2. Make sure backend is running
3. Try hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Issue: "npm: command not found"

**Solution:**
1. Check Node.js is installed: `node --version`
2. If not installed, download from: https://nodejs.org/
3. After installing, restart terminal

### Issue: "python: command not found"

**Solution:**
1. Use `python3` instead: `python3 --version`
2. If not found, install Python from: https://www.python.org/downloads/
3. Make sure to add Python to PATH during installation

### Issue: Virtual environment not activating

**Solution:**
- On Windows: Use `venv\Scripts\activate` instead of `source venv/bin/activate`
- Make sure you're in the `backend/` directory
- Try creating a new venv: `python -m venv venv`

---

## 📊 Understanding the Architecture

```
┌─────────────────────────────────────────────────────┐
│              Your Web Browser                       │
│         http://localhost:5173                       │
│                                                     │
│    [Your Prompt] → [Click Generate] → [Result]     │
└────────────────────────┬────────────────────────────┘
                         │
                    HTTP POST Request
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend                        │
│         http://localhost:8000                       │
│                                                     │
│    [Receive Prompt] → [Call OpenAI] → [Stream Back]│
└────────────────────────┬────────────────────────────┘
                         │
                    HTTP Streaming
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│              OpenAI API                             │
│         (Your API Key)                              │
│                                                     │
│    [Generate Text] → [Stream to Backend]          │
└─────────────────────────────────────────────────────┘
```

---

## 📱 Ports Used

| Service | Port | URL | Started By |
|---------|------|-----|-----------|
| **Frontend** | 5173 | http://localhost:5173 | `npm run dev` |
| **Backend** | 8000 | http://localhost:8000 | `python main.py` |

If these ports are already in use on your machine, you may need to change them in:
- Frontend: `frontend/vite.config.js` → `port: 5173`
- Backend: `backend/main.py` or `backend/.env` → `BACKEND_PORT=8000`

---

## 🎬 Making Changes

### If you change Frontend code:
1. Edit files in `frontend/src/`
2. Browser automatically refreshes (Hot Reload)
3. No need to restart

### If you change Backend code:
1. Edit `backend/main.py`
2. Backend auto-restarts (if using `--reload`)
3. If not, restart: `Ctrl+C` then `python main.py` again

---

## 📦 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

Creates optimized files in `frontend/dist/` (ready to deploy)

### Backend Deployment
See `backend/README.md` for production deployment instructions.

---

## ✨ Summary

| Step | Terminal | Command | Output |
|------|----------|---------|--------|
| 1 | Backend | `cd backend` | `backend/` |
| 2 | Backend | `python -m venv venv` | `venv/` folder created |
| 3 | Backend | `source venv/bin/activate` | `(venv) $` prompt |
| 4 | Backend | `pip install -r requirements.txt` | Packages installed |
| 5 | Backend | Edit `.env` with API key | Save file |
| 6 | Backend | `python main.py` | Server running on :8000 |
| 7 | Frontend (New) | `cd frontend` | `frontend/` |
| 8 | Frontend | `npm install` | 135 packages |
| 9 | Frontend | `npm run dev` | Server running on :5173 |
| 10 | Browser | Open http://localhost:5173 | See UI |
| 11 | Browser | Fill form & click Generate | **Enjoy!** 🎉 |

---

## 🎓 Next Steps

After running successfully:

1. **Explore the Code**: Check `frontend/src/App.jsx` and `backend/main.py`
2. **Customize UI**: Edit colors and animations in `frontend/src/index.css`
3. **Change Prompts**: Modify system messages in `backend/main.py` (line ~61)
4. **Deploy**: Follow deployment guides in `backend/README.md` and `frontend/README.md`
5. **Contribute**: See `CONTRIBUTING.md` for how to submit improvements

---

## 📞 Need Help?

Check these files:
- **Connection Issues**: [CONNECTION_GUIDE.md](CONNECTION_GUIDE.md)
- **Backend Help**: [backend/README.md](backend/README.md)
- **Frontend Help**: [frontend/README.md](frontend/README.md)
- **General Questions**: [README.md](README.md)

---

**Happy Content Generating! 🚀**

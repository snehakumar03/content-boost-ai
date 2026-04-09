# ContentBoost AI - Full Stack Application

A modern AI-powered content generation platform built with React, FastAPI, and OpenAI. Generate high-converting marketing copy for social media, ecommerce, and ads in real-time with streaming responses.

![ContentBoost AI](./frontend/src/assets/preview.png)

## 🎯 Features

- **Glassmorphism UI**: Beautiful dark theme with glowing orbs and smooth animations
- **Real-time Streaming**: AI-generated content appears letter-by-letter as it's generated
- **Multi-Platform Support**: Optimize content for Social Media, Ecommerce, or Ads
- **Customizable Tone**: Choose from Engaging, Professional, Funny, Inspirational, or Casual
- **One-Click Copy**: Easily copy generated content to clipboard
- **Regenerate**: Create new variations with a single click
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh && ./setup.sh
chmod +x start.sh && ./start.sh
```

**Windows:**
```cmd
setup.bat
start.bat
```

### Manual Setup

See [RUN_GUIDE.md](RUN_GUIDE.md) for detailed step-by-step instructions.

**Quick Manual:**
```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Edit .env and add your OpenAI API key
python main.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Then open: [http://localhost:5173](http://localhost:5173)

## 📋 Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- OpenAI API Key ([Get it here](https://platform.openai.com/account/api-keys))

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [RUN_GUIDE.md](RUN_GUIDE.md) | **Complete step-by-step instructions** |
| [QUICKSTART.md](QUICKSTART.md) | Ultra-fast 5-minute setup |
| [CONNECTION_GUIDE.md](CONNECTION_GUIDE.md) | How frontend & backend communicate |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [backend/README.md](backend/README.md) | Backend documentation |
| [frontend/README.md](frontend/README.md) | Frontend documentation |

## 📁 Project Structure

```
ai-content-gen/
├── frontend/                 # React + Tailwind + Framer Motion
│   ├── src/
│   │   ├── App.jsx          # Main component (entire UI)
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Tailwind + custom styles
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                  # FastAPI + OpenAI
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Configuration (create from .env.example)
│
├── RUN_GUIDE.md            # Detailed step-by-step instructions
├── QUICKSTART.md           # 5-minute quick start
├── setup.sh / setup.bat    # Automated setup scripts
├── start.sh / start.bat    # Scripts to start both services
└── README.md               # This file
```

## 🔌 API Endpoints

### Health Check
```
GET /health
Response: {"status": "ok", "message": "..."}
```

### Generate Content (Streaming)
```
POST /generate
Body: {"prompt": "...", "tone": "...", "platform": "..."}
Response: Text stream (character-by-character)
```

## 🛠️ Technology Stack

### Frontend
- React 18
- Tailwind CSS 3
- Framer Motion 10
- Vite
- Lucide React

### Backend
- FastAPI
- Uvicorn
- OpenAI API
- Python 3.8+

## 🎨 Customization

### Change Colors
Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  'purple-dark': '#1a0033',  // Your color
}
```

### Change AI Behavior
Edit `backend/main.py` (~line 106):
```python
temperature=0.7,      # Higher = more creative
max_tokens=500,       # Longer responses
```

### Add More Tones
Edit `backend/main.py` (`build_system_message()` function)

## 🚨 Troubleshooting

### "Cannot reach backend"
- Ensure backend is running: `python main.py`
- Check it's on port 8000: `curl http://localhost:8000/health`

### "Invalid API key"
- Add key to `backend/.env`
- Key must start with `sk-`
- Restart backend

### "npm: command not found"
- Install Node.js from https://nodejs.org/

### "python: command not found"
- Use `python3` instead
- Or install Python from https://www.python.org/

See [RUN_GUIDE.md](RUN_GUIDE.md) for more troubleshooting.

## 📦 Build for Production

### Frontend
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend
See `backend/README.md` for production deployment.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔗 Links

- Repository: https://github.com/snehakumar03/content-boost-ai
- GitHub Issues: https://github.com/snehakumar03/content-boost-ai/issues
- OpenAI API: https://platform.openai.com/

---

**Built with ❤️ using React, FastAPI, and OpenAI**

**[👉 Get Started with RUN_GUIDE.md](RUN_GUIDE.md)**
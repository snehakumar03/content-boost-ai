# QUICK START GUIDE

## 🚀 Get Running in 5 Minutes

### Terminal 1: Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI API key
python main.py
```

The backend runs at: **http://localhost:8000**

### Terminal 2: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend runs at: **http://localhost:5173**

### ✅ Done!
Open http://localhost:5173 in your browser and start generating content!

---

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key and paste it in `backend/.env`
4. Make sure it starts with `sk-`

---

## 🎯 Testing the Connection

1. **Backend Health Check**: Visit http://localhost:8000/health
2. **Frontend Loads**: Visit http://localhost:5173
3. **Try Generation**: Fill form and click "Generate Content"

---

## ❌ Stuck? Common Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" | Backend not running on port 8000 |
| "Invalid API key" | Check `.env` file has correct OpenAI key |
| CORS errors | Backend is running, refresh front-end |
| Nothing happening when generating | Check browser console (F12) for errors |

---

## 📱 Features to Try

- ✅ Change platform (Social Media → Ecommerce → Ads)
- ✅ Change tone (Engaging → Professional → Funny)
- ✅ Copy generated content
- ✅ Regenerate with "Regenerate" button
- ✅ Watch content stream letter-by-letter

**Happy content generating! 🎉**

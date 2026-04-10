# Authentication System Setup Guide

## Prerequisites

1. **MySQL Server** installed and running
2. **Python 3.8+** with pip
3. **Node.js 16+** with npm

## Database Setup

### Option 1: Using MySQL Command Line

```bash
# Login to MySQL
mysql -u root -p

# Run the schema script
source backend/schema.sql

# Exit MySQL
exit
```

### Option 2: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open `backend/schema.sql`
4. Execute the script

### Environment Variables

Update `backend/.env` with your MySQL credentials:

```bash
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/contentboost
```

## Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the frontend
npm run dev
```

## Testing the Application

### 1. Register a New User

1. Go to http://localhost:5173/register
2. Fill in name, email, and password
3. Click "Sign Up"
4. You'll be redirected to login

### 2. Login

1. Go to http://localhost:5173/login
2. Enter your email and password
3. Click "Sign In"
4. You'll be redirected to the dashboard

### 3. Test Rate Limiting (Without Login)

1. Go to http://localhost:5173/dashboard
2. Generate content 6 times
3. The 6th attempt should show a rate limit error

### 4. Test OAuth (Optional)

To enable OAuth, you need to set up:

**Google OAuth:**
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add `http://localhost:8000/api/auth/oauth/callback/google` to authorized redirect URIs
6. Copy Client ID and Secret to `.env`

**GitHub OAuth:**
1. Go to https://github.com/settings/developers
2. Create a new OAuth App
3. Set Authorization callback URL: `http://localhost:8000/api/auth/oauth/callback/github`
4. Copy Client ID and Secret to `.env`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Logout current user
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/rate-limit` - Get rate limit status

### OAuth

- `GET /api/auth/oauth/google` - Initiate Google OAuth
- `GET /api/auth/oauth/github` - Initiate GitHub OAuth
- `GET /api/auth/oauth/callback/{provider}` - OAuth callback

### Content Generation

- `POST /generate` - Generate content (rate limited)

## Default Admin User

Email: `admin@contentboost.ai`
Password: `admin123`

**Important:** Change this password in production!

## Troubleshooting

### Database Connection Error

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```

**Solution:** Make sure MySQL is running and credentials in `.env` are correct.

### CORS Error

**Solution:** Make sure backend CORS settings include your frontend URL.

### Import Errors

**Solution:** Run `pip install -r requirements.txt` in the backend directory.

### OAuth Not Working

**Solution:** Make sure you've set up OAuth apps and added credentials to `.env`.

## Production Deployment

For production, make sure to:

1. Change `JWT_SECRET` to a strong random value
2. Use HTTPS for all communications
3. Set proper CORS origins (not `*`)
4. Use environment variables for sensitive data
5. Set up proper database backups
6. Implement email verification
7. Add proper logging and monitoring

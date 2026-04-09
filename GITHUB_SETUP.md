# GitHub Setup Guide for ContentBoost AI

This guide will help you connect your local repository to GitHub.

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `ai-content-gen` (or your preferred name)
3. Description: `AI-powered content generation platform for social media & ecommerce`
4. Choose **Public** or **Private**
5. **Do NOT** initialize with README, .gitignore, or license (we have them)
6. Click **Create Repository**

### Step 2: Connect Local Repository to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
# Navigate to your project
cd /home/sneha/personal-work/ai-content-gen

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/ai-content-gen.git

# Rename branch to main (if on master)
git branch -M main

# Stage all files
git add .

# Create first commit
git commit -m "Initial commit: Full-stack ContentBoost AI application"

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Verify on GitHub

Visit: `https://github.com/YOUR_USERNAME/ai-content-gen`

You should see your code!

---

## 📝 Current Git Status

```bash
# Check current status
git status

# See commit history
git log --oneline

# See remote connections
git remote -v
```

---

## 🔄 Regular Workflow

After setup, here's your typical workflow:

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes...

# Stage changes
git add .

# Commit
git commit -m "feat: add your feature"

# Push to GitHub
git push origin feature/your-feature

# Create Pull Request on GitHub
# (GitHub will show a prompt to create PR)
```

---

## 🛠️ Useful Git Commands

### View Status
```bash
git status                    # See what files changed
git log --oneline            # See commit history
git branch -a                # See all branches
```

### Create & Switch Branches
```bash
git checkout -b feature/name  # Create and switch to new branch
git checkout main            # Switch to main branch
git branch -d feature/name   # Delete branch locally
```

### Commit & Push
```bash
git add .                    # Stage all files
git add filename             # Stage specific file
git commit -m "message"      # Create commit
git push                     # Push to GitHub
git push origin --delete feature/name  # Delete remote branch
```

### Pull Updates
```bash
git pull                     # Fetch and merge latest
git fetch                    # Just fetch without merging
```

---

## 🔐 Authentication

### Using HTTPS (Easier for beginners)
When prompted for password, use:
- **Username**: Your GitHub username
- **Password**: Personal Access Token (from https://github.com/settings/tokens)

### Using SSH (Recommended for frequent use)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
# Go to https://github.com/settings/keys
# Paste contents of ~/.ssh/id_ed25519.pub

# Test connection
ssh -T git@github.com
```

---

## 📦 What's Included in the Repository

```
.gitignore              ✓ Ignores node_modules, venv, .env
.github/
  ├── workflows/
  │   └── ci.yml       ✓ GitHub Actions CI/CD
  ├── ISSUE_TEMPLATE/  ✓ Bug & Feature templates
  └── pull_request_template.md  ✓ PR template

LICENSE                 ✓ MIT License
CONTRIBUTING.md         ✓ Contribution guidelines
README.md               ✓ Main documentation
QUICKSTART.md           ✓ Quick setup guide
CONNECTION_GUIDE.md     ✓ Frontend-backend integration
PROJECT_OVERVIEW.md     ✓ Deliverables list

frontend/               ✓ React + Tailwind + Framer Motion
backend/                ✓ FastAPI + OpenAI
```

---

## ✅ Pre-Push Checklist

Before pushing to GitHub:

- [ ] All changes committed with clear messages
- [ ] No sensitive data (API keys, passwords) committed
- [ ] Updated relevant documentation
- [ ] Tested your changes locally
- [ ] No merge conflicts
- [ ] Branch is up to date with main

---

## 🔗 GitHub Actions CI/CD

The repository includes automated testing:

```
On every push/PR:
  ├── Backend Tests (Python 3.8-3.11)
  │   └── Syntax check
  └── Frontend Build (Node 18)
      └── Build verification
```

Check status at: `https://github.com/YOUR_USERNAME/ai-content-gen/actions`

---

## 🚨 Common Issues

### "Fatal: not a git repository"
```bash
# Reinitialize git
git init
git remote add origin https://github.com/YOUR_USERNAME/ai-content-gen.git
```

### "Permission denied (publickey)"
- SSH key not set up or added to ssh-agent
- Use HTTPS instead: `https://github.com/username/repo.git`

### "Updates were rejected"
```bash
# Pull latest before pushing
git pull origin main
# Resolve conflicts if any
git push origin main
```

### ".env file committed accidentally"
```bash
# Remove from history
git rm --cached backend/.env
git commit -m "Remove .env from tracking"
git push
```

---

## 📚 Useful Resources

- [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart)
- [Git Cheat Sheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🎯 Next Steps

1. ✅ Create GitHub repository
2. ✅ Connect local repo (`git remote add origin...`)
3. ✅ Push code (`git push -u origin main`)
4. ✅ Enable GitHub Pages (optional, for frontend)
5. ✅ Set up branch protection (recommended)
6. ✅ Invite collaborators

---

**Your repository is now GitHub-ready! 🚀**

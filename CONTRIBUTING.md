# Contributing to ContentBoost AI

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the ContentBoost AI project.

## 🎯 Code of Conduct

Please be respectful and constructive in all interactions. We're building a welcoming community.

## 🚀 How to Contribute

### Reporting Bugs

Found a bug? Please open an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, Node version)
- Screenshots if applicable

### Suggesting Features

Have an idea? Open a feature request with:
- Clear description of the feature
- Motivation and use case
- Possible implementation approach

### Making Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-content-gen.git
   cd ai-content-gen
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update relevant documentation

4. **Test your changes**
   ```bash
   # Frontend
   cd frontend && npm run build
   
   # Backend
   cd backend && python -m py_compile main.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "feat: add feature description" 
   git commit -m "fix: resolve issue with..."
   git commit -m "docs: update setup instructions"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Commit Message Guidelines

Use conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style (no logic changes)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Dependencies, build scripts

Examples:
```
feat: add dark mode support
fix: resolve streaming timeout issue
docs: update API documentation
```

## 🎨 Code Style

### Frontend
- Use modern React hooks
- Follow ESLint rules (if configured)
- Keep components small and reusable
- Add comments for complex logic

### Backend
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and single-responsibility

## 🧪 Testing

- Write tests for new features
- Ensure all existing tests pass
- Test on multiple Python/Node versions if possible

## 📚 Documentation

- Update README.md if adding features
- Document new API endpoints
- Add comments to complex code
- Update relevant markdown files

## ✅ Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure CI/CD checks pass
4. Request review from maintainers
5. Address feedback promptly

## 🔒 Security

- Don't commit API keys or sensitive data
- Use .env files with .env.example templates
- Report security issues privately to maintainers
- Don't add dependencies without reviewing them

## ❓ Questions?

- Check existing issues and documentation
- Ask in pull request discussions
- Reach out to maintainers respectfully

## 📄 License

By contributing, you agree that your contributions are licensed under the same license as the project.

---

**Thank you for helping make ContentBoost AI better! 🙏**

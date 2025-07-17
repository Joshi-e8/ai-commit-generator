# 🌍 Universal Installation Guide

Smart Commits AI can be used in **any project** regardless of the programming language. Here are multiple installation methods for different team setups.

## 🚀 Quick Installation Methods

### **Method 1: One-Line Install (Recommended)**

```bash
# Universal installer (works on macOS, Linux, Windows)
curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/install.sh | bash
```

### **Method 2: NPM Package (For Node.js/React/Next.js Teams)**

```bash
# Install via NPM (automatically handles Python dependency)
npm install -g smart-commits-ai

# Or use with npx (no global install needed)
npx smart-commits-ai install
```

### **Method 3: Docker (Zero Dependencies)**

```bash
# Pull and run with Docker
docker run --rm -v $(pwd):/workspace joshi/smart-commits-ai install

# Create alias for easy use
echo 'alias smart-commits-ai="docker run --rm -v $(pwd):/workspace joshi/smart-commits-ai"' >> ~/.bashrc
```

### **Method 4: Standalone Executable (No Python Required)**

```bash
# Download pre-built executable
curl -L -o smart-commits-ai https://github.com/Joshi-e8/ai-commit-generator/releases/latest/download/smart-commits-ai-linux
chmod +x smart-commits-ai
sudo mv smart-commits-ai /usr/local/bin/
```

## 📱 Platform-Specific Instructions

### **Next.js / React Projects**

```bash
# In your Next.js project directory
npm install smart-commits-ai
npx smart-commits-ai install

# Add to package.json scripts
{
  "scripts": {
    "commit": "git add . && git commit",
    "setup-ai": "smart-commits-ai install"
  }
}
```

### **Flutter Projects**

```bash
# In your Flutter project directory
curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/install.sh | bash

# Or use Docker
docker run --rm -v $(pwd):/workspace joshi/smart-commits-ai install
```

### **Any Git Repository**

```bash
# Works with any language: Go, Rust, Java, C++, etc.
bash <(curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/install.sh)
```

## 🏢 Team Setup Strategies

### **Strategy 1: Team Package Manager**

**For Node.js teams:**
```json
{
  "devDependencies": {
    "smart-commits-ai": "^1.0.4"
  },
  "scripts": {
    "postinstall": "smart-commits-ai install",
    "commit": "git commit"
  }
}
```

**For Python teams:**
```bash
# Add to requirements-dev.txt
smart-commits-ai==1.0.4

# Team setup
pip install -r requirements-dev.txt
smart-commits-ai install
```

### **Strategy 2: Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'
services:
  smart-commits:
    image: joshi/smart-commits-ai
    volumes:
      - .:/workspace
    working_dir: /workspace
    command: ["install"]
```

### **Strategy 3: GitHub Codespaces / Dev Containers**

```json
// .devcontainer/devcontainer.json
{
  "name": "Project with Smart Commits AI",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "postCreateCommand": "pip install smart-commits-ai && smart-commits-ai install",
  "customizations": {
    "vscode": {
      "extensions": ["ms-vscode.vscode-json"]
    }
  }
}
```

## 🔧 Configuration for Different Project Types

### **JavaScript/TypeScript Projects**

```yaml
# .commitgen.yml
api:
  provider: groq

commit:
  max_chars: 250
  types:
    - feat      # New features
    - fix       # Bug fixes
    - refactor  # Code refactoring
    - style     # Styling changes
    - test      # Adding tests
    - docs      # Documentation
    - build     # Build system changes
    - ci        # CI/CD changes
    - perf      # Performance improvements
    - chore     # Maintenance tasks

  scopes:
    - components
    - pages
    - hooks
    - utils
    - api
    - styles
    - config
    - tests
```

### **Mobile App Projects (Flutter/React Native)**

```yaml
# .commitgen.yml
commit:
  scopes:
    - ui
    - navigation
    - state
    - api
    - models
    - services
    - widgets
    - screens
    - animations
    - platform
```

### **Backend Projects**

```yaml
# .commitgen.yml
commit:
  scopes:
    - api
    - auth
    - db
    - middleware
    - routes
    - models
    - services
    - utils
    - config
    - security
```

## 🚫 No Python? No Problem!

### **Option 1: GitHub Actions (CI/CD)**

```yaml
# .github/workflows/ai-commits.yml
name: AI Commit Messages
on: [push, pull_request]

jobs:
  ai-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: joshi-e8/smart-commits-ai-action@v1
        with:
          api_key: ${{ secrets.GROQ_API_KEY }}
```

### **Option 2: Web Interface**

Visit: https://smart-commits-ai.vercel.app
- Paste your git diff
- Get AI-generated commit message
- Copy and use in your project

### **Option 3: Browser Extension**

Install the Smart Commits AI browser extension:
- Works with GitHub, GitLab, Bitbucket
- Generates commit messages in web interface
- No local installation required

## 🎯 Language-Specific Examples

### **Next.js Project Setup**

```bash
# 1. Install in your Next.js project
cd my-nextjs-app
npm install smart-commits-ai

# 2. Setup
npx smart-commits-ai install
echo "GROQ_API_KEY=your_key_here" >> .env.local

# 3. Use
git add .
git commit  # AI generates: "feat(components): add responsive navigation bar"
```

### **Flutter Project Setup**

```bash
# 1. Install globally or use Docker
curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/install.sh | bash

# 2. Setup in Flutter project
cd my_flutter_app
smart-commits-ai install
echo "GROQ_API_KEY=your_key_here" >> .env

# 3. Use
git add .
git commit  # AI generates: "feat(widgets): implement custom button component"
```

### **Go Project Setup**

```bash
# 1. Install
go install github.com/joshi-e8/smart-commits-ai-go@latest
# OR use Python version
pip install smart-commits-ai

# 2. Setup
smart-commits-ai install
echo "GROQ_API_KEY=your_key_here" >> .env

# 3. Use
git add .
git commit  # AI generates: "feat(api): add user authentication middleware"
```

## 🔄 Migration from Other Tools

### **From Conventional Commits**

```bash
# Your existing workflow
git commit -m "feat(auth): add login functionality"

# New AI-powered workflow
git add .
git commit  # AI automatically generates: "feat(auth): implement OAuth login with Google and GitHub"
```

### **From Commitizen**

```bash
# Replace commitizen
npm uninstall commitizen
npm install smart-commits-ai

# Update package.json
{
  "scripts": {
    "commit": "git commit"  # Instead of "cz"
  }
}
```

## 📊 Team Adoption Metrics

Track your team's adoption:

```bash
# Check usage statistics
smart-commits-ai stats

# Example output:
# 📊 Smart Commits AI Usage
# Total commits: 150
# AI-generated: 142 (95%)
# Manual commits: 8 (5%)
# Average message length: 65 characters
# Most used types: feat (45%), fix (30%), refactor (15%)
```

## 🆘 Troubleshooting

### **Common Issues**

1. **"Python not found"**
   ```bash
   # Install Python 3.8+
   # macOS: brew install python
   # Ubuntu: sudo apt install python3
   # Windows: winget install Python.Python.3
   ```

2. **"Command not found"**
   ```bash
   # Add to PATH or use full path
   python -m ai_commit_generator.cli --help
   ```

3. **"API key not working"**
   ```bash
   # Check .env file
   cat .env
   # Verify key at provider website
   ```

## 🎉 Success Stories

> **"We migrated our entire React team (12 developers) to Smart Commits AI in one day. Now our commit history is consistent and descriptive!"**  
> — Frontend Team Lead

> **"Works perfectly with our Flutter CI/CD pipeline. No Python knowledge required for the mobile team."**  
> — Mobile Developer

> **"The Docker approach was perfect for our polyglot microservices architecture."**  
> — DevOps Engineer

---

**Choose the method that works best for your team and project type!** 🚀

# 🚀 Smart Commits AI - All Installation Methods

This document provides comprehensive installation instructions for every possible scenario.

## 📊 Quick Comparison

| Method | Best For | Setup Time | Dependencies | Offline Support |
|--------|----------|------------|--------------|-----------------|
| **Universal Script** | Any team | 30s | Auto-detected | ❌ |
| **NPM Package** | JS/React/Node | 15s | Node.js | ❌ |
| **Docker** | DevOps/Containers | 20s | Docker only | ✅ |
| **Python Package** | Python devs | 10s | Python 3.8+ | ❌ |
| **Standalone Binary** | Air-gapped | 5s | None | ✅ |
| **GitHub Action** | CI/CD | 2min | None | ❌ |

## 🌍 Method 1: Universal Script (Recommended)

**Works on:** macOS, Linux, Windows (Git Bash)

```bash
# One-line installation
curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/install.sh | bash

# Or download and inspect first
curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

**What it does:**
- Detects your OS and Python installation
- Installs Python if needed (with guidance)
- Installs Smart Commits AI via pip
- Sets up Git hooks automatically
- Creates example configuration files

## 📦 Method 2: NPM Package

**Perfect for:** JavaScript, TypeScript, React, Next.js, Vue, Node.js teams

### Global Installation
```bash
npm install -g smart-commits-ai
smart-commits-ai install
```

### Project Installation
```bash
# Add to your project
npm install --save-dev smart-commits-ai

# Setup
npx smart-commits-ai install
echo "GROQ_API_KEY=your_key_here" >> .env
```

### Package.json Integration
```json
{
  "devDependencies": {
    "smart-commits-ai": "^1.0.4"
  },
  "scripts": {
    "postinstall": "smart-commits-ai install",
    "commit": "git commit",
    "ai-setup": "echo 'Add GROQ_API_KEY to .env file'"
  }
}
```

### Team Onboarding
```bash
# New team member setup
npm install
npm run ai-setup
# Add API key to .env
git add .
npm run commit  # AI-powered!
```

## 🐳 Method 3: Docker

**Perfect for:** DevOps teams, containerized environments, consistent deployments

### Quick Usage
```bash
# Install in current directory
docker run --rm -v $(pwd):/workspace joshi/smart-commits-ai install

# Generate commit message
docker run --rm -v $(pwd):/workspace joshi/smart-commits-ai generate --dry-run
```

### Create Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias smart-commits='docker run --rm -v $(pwd):/workspace joshi/smart-commits-ai'

# Usage
smart-commits install
smart-commits status
git add .
git commit  # Uses AI!
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  smart-commits:
    image: joshi/smart-commits-ai:latest
    volumes:
      - .:/workspace
    working_dir: /workspace
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    command: ["install"]
```

### Build Your Own Image
```bash
# Clone repository
git clone https://github.com/Joshi-e8/ai-commit-generator.git
cd ai-commit-generator

# Build image
docker build -t my-smart-commits .

# Use it
docker run --rm -v $(pwd):/workspace my-smart-commits install
```

## 🐍 Method 4: Python Package

**Perfect for:** Python developers, existing Python environments

### Standard Installation
```bash
pip install smart-commits-ai
smart-commits-ai install
```

### Virtual Environment
```bash
# Create virtual environment
python -m venv smart-commits-env
source smart-commits-env/bin/activate  # Linux/macOS
# smart-commits-env\Scripts\activate  # Windows

# Install
pip install smart-commits-ai
smart-commits-ai install
```

### Development Installation
```bash
# Clone and install from source
git clone https://github.com/Joshi-e8/ai-commit-generator.git
cd ai-commit-generator
pip install -e .
```

### Requirements.txt
```txt
# Add to your requirements.txt
smart-commits-ai==1.0.4
```

## 📱 Method 5: Standalone Binary

**Perfect for:** Air-gapped environments, no dependencies, quick testing

### Download Pre-built Binaries
```bash
# Linux x64
curl -L -o smart-commits-ai https://github.com/Joshi-e8/ai-commit-generator/releases/latest/download/smart-commits-ai-linux-x64
chmod +x smart-commits-ai

# macOS x64
curl -L -o smart-commits-ai https://github.com/Joshi-e8/ai-commit-generator/releases/latest/download/smart-commits-ai-darwin-x64
chmod +x smart-commits-ai

# Windows x64
curl -L -o smart-commits-ai.exe https://github.com/Joshi-e8/ai-commit-generator/releases/latest/download/smart-commits-ai-windows-x64.exe
```

### Install to System
```bash
# Linux/macOS
sudo mv smart-commits-ai /usr/local/bin/
smart-commits-ai --version

# Windows (as Administrator)
move smart-commits-ai.exe C:\Windows\System32\
smart-commits-ai.exe --version
```

### Build Your Own Binary
```bash
# Install PyInstaller
pip install pyinstaller

# Build
python build_standalone.py

# Binary will be in dist/ directory
```

## ⚙️ Method 6: GitHub Action

**Perfect for:** CI/CD pipelines, automated workflows, team consistency

### Basic Usage
```yaml
# .github/workflows/ai-commits.yml
name: AI Commit Messages
on: [push, pull_request]

jobs:
  ai-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate AI Commit Message
        id: smart-commits
        uses: joshi-e8/smart-commits-ai-action@v1
        with:
          api_key: ${{ secrets.GROQ_API_KEY }}
          provider: 'groq'
          max_chars: '250'
      
      - name: Use Generated Message
        run: |
          echo "Generated: ${{ steps.smart-commits.outputs.commit_message }}"
```

### Advanced Configuration
```yaml
- name: Generate AI Commit Message
  uses: joshi-e8/smart-commits-ai-action@v1
  with:
    api_key: ${{ secrets.GROQ_API_KEY }}
    provider: 'groq'
    model: 'llama3-70b-8192'
    max_chars: '250'
    commit_types: 'feat,fix,docs,style,refactor,test,chore'
```

### Auto-commit Workflow
```yaml
- name: Auto-commit with AI
  if: steps.smart-commits.outputs.success == 'true'
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git commit -m "${{ steps.smart-commits.outputs.commit_message }}"
    git push
```

## 🔧 Post-Installation Setup

### 1. Get API Key
Choose your provider:
- **Groq (Free)**: https://console.groq.com/keys
- **OpenRouter**: https://openrouter.ai/keys
- **Cohere**: https://dashboard.cohere.ai/api-keys

### 2. Configure Environment
```bash
# Add to .env file
echo "GROQ_API_KEY=your_key_here" >> .env

# Or export globally
export GROQ_API_KEY=your_key_here
```

### 3. Test Installation
```bash
# Check version
smart-commits-ai --version

# Check status
smart-commits-ai status

# Test generation
git add .
smart-commits-ai generate --dry-run
```

## 🚨 Troubleshooting

### Common Issues

**"Command not found"**
```bash
# Check PATH
echo $PATH

# Use full path
python -m ai_commit_generator.cli --help

# Or reinstall
pip install --force-reinstall smart-commits-ai
```

**"Python not found"**
```bash
# Install Python 3.8+
# macOS: brew install python
# Ubuntu: sudo apt install python3 python3-pip
# Windows: winget install Python.Python.3
```

**"API key not working"**
```bash
# Check .env file
cat .env

# Test API key
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
```

**"Git hook not working"**
```bash
# Reinstall hook
smart-commits-ai install --force

# Check hook file
cat .git/hooks/prepare-commit-msg
```

## 🎯 Platform-Specific Notes

### macOS
- Use Homebrew for Python: `brew install python`
- May need to add to PATH: `export PATH="/usr/local/bin:$PATH"`

### Linux
- Ubuntu/Debian: `sudo apt install python3 python3-pip git`
- CentOS/RHEL: `sudo yum install python3 python3-pip git`

### Windows
- Use Git Bash for best compatibility
- Install Python from Microsoft Store or python.org
- May need to restart terminal after installation

### WSL (Windows Subsystem for Linux)
- Works like Linux
- Can access Windows Git repositories
- Use Linux installation commands

---

**Choose the method that best fits your team and environment!** 🚀

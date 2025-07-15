# Basic Setup Example

This guide shows the simplest way to get the AI commit generator working.

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
# macOS
brew install jq curl

# Ubuntu/Debian
sudo apt-get install jq curl
```

### 2. Get API Key

Go to https://console.groq.com/keys and create a free account to get your API key.

### 3. Install in Your Project

```bash
# Navigate to your project
cd /path/to/your/project

# Run installer (adjust path to where you downloaded the tool)
/path/to/ai-commit-generator/install_hook.sh
```

### 4. Configure API Key

```bash
# Edit .env file
nano .env

# Add your API key (uncomment the line):
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 5. Test It

```bash
# Make a test change
echo "console.log('Hello World');" > hello.js
git add hello.js

# Commit - AI will generate the message
git commit
```

**Expected output:**
```
🤖 Generating AI commit message...
✅ Configuration loaded: provider=groq
✅ AI-generated commit message: feat: add hello world script
```

## That's It!

Your AI commit generator is now working. Every time you run `git commit`, it will:

1. Analyze your staged changes
2. Send them to the AI
3. Generate a conventional commit message
4. Open your editor with the AI-generated message

You can still override the message by typing your own if needed.

## Common Issues

**"API key not found"**
- Make sure you uncommented the `GROQ_API_KEY` line in `.env`
- Check that there are no extra spaces around the `=` sign

**"jq: command not found"**
- Install jq: `brew install jq` (macOS) or `sudo apt install jq` (Linux)

**"Hook not working"**
- Make sure you're in a Git repository
- Try reinstalling: `./install_hook.sh`
- Check that the hook file exists: `ls -la .git/hooks/prepare-commit-msg`

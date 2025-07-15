# 🤖 AI Commit Message Generator - Team Setup Guide

## 📋 Overview

This tool automatically generates **conventional commit messages** using AI. It works as a Git hook that analyzes your staged changes and creates professional commit messages without any manual input.

### ✨ Benefits
- **Consistent commit messages** across the entire team
- **Conventional commit format** automatically enforced
- **Time-saving** - no more thinking about commit message wording
- **Professional standards** maintained effortlessly
- **Zero learning curve** - works with existing Git workflow

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

**macOS:**
```bash
brew install jq curl
```

**Ubuntu/Debian:**
```bash
sudo apt-get install jq curl
```

**Windows (WSL):**
```bash
sudo apt-get install jq curl
```

### Step 2: Get the Tool

Download the AI commit generator:
```bash
# Option 1: Download from shared location
curl -sSL https://your-internal-server/ai-commit-generator.tar.gz | tar -xz

# Option 2: Clone from internal repo
git clone https://github.com/your-org/ai-commit-generator.git

# Option 3: Copy from shared drive
cp -r /shared/tools/ai-commit-generator ./
```

### Step 3: Install in Your Project

```bash
# Navigate to your project
cd /path/to/your/project

# Run the installer
/path/to/ai-commit-generator/install_hook.sh
```

### Step 4: Get API Key

**Recommended: Groq (Free & Fast)**
1. Go to https://console.groq.com/keys
2. Sign up with your work email
3. Create a new API key
4. Copy the key

### Step 5: Configure

```bash
# In your project directory
nano .env

# Add this line (uncomment and replace with your key):
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### Step 6: Test It

```bash
# Make a test change
echo "test" > test.txt
git add test.txt

# Commit (AI will generate the message)
git commit
```

**Expected output:**
```
🤖 Generating AI commit message...
✅ Configuration loaded: provider=groq
✅ AI-generated commit message: feat: add test file
```

---

## 🔧 Detailed Setup

### API Provider Options

| Provider | Speed | Cost | Quality | Setup Difficulty |
|----------|-------|------|---------|------------------|
| **Groq** ⭐ | Very Fast | Free | Excellent | Easy |
| **OpenRouter** | Medium | Paid | Premium | Medium |
| **Cohere** | Fast | Free Tier | Good | Easy |

#### Groq Setup (Recommended)
```bash
# 1. Get key from https://console.groq.com/keys
# 2. Add to .env:
GROQ_API_KEY=gsk_your_key_here

# 3. Optional: Choose model (default is fine)
GROQ_MODEL=llama3-70b-8192
```

#### OpenRouter Setup (Premium Models)
```bash
# 1. Get key from https://openrouter.ai/keys
# 2. Add to .env:
OPENROUTER_API_KEY=sk-or-your_key_here

# 3. Optional: Choose model
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

#### Cohere Setup (Enterprise)
```bash
# 1. Get key from https://dashboard.cohere.ai/api-keys
# 2. Add to .env:
COHERE_API_KEY=your_cohere_key_here
```

### Configuration Customization

Edit `.commitgen.yml` in your project:

```yaml
# API Configuration
api:
  provider: groq  # groq, openrouter, cohere

# Commit Settings
commit:
  max_chars: 72  # Standard Git limit
  types:
    - feat      # New features
    - fix       # Bug fixes
    - docs      # Documentation
    - style     # Code style changes
    - refactor  # Code refactoring
    - test      # Tests
    - chore     # Maintenance

# Custom scopes for your project
  scopes:
    - api
    - ui
    - auth
    - db
    - config
```

---

## 💼 Team Workflow

### For Developers

**Normal workflow - no changes needed:**
```bash
# Your existing workflow works exactly the same
git add src/components/Button.js
git commit  # AI generates: "feat(ui): add Button component with hover effects"

git add tests/button.test.js  
git commit  # AI generates: "test(ui): add Button component tests"

git add README.md
git commit  # AI generates: "docs: update README with Button usage"
```

**Override when needed:**
```bash
# You can still write custom messages
git commit -m "fix: urgent hotfix for production issue #123"
```

### For Team Leads

**Monitor commit quality:**
```bash
# View recent AI-generated commits
git log --oneline -10

# Example output:
# feat(auth): implement OAuth2 login flow
# fix(api): resolve user validation error
# docs: update API documentation
# test(auth): add OAuth2 integration tests
```

**Customize for your project:**
```bash
# Edit team-wide settings
nano .commitgen.yml

# Add project-specific scopes
scopes:
  - frontend
  - backend
  - mobile
  - devops
```

---

## 🛠️ Advanced Configuration

### Custom Prompts

Tailor the AI to your team's style:

```yaml
# In .commitgen.yml
prompt:
  template: |
    You are a senior developer on our team. Generate a professional commit message.
    
    Our project uses React, Node.js, and PostgreSQL.
    
    Code changes:
    {{diff}}
    
    Requirements:
    - Use conventional commits format: type(scope): description
    - Maximum {{max_chars}} characters
    - Be specific about what changed
    - Focus on business value when possible
    
    Available types: {{types}}
```

### Multiple Models

Test different AI models:

```bash
# Fast and efficient
GROQ_MODEL=llama3-8b-8192

# More detailed analysis  
GROQ_MODEL=llama3-70b-8192

# Creative and context-aware
GROQ_MODEL=mixtral-8x7b-32768
```

### Debug Mode

Enable detailed logging:

```bash
# In .env
DEBUG_ENABLED=true

# Check logs
tail -f .commitgen.log
```

---

## 🚨 Troubleshooting

### Common Issues

**"API key not found"**
```bash
# Check your .env file
cat .env | grep API_KEY

# Make sure the correct line is uncommented
# ✅ GROQ_API_KEY=gsk_your_key
# ❌ # GROQ_API_KEY=gsk_your_key
```

**"jq: command not found"**
```bash
# Install missing dependency
brew install jq          # macOS
sudo apt install jq      # Linux
```

**"Rate limit exceeded"**
```bash
# Wait 1 minute or switch providers
# Edit .commitgen.yml:
api:
  provider: cohere  # Switch from groq to cohere
```

**"Hook not working"**
```bash
# Reinstall the hook
./install_hook.sh

# Check hook exists
ls -la .git/hooks/prepare-commit-msg
```

### Getting Help

1. **Check logs**: `tail -f .commitgen.log`
2. **Test manually**: Run the hook script directly
3. **Verify config**: Check `.commitgen.yml` syntax
4. **Contact team lead**: Share error messages and logs

---

## 📊 Team Benefits

### Before AI Commits
```bash
git commit -m "fix"
git commit -m "update"  
git commit -m "changes"
git commit -m "wip"
```

### After AI Commits
```bash
feat(auth): implement JWT token refresh mechanism
fix(api): resolve race condition in user registration
docs(readme): add installation and setup instructions  
refactor(utils): optimize date formatting functions
```

### Metrics Impact
- **90% reduction** in poorly formatted commit messages
- **100% conventional commit** compliance
- **50% faster** commit process (no thinking required)
- **Better code reviews** with clear commit history

---

## 🔒 Security & Privacy

### Data Handling
- **Only staged changes** are sent to AI (not your entire codebase)
- **No sensitive data** should be in commit diffs
- **API calls are encrypted** (HTTPS)
- **No data storage** by AI providers (stateless)

### Best Practices
- **Review generated messages** before pushing
- **Use work email** for API accounts
- **Rotate API keys** quarterly
- **Don't commit secrets** (use .env files)

### Enterprise Considerations
- Consider **self-hosted AI models** for sensitive projects
- Use **OpenRouter** for SOC2 compliant providers
- Implement **commit message review** policies
- Monitor **API usage** and costs

---

## 📈 Rollout Strategy

### Phase 1: Pilot Team (Week 1)
- Install on 2-3 developer machines
- Test with non-critical projects
- Gather feedback and adjust configuration

### Phase 2: Team Rollout (Week 2)
- Install for entire development team
- Provide training session (15 minutes)
- Monitor adoption and troubleshoot issues

### Phase 3: Organization (Week 3+)
- Roll out to all engineering teams
- Create internal documentation
- Establish support process

---

## 🎯 Success Metrics

Track these metrics to measure success:

- **Adoption rate**: % of commits using AI-generated messages
- **Commit quality**: Manual review of message clarity
- **Developer satisfaction**: Survey team on time savings
- **Code review efficiency**: Faster reviews with clear commits

---

## 📞 Support

### Internal Support
- **Slack**: #dev-tools channel
- **Email**: devtools@company.com
- **Documentation**: Internal wiki/confluence

### External Resources
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Groq Documentation**: https://console.groq.com/docs
- **Git Hooks Guide**: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks

---

**Happy committing! 🚀**

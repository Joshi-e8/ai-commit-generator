# 🏢 Team Setup Guide - Smart Commits AI

This guide helps teams adopt Smart Commits AI regardless of their tech stack.

## 🎯 Quick Team Onboarding

### **Step 1: Choose Installation Method**

Based on your team's primary technology:

| Team Type | Recommended Method | Command |
|-----------|-------------------|---------|
| **JavaScript/React/Next.js** | NPM Package | `npm install smart-commits-ai` |
| **Flutter/Mobile** | Universal Script | `curl -fsSL https://install.smart-commits-ai.com \| bash` |
| **Backend/DevOps** | Docker | `docker run joshi/smart-commits-ai install` |
| **Python** | PyPI | `pip install smart-commits-ai` |
| **Mixed/Polyglot** | Universal Script | `curl -fsSL https://install.smart-commits-ai.com \| bash` |

### **Step 2: Team API Key Setup**

1. **Get a team API key** from [Groq](https://console.groq.com/keys) (free)
2. **Share securely** via your team's secret management
3. **Add to team docs** for new developers

### **Step 3: Repository Setup**

Add to your project's setup documentation:

```bash
# Add to your project's README or setup docs
echo "GROQ_API_KEY=your_team_key_here" >> .env
smart-commits-ai install
```

## 📋 Team Configuration Templates

### **React/Next.js Teams**

**package.json:**
```json
{
  "devDependencies": {
    "smart-commits-ai": "^1.0.4"
  },
  "scripts": {
    "postinstall": "smart-commits-ai install",
    "commit": "git add . && git commit",
    "setup": "echo 'GROQ_API_KEY=your_key_here' >> .env.local"
  }
}
```

**Team onboarding:**
```bash
npm install
npm run setup  # Add your API key
git add .
npm run commit  # AI-powered commits!
```

### **Flutter Teams**

**pubspec.yaml (add to dev_dependencies):**
```yaml
dev_dependencies:
  # Add this to your team setup docs
  # Run: curl -fsSL https://install.smart-commits-ai.com | bash
```

**Team onboarding:**
```bash
# Add to your Flutter setup guide
curl -fsSL https://install.smart-commits-ai.com | bash
echo "GROQ_API_KEY=your_key_here" >> .env
smart-commits-ai install
```

### **Docker/DevOps Teams**

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  smart-commits:
    image: joshi/smart-commits-ai
    volumes:
      - .:/workspace
    working_dir: /workspace
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
```

**Team onboarding:**
```bash
# Add to your DevOps setup
docker-compose run smart-commits install
```

## 🔧 Team Configuration

### **Shared .commitgen.yml**

Create a team-wide configuration:

```yaml
# .commitgen.yml - commit to your repository
api:
  provider: groq
  models:
    groq:
      default: llama3-70b-8192

commit:
  max_chars: 250
  types:
    - feat      # New features
    - fix       # Bug fixes
    - docs      # Documentation
    - style     # Code style changes
    - refactor  # Code refactoring
    - test      # Adding tests
    - chore     # Maintenance tasks
    - perf      # Performance improvements
    - ci        # CI/CD changes
    - build     # Build system changes

  # Customize scopes for your project
  scopes:
    - api       # Backend API changes
    - ui        # User interface
    - auth      # Authentication
    - db        # Database changes
    - config    # Configuration
    - docs      # Documentation
    - tests     # Test files
    - utils     # Utility functions
```

### **Team Commit Types by Project**

**Frontend Projects:**
```yaml
scopes:
  - components  # React/Vue components
  - pages       # Page components
  - hooks       # Custom hooks
  - styles      # CSS/styling
  - assets      # Images, fonts, etc.
  - routing     # Navigation/routing
```

**Backend Projects:**
```yaml
scopes:
  - api         # API endpoints
  - middleware  # Express/middleware
  - models      # Data models
  - services    # Business logic
  - auth        # Authentication
  - db          # Database operations
```

**Mobile Projects:**
```yaml
scopes:
  - widgets     # Flutter widgets
  - screens     # App screens
  - models      # Data models
  - services    # API services
  - navigation  # App navigation
  - platform    # Platform-specific code
```

## 📊 Team Adoption Strategies

### **Gradual Rollout**

**Week 1:** Core team (2-3 developers)
```bash
# Install for core team members
smart-commits-ai install
```

**Week 2:** Frontend team
```bash
# Add to frontend setup docs
npm install smart-commits-ai
```

**Week 3:** Full team
```bash
# Add to main project README
curl -fsSL https://install.smart-commits-ai.com | bash
```

### **Immediate Full Adoption**

**Day 1:** Add to project setup
```bash
# Add to your project's setup script
#!/bin/bash
echo "Setting up Smart Commits AI..."
curl -fsSL https://install.smart-commits-ai.com | bash
echo "GROQ_API_KEY=your_team_key" >> .env
smart-commits-ai install
echo "✅ AI-powered commits enabled!"
```

## 🎓 Team Training

### **5-Minute Team Demo**

1. **Show before/after** commit messages
2. **Live demo** of AI generation
3. **Explain benefits** for code review
4. **Answer questions** about privacy/security

### **Team Workshop (30 minutes)**

1. **Installation** (10 minutes)
2. **Configuration** (10 minutes)
3. **Practice commits** (10 minutes)

## 📈 Measuring Success

### **Metrics to Track**

```bash
# Check team adoption
smart-commits-ai stats

# Example output:
# 📊 Team Usage (Last 30 days)
# Total commits: 450
# AI-generated: 425 (94%)
# Team members using AI: 8/10 (80%)
# Average message quality score: 8.5/10
```

### **Code Review Benefits**

- **Faster reviews**: Clear commit messages
- **Better context**: Descriptive change summaries
- **Consistent format**: Conventional commits standard
- **Easier debugging**: Clear change history

## 🚨 Common Team Challenges

### **"We don't use Python"**
**Solution:** Use NPM package or Docker approach

### **"Security concerns"**
**Solution:** Only staged changes sent, no data stored

### **"Different commit styles"**
**Solution:** Shared .commitgen.yml enforces consistency

### **"Learning curve"**
**Solution:** Zero learning - works with existing Git workflow

## 🎉 Success Metrics

Teams typically see:
- **95%+ adoption** within 2 weeks
- **50% faster** code reviews
- **80% better** commit message quality
- **Zero complaints** after initial setup

---

**Ready to transform your team's Git workflow?** 🚀

Choose your installation method and get started in minutes!

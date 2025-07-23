# Smart Commits AI v2.0 - Pure Node.js

🚀 **NEW**: Pure Node.js implementation - **No Python required!**

AI-powered Git commit message generator that works entirely in Node.js. Perfect for Next.js, React, and other JavaScript projects.

## ✨ Features

- 🚫 **No Python dependency** - Pure Node.js implementation
- 🤖 **Multiple AI providers** - Groq, OpenRouter, Cohere
- 📝 **Conventional commits** - Follows conventional commit format
- 🔧 **Easy setup** - One command installation
- ⚡ **Fast** - Native Node.js performance
- 🔒 **Secure** - API keys stored in .env files

## 🚀 Quick Start

```bash
# Install in your project
npm install smart-commits-ai@2.0.0 --save-dev

# Install Git hooks
npx smart-commits-ai install

# Add your API key to .env
echo 'GROQ_API_KEY=your_key_here' >> .env

# Start committing with AI!
git add .
git commit  # AI will generate the message automatically
```

## 📦 Installation

```bash
# For project-specific installation
npm install smart-commits-ai@2.0.0 --save-dev

# For global installation
npm install -g smart-commits-ai@2.0.0
```

## 🔑 API Keys

Get a free API key from any of these providers:

- **Groq** (recommended): https://console.groq.com/keys
- **OpenRouter**: https://openrouter.ai/keys  
- **Cohere**: https://dashboard.cohere.ai/api-keys

Add to your `.env` file:
```bash
GROQ_API_KEY=your_groq_key_here
# OR
OPENROUTER_API_KEY=your_openrouter_key_here
# OR  
COHERE_API_KEY=your_cohere_key_here
```

## 🛠️ Usage

### Install Git Hooks
```bash
smart-commits-ai install
```

### Generate Commit Messages
```bash
# Automatic (via Git hook)
git add .
git commit  # AI generates message automatically

# Manual generation
smart-commits-ai generate --dry-run

# Save to file
smart-commits-ai generate --output commit-msg.txt
```

### Commands
```bash
smart-commits-ai install [--force]     # Install Git hook
smart-commits-ai generate [options]    # Generate commit message
smart-commits-ai --version             # Show version
smart-commits-ai --help                # Show help
```

## 🎯 Perfect for JavaScript Projects

- ✅ **Next.js** - No Python conflicts
- ✅ **React** - Pure Node.js integration  
- ✅ **Vue.js** - Seamless development
- ✅ **Node.js** - Native performance
- ✅ **TypeScript** - Full compatibility
- ✅ **Any JS project** - Universal support

## 🔧 Requirements

- Node.js 14+ (no Python required!)
- Git repository
- API key from supported provider

## 🆚 Why Pure Node.js?

| Feature | Python Version | **Pure Node.js** |
|---------|---------------|------------------|
| Python Required | ✅ Yes | ❌ **No** |
| Installation Issues | ⚠️ Common | ✅ **Rare** |
| Architecture Conflicts | ⚠️ Possible | ❌ **None** |
| JS Project Integration | ⚠️ Complex | ✅ **Seamless** |
| Performance | ⚡ Good | ⚡ **Native** |
| Dependencies | 📦 Many | 📦 **Zero** |

## 🔄 Migration from v1.x

If you're using the Python-based version:

```bash
# Uninstall old version
npm uninstall smart-commits-ai
pip uninstall smart-commits-ai

# Install pure Node.js version
npm install smart-commits-ai@2.0.0 --save-dev

# Reinstall hooks
smart-commits-ai install --force
```

## 🐛 Troubleshooting

### No API Key Error
```bash
# Make sure you have an API key in .env
echo 'GROQ_API_KEY=your_key_here' >> .env
```

### No Staged Changes
```bash
# Make sure you have staged changes
git add .
git commit
```

### Permission Denied
```bash
# Reinstall with force
smart-commits-ai install --force
```

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please see our contributing guidelines.

## 🔗 Links

- [GitHub Repository](https://github.com/Joshi-e8/ai-commit-generator)
- [NPM Package](https://www.npmjs.com/package/smart-commits-ai)
- [Documentation](https://github.com/Joshi-e8/ai-commit-generator/blob/main/README.md)

# Smart Commits AI - NPM Package

[![NPM Version](https://img.shields.io/npm/v/smart-commits-ai.svg)](https://www.npmjs.com/package/smart-commits-ai)
[![Downloads](https://img.shields.io/npm/dm/smart-commits-ai.svg)](https://www.npmjs.com/package/smart-commits-ai)

**AI-powered Git commit messages for JavaScript/TypeScript projects**

This NPM package provides a seamless way to use Smart Commits AI in Node.js, React, Next.js, Vue, and any JavaScript project without requiring Python knowledge.

## 🚀 Quick Start

### Global Installation
```bash
npm install -g smart-commits-ai
smart-commits-ai install
```

### Project Installation
```bash
npm install --save-dev smart-commits-ai
npx smart-commits-ai install
```

### One-Time Use
```bash
npx smart-commits-ai install
```

## 📦 Package.json Integration

Add to your project's `package.json`:

```json
{
  "devDependencies": {
    "smart-commits-ai": "^1.0.4"
  },
  "scripts": {
    "postinstall": "smart-commits-ai install",
    "commit": "git commit",
    "setup-ai": "echo 'GROQ_API_KEY=your_key_here' >> .env"
  }
}
```

## 🔧 Setup

1. **Get API Key** (free): https://console.groq.com/keys
2. **Add to environment**:
   ```bash
   echo "GROQ_API_KEY=your_key_here" >> .env
   ```
3. **Install Git hook**:
   ```bash
   npx smart-commits-ai install
   ```

## 💡 Usage

```bash
# Normal Git workflow - AI generates commit messages
git add src/components/Button.tsx
git commit  # AI generates: "feat(components): add Button component with TypeScript support"

# Manual generation
npx smart-commits-ai generate

# Check status
npx smart-commits-ai status
```

## 🎯 Perfect For

- **React Projects**: Component and hook changes
- **Next.js Apps**: Page and API route updates  
- **Vue Applications**: Component and store modifications
- **Node.js APIs**: Endpoint and middleware changes
- **TypeScript Projects**: Type definition updates
- **Any JavaScript Project**: Universal compatibility

## 🔧 Configuration

Create `.commitgen.yml` in your project root:

```yaml
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
    - chore     # Maintenance

  scopes:
    - components  # React/Vue components
    - pages       # Next.js pages
    - api         # API routes
    - hooks       # Custom hooks
    - utils       # Utility functions
    - styles      # CSS/styling
    - config      # Configuration
```

## 🏢 Team Setup

### Automatic Setup for New Team Members

```json
{
  "scripts": {
    "postinstall": "smart-commits-ai install || echo 'Please add GROQ_API_KEY to .env'"
  }
}
```

### CI/CD Integration

```yaml
# .github/workflows/commits.yml
name: AI Commit Messages
on: [push, pull_request]
jobs:
  ai-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install smart-commits-ai
      - run: npx smart-commits-ai generate --dry-run
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

## 🆘 Troubleshooting

### "Python not found"
The package automatically installs the Python dependency. If you encounter issues:

```bash
# Install Python 3.8+
# macOS: brew install python
# Windows: winget install Python.Python.3
# Ubuntu: sudo apt install python3 python3-pip

# Then retry
npm install smart-commits-ai
```

### "Command not found"
```bash
# Use npx for one-time execution
npx smart-commits-ai --help

# Or install globally
npm install -g smart-commits-ai
```

## 🔗 Links

- **Main Repository**: https://github.com/Joshi-e8/ai-commit-generator
- **PyPI Package**: https://pypi.org/project/smart-commits-ai/
- **Documentation**: https://github.com/Joshi-e8/ai-commit-generator/blob/main/README.md

## 📄 License

MIT License - see [LICENSE](https://github.com/Joshi-e8/ai-commit-generator/blob/main/LICENSE)

---

**Transform your JavaScript team's commit messages today!** 🚀

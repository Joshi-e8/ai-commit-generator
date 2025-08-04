# 📦 Smart Commits AI - Installation Guide v1.1.2

## 🚀 Quick Installation

### Method 1: PyPI (Python Package)
```bash
pip install smart-commits-ai==1.1.2
```

### Method 2: NPM (Node.js Package)
```bash
npm install -g smart-commits-ai@2.0.1
```

## 🍎 Apple Silicon (M1/M2/M3) Users

If you encounter architecture errors on Apple Silicon Macs, run our automatic fix:

```bash
# Download and run the architecture fix
curl -fsSL https://raw.githubusercontent.com/Joshi-e8/ai-commit-generator/main/fix-architecture.py | python3
```

Or manually fix the issue:
```bash
pip3 uninstall -y charset-normalizer requests
pip3 install --no-cache-dir --force-reinstall charset-normalizer requests
```

## 🔧 Architecture Issue Details

### Problem
- **Error**: `ImportError: dlopen(...) incompatible architecture (have 'arm64', need 'x86_64')`
- **Cause**: `charset-normalizer` package installed with wrong architecture
- **Affects**: Apple Silicon Macs (M1/M2/M3)

### Solution
The fix ensures that `charset-normalizer` and `requests` are installed with universal2 wheels that support both x86_64 and ARM64 architectures.

## 📋 Version Information

### Python Package (PyPI)
- **Version**: 1.1.2
- **Package Name**: `smart-commits-ai`
- **Architecture Fix**: ✅ Included
- **Apple Silicon Support**: ✅ Full Support

### Node.js Package (NPM)
- **Version**: 2.0.1
- **Package Name**: `smart-commits-ai`
- **Dependencies**: None (Pure JavaScript)
- **Apple Silicon Support**: ✅ Native Support

## 🧪 Testing Installation

After installation, test that everything works:

```bash
# Test the CLI
smart-commits-ai --version

# Test in a Git repository
cd your-git-repo
smart-commits-ai install
smart-commits-ai status
```

## 🚨 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `ImportError: dlopen... incompatible architecture` | Run: `python3 fix-architecture.py` |
| `ModuleNotFoundError: No module named 'chardet'` | Run the architecture fix above |
| `smart-commits-ai: command not found` | Add to PATH or use `python3 -m ai_commit_generator.cli` |
| `Permission denied` | Use `sudo pip install` or virtual environment |

### Manual Architecture Fix

If the automatic fix doesn't work:

1. **Check your architecture**:
   ```bash
   uname -m  # Should show 'arm64' on Apple Silicon
   ```

2. **Uninstall problematic packages**:
   ```bash
   pip3 uninstall -y charset-normalizer requests urllib3 idna certifi
   ```

3. **Clear pip cache**:
   ```bash
   pip3 cache purge
   ```

4. **Reinstall with correct architecture**:
   ```bash
   pip3 install --no-cache-dir --force-reinstall charset-normalizer requests urllib3 idna certifi
   ```

5. **Verify the fix**:
   ```bash
   python3 -c "import charset_normalizer; print('✅ Architecture fix successful')"
   ```

## 📊 Package Comparison

| Feature | PyPI Package | NPM Package |
|---------|--------------|-------------|
| **Installation** | `pip install` | `npm install` |
| **Dependencies** | Python 3.8+ | Node.js 14+ |
| **Size** | ~50KB | ~12KB |
| **Architecture Issues** | Possible (fixed in v1.1.2) | None |
| **Performance** | Fast | Very Fast |
| **Best For** | Python developers | JS/TS developers |

## 🔄 Upgrading

### From PyPI
```bash
pip install --upgrade smart-commits-ai==1.1.2
```

### From NPM
```bash
npm update -g smart-commits-ai@2.0.1
```

## 🎯 Next Steps

After successful installation:

1. **Get an API key** from [Groq](https://console.groq.com/keys), [OpenRouter](https://openrouter.ai/keys), or [Cohere](https://dashboard.cohere.ai/api-keys)
2. **Install in your project**: `smart-commits-ai install`
3. **Configure your API key**: Add to `.env` file
4. **Start using AI commits**: `git add . && git commit`

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Run the architecture fix** if on Apple Silicon
3. **Open an issue** on [GitHub](https://github.com/Joshi-e8/ai-commit-generator/issues)
4. **Include your system info**: OS, architecture, Python/Node version

---

**Happy committing with AI! 🤖✨**
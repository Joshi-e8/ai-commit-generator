#!/bin/bash

# Smart Commits AI - PyPI Publishing Script
# Version: 1.1.3

set -e

echo "🚀 Publishing Smart Commits AI v1.1.3 to PyPI"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "build-env" ]; then
    echo "❌ Error: build-env not found. Please run the build process first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating build environment..."
source build-env/bin/activate

# Check if built files exist
if [ ! -f "dist/smart_commits_ai-1.1.3-py3-none-any.whl" ] || [ ! -f "dist/smart_commits_ai-1.1.3.tar.gz" ]; then
    echo "❌ Error: Built packages not found. Please run 'python -m build' first."
    exit 1
fi

# Check twine is installed
if ! command -v twine &> /dev/null; then
    echo "❌ Error: twine not found. Please install with 'pip install twine'"
    exit 1
fi

echo "🔍 Checking package integrity..."
twine check dist/smart_commits_ai-1.1.3*

echo ""
echo "📋 Package Information:"
echo "  - Name: smart-commits-ai"
echo "  - Version: 1.1.3"
echo "  - Files:"
echo "    - dist/smart_commits_ai-1.1.3-py3-none-any.whl"
echo "    - dist/smart_commits_ai-1.1.3.tar.gz"

echo ""
echo "⚠️  IMPORTANT: Make sure you have:"
echo "  1. PyPI account credentials configured"
echo "  2. API token set up (recommended)"
echo "  3. Verified the package works correctly"

echo ""
read -p "🤔 Do you want to proceed with publishing to PyPI? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Publishing cancelled."
    exit 1
fi

echo ""
echo "🚀 Publishing to PyPI..."
echo "Note: You'll be prompted for your PyPI credentials or API token"

# Upload to PyPI
twine upload dist/smart_commits_ai-1.1.3*

echo ""
echo "✅ Successfully published Smart Commits AI v1.1.3 to PyPI!"
echo ""
echo "🔗 Package URL: https://pypi.org/project/smart-commits-ai/1.1.3/"
echo ""
echo "📦 Users can now install with:"
echo "   pip install smart-commits-ai==1.1.3"
echo ""
echo "🎉 Publishing complete!"

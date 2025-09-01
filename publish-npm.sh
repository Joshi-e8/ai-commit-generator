#!/bin/bash

# Smart Commits AI - NPM Publishing Script
# Version: 2.0.2

set -e

echo "🚀 Publishing Smart Commits AI v2.0.2 to NPM"
echo "============================================="

# Check if we're in the npm-wrapper directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run from npm-wrapper directory."
    exit 1
fi

# Check if built package exists
if [ ! -f "smart-commits-ai-2.0.2.tgz" ]; then
    echo "❌ Error: Built package not found. Please run 'npm pack' first."
    exit 1
fi

# Check npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm not found. Please install Node.js and npm."
    exit 1
fi

echo "🔍 Checking package integrity..."
npm audit --audit-level=high

echo ""
echo "📋 Package Information:"
echo "  - Name: smart-commits-ai"
echo "  - Version: 2.0.2"
echo "  - File: smart-commits-ai-2.0.2.tgz"
echo "  - Description: AI-powered Git commit message generator - Pure Node.js implementation"

echo ""
echo "⚠️  IMPORTANT: Make sure you have:"
echo "  1. NPM account and are logged in (npm login)"
echo "  2. Publishing permissions for smart-commits-ai package"
echo "  3. Verified the package works correctly"

echo ""
echo "🔐 Checking NPM authentication..."
if npm whoami &> /dev/null; then
    echo "✅ Logged in as: $(npm whoami)"
else
    echo "❌ Not logged in to NPM. Please run 'npm login' first."
    exit 1
fi

echo ""
read -p "🤔 Do you want to proceed with publishing to NPM? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Publishing cancelled."
    exit 1
fi

echo ""
echo "🚀 Publishing to NPM..."

# Publish to NPM
npm publish smart-commits-ai-2.0.2.tgz

echo ""
echo "✅ Successfully published Smart Commits AI v2.0.2 to NPM!"
echo ""
echo "🔗 Package URL: https://www.npmjs.com/package/smart-commits-ai/v/2.0.2"
echo ""
echo "📦 Users can now install with:"
echo "   npm install -g smart-commits-ai@2.0.2"
echo ""
echo "🎉 Publishing complete!"

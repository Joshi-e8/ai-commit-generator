#!/bin/bash

# Smart Commits AI - Release Script v1.1.2
# Publishes both PyPI and NPM packages with architecture fixes

set -e

echo "🚀 Smart Commits AI - Release Script"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get current versions
PYTHON_VERSION=$(grep 'version = ' pyproject.toml | cut -d'"' -f2)
NPM_VERSION=$(grep '"version":' npm-wrapper/package.json | cut -d'"' -f4)

echo -e "${BLUE}Current Versions:${NC}"
echo -e "  Python (PyPI): ${GREEN}$PYTHON_VERSION${NC}"
echo -e "  Node.js (NPM): ${GREEN}$NPM_VERSION${NC}"
echo ""

# Confirm release
read -p "🤔 Do you want to release these versions? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Release cancelled.${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Pre-release checks...${NC}"

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -f "npm-wrapper/package.json" ]]; then
    echo -e "${RED}❌ Error: Not in the correct directory${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if git is clean
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  Warning: Git working directory is not clean${NC}"
    git status --short
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Release cancelled.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}🔨 Building packages...${NC}"

# Build Python package
echo -e "${YELLOW}Building Python package...${NC}"
rm -rf dist/smart_commits_ai-$PYTHON_VERSION*
python3 -m build
if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ Python build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python package built successfully${NC}"

# Build NPM package
echo -e "${YELLOW}Building NPM package...${NC}"
cd npm-wrapper
rm -f smart-commits-ai-$NPM_VERSION.tgz
npm pack
if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ NPM build failed${NC}"
    exit 1
fi
cd ..
echo -e "${GREEN}✅ NPM package built successfully${NC}"

echo -e "${BLUE}📦 Package Information:${NC}"
echo -e "  Python wheel: ${GREEN}dist/smart_commits_ai-$PYTHON_VERSION-py3-none-any.whl${NC}"
echo -e "  Python source: ${GREEN}dist/smart_commits_ai-$PYTHON_VERSION.tar.gz${NC}"
echo -e "  NPM package: ${GREEN}npm-wrapper/smart-commits-ai-$NPM_VERSION.tgz${NC}"
echo ""

# Test packages locally
echo -e "${BLUE}🧪 Testing packages locally...${NC}"

# Test Python package
echo -e "${YELLOW}Testing Python package...${NC}"
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from ai_commit_generator.cli import main
    print('✅ Python package imports successfully')
except Exception as e:
    print(f'❌ Python package test failed: {e}')
    sys.exit(1)
"

# Test NPM package
echo -e "${YELLOW}Testing NPM package...${NC}"
cd npm-wrapper
node -e "
try {
    const client = require('./lib/ai-client.js');
    console.log('✅ NPM package loads successfully');
} catch (e) {
    console.log('❌ NPM package test failed:', e.message);
    process.exit(1);
}
"
cd ..

echo -e "${GREEN}✅ All package tests passed${NC}"
echo ""

# Publish confirmation
echo -e "${BLUE}🚀 Ready to publish!${NC}"
echo -e "${YELLOW}This will:${NC}"
echo "  1. Publish Python package to PyPI"
echo "  2. Publish NPM package to npmjs.com"
echo "  3. Create and push git tags"
echo ""

read -p "🚀 Proceed with publishing? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Publishing cancelled.${NC}"
    exit 1
fi

# Check for required tools
echo -e "${BLUE}🔍 Checking required tools...${NC}"

if ! command -v twine &> /dev/null; then
    echo -e "${YELLOW}Installing twine for PyPI publishing...${NC}"
    pip3 install twine
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is required but not installed${NC}"
    exit 1
fi

# Publish Python package to PyPI
echo -e "${BLUE}📤 Publishing Python package to PyPI...${NC}"
echo -e "${YELLOW}Note: You'll need to enter your PyPI credentials${NC}"

twine upload dist/smart_commits_ai-$PYTHON_VERSION*
if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ PyPI publishing failed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python package published to PyPI${NC}"

# Publish NPM package
echo -e "${BLUE}📤 Publishing NPM package...${NC}"
echo -e "${YELLOW}Note: You'll need to be logged in to npm${NC}"

cd npm-wrapper
npm publish smart-commits-ai-$NPM_VERSION.tgz
if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ NPM publishing failed${NC}"
    exit 1
fi
cd ..
echo -e "${GREEN}✅ NPM package published${NC}"

# Create git tags
echo -e "${BLUE}🏷️  Creating git tags...${NC}"

git tag -a "v$PYTHON_VERSION" -m "Release v$PYTHON_VERSION - Architecture compatibility fix"
git tag -a "npm-v$NPM_VERSION" -m "NPM Release v$NPM_VERSION - Improved compatibility"

echo -e "${YELLOW}Pushing tags to remote...${NC}"
git push origin "v$PYTHON_VERSION"
git push origin "npm-v$NPM_VERSION"

echo -e "${GREEN}✅ Git tags created and pushed${NC}"

# Final success message
echo ""
echo -e "${GREEN}🎉 Release completed successfully!${NC}"
echo -e "${BLUE}Published versions:${NC}"
echo -e "  📦 PyPI: ${GREEN}smart-commits-ai $PYTHON_VERSION${NC}"
echo -e "  📦 NPM:  ${GREEN}smart-commits-ai $NPM_VERSION${NC}"
echo ""
echo -e "${BLUE}🔗 Package URLs:${NC}"
echo -e "  PyPI: ${YELLOW}https://pypi.org/project/smart-commits-ai/$PYTHON_VERSION/${NC}"
echo -e "  NPM:  ${YELLOW}https://www.npmjs.com/package/smart-commits-ai/v/$NPM_VERSION${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "  1. Update documentation with new version numbers"
echo "  2. Create GitHub release with changelog"
echo "  3. Announce the release"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
#!/bin/bash

# AI Commit Message Generator - Installation Script
# This script installs the AI-powered Git hook into any repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SOURCE="$SCRIPT_DIR/hooks/prepare-commit-msg"
CONFIG_SOURCE="$SCRIPT_DIR/.commitgen.yml"
ENV_TEMPLATE="$SCRIPT_DIR/.env.example"

# Print banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║           🤖 AI Commit Message Generator                     ║"
    echo "║                                                              ║"
    echo "║     Automatically generate conventional commit messages      ║"
    echo "║              using AI (Groq, OpenRouter, Cohere)            ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}❌ Error: Not in a Git repository${NC}"
        echo -e "${YELLOW}Please run this script from within a Git repository.${NC}"
        exit 1
    fi
    
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    echo -e "${GREEN}✅ Git repository detected: ${BLUE}$repo_root${NC}"
}

# Check dependencies
check_dependencies() {
    echo -e "${BLUE}🔍 Checking dependencies...${NC}"
    
    local missing_deps=()
    
    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi
    
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo -e "${RED}❌ Missing dependencies: ${missing_deps[*]}${NC}"
        echo -e "${YELLOW}Please install the missing dependencies:${NC}"
        
        # Provide installation instructions based on OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo -e "${CYAN}  macOS: brew install ${missing_deps[*]}${NC}"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo -e "${CYAN}  Ubuntu/Debian: sudo apt-get install ${missing_deps[*]}${NC}"
            echo -e "${CYAN}  CentOS/RHEL: sudo yum install ${missing_deps[*]}${NC}"
        fi
        
        exit 1
    fi
    
    echo -e "${GREEN}✅ All dependencies are installed${NC}"
}

# Install the Git hook
install_hook() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    local hooks_dir="$repo_root/.git/hooks"
    local hook_dest="$hooks_dir/prepare-commit-msg"
    
    echo -e "${BLUE}📦 Installing Git hook...${NC}"
    
    # Create hooks directory if it doesn't exist
    mkdir -p "$hooks_dir"
    
    # Check if hook already exists
    if [[ -f "$hook_dest" ]]; then
        echo -e "${YELLOW}⚠️  Git hook already exists${NC}"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Installation cancelled${NC}"
            exit 0
        fi
        
        # Backup existing hook
        cp "$hook_dest" "$hook_dest.backup.$(date +%s)"
        echo -e "${GREEN}✅ Existing hook backed up${NC}"
    fi
    
    # Copy and make executable
    cp "$HOOK_SOURCE" "$hook_dest"
    chmod +x "$hook_dest"
    
    echo -e "${GREEN}✅ Git hook installed successfully${NC}"
}

# Install configuration file
install_config() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    local config_dest="$repo_root/.commitgen.yml"
    
    echo -e "${BLUE}⚙️  Installing configuration file...${NC}"
    
    if [[ -f "$config_dest" ]]; then
        echo -e "${YELLOW}⚠️  Configuration file already exists${NC}"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Skipping configuration file${NC}"
            return
        fi
    fi
    
    cp "$CONFIG_SOURCE" "$config_dest"
    echo -e "${GREEN}✅ Configuration file installed${NC}"
}

# Create .env file
create_env_file() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    local env_dest="$repo_root/.env"
    
    echo -e "${BLUE}🔑 Setting up environment file...${NC}"
    
    if [[ -f "$env_dest" ]]; then
        echo -e "${YELLOW}⚠️  .env file already exists${NC}"
        read -p "Do you want to add AI API configuration to it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Skipping .env setup${NC}"
            return
        fi
    fi
    
    # Add AI API configuration to .env
    cat >> "$env_dest" << 'EOF'

# AI Commit Message Generator Configuration
# Uncomment and set the API key for your preferred provider

# Groq (recommended - fast and free)
# GROQ_API_KEY=your_groq_api_key_here

# OpenRouter (multiple models available)
# OPENROUTER_API_KEY=your_openrouter_api_key_here

# Cohere
# COHERE_API_KEY=your_cohere_api_key_here

# Optional: Override default models
# GROQ_MODEL=llama3-70b-8192
# OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
# COHERE_MODEL=command-r-plus
EOF
    
    echo -e "${GREEN}✅ Environment file configured${NC}"
}

# Add .env to .gitignore
update_gitignore() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    local gitignore="$repo_root/.gitignore"
    
    echo -e "${BLUE}🔒 Updating .gitignore...${NC}"
    
    # Check if .env is already in .gitignore
    if [[ -f "$gitignore" ]] && grep -q "^\.env$" "$gitignore"; then
        echo -e "${GREEN}✅ .env already in .gitignore${NC}"
        return
    fi
    
    # Add .env to .gitignore
    echo "" >> "$gitignore"
    echo "# AI Commit Generator" >> "$gitignore"
    echo ".env" >> "$gitignore"
    echo ".commitgen.log" >> "$gitignore"
    
    echo -e "${GREEN}✅ .gitignore updated${NC}"
}

# Show setup instructions
show_setup_instructions() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                        🎉 Installation Complete!             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo
    echo -e "${BLUE}1. Get an API key from one of these providers:${NC}"
    echo -e "   • ${GREEN}Groq${NC} (recommended): https://console.groq.com/keys"
    echo -e "   • ${GREEN}OpenRouter${NC}: https://openrouter.ai/keys"
    echo -e "   • ${GREEN}Cohere${NC}: https://dashboard.cohere.ai/api-keys"
    echo
    echo -e "${BLUE}2. Add your API key to .env:${NC}"
    echo -e "   ${CYAN}nano .env${NC}"
    echo -e "   ${CYAN}# Uncomment and set: GROQ_API_KEY=your_actual_key_here${NC}"
    echo
    echo -e "${BLUE}3. Test the installation:${NC}"
    echo -e "   ${CYAN}echo 'test' > test.txt${NC}"
    echo -e "   ${CYAN}git add test.txt${NC}"
    echo -e "   ${CYAN}git commit${NC}"
    echo
    echo -e "${BLUE}4. Customize configuration (optional):${NC}"
    echo -e "   ${CYAN}nano .commitgen.yml${NC}"
    echo
    echo -e "${GREEN}🚀 Your commits will now be automatically enhanced with AI!${NC}"
}

# Main installation function
main() {
    print_banner
    
    echo -e "${BLUE}🔧 Starting installation...${NC}"
    echo
    
    check_git_repo
    check_dependencies
    install_hook
    install_config
    create_env_file
    update_gitignore
    
    echo
    show_setup_instructions
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "AI Commit Message Generator - Installation Script"
        echo
        echo "Usage: $0 [options]"
        echo
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --uninstall    Remove the Git hook"
        echo
        echo "This script installs an AI-powered Git hook that automatically"
        echo "generates conventional commit messages using AI APIs."
        exit 0
        ;;
    --uninstall)
        repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
        if [[ -z "$repo_root" ]]; then
            echo -e "${RED}❌ Not in a Git repository${NC}"
            exit 1
        fi
        
        hook_file="$repo_root/.git/hooks/prepare-commit-msg"
        if [[ -f "$hook_file" ]]; then
            rm "$hook_file"
            echo -e "${GREEN}✅ AI commit hook uninstalled${NC}"
        else
            echo -e "${YELLOW}⚠️  Hook not found${NC}"
        fi
        exit 0
        ;;
    "")
        main
        ;;
    *)
        echo -e "${RED}❌ Unknown option: $1${NC}"
        echo "Use --help for usage information"
        exit 1
        ;;
esac

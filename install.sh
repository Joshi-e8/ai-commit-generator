#!/bin/bash
# Universal installation script for Smart Commits AI
# Works on macOS, Linux, and Windows (via Git Bash)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Package information
PACKAGE_NAME="smart-commits-ai"
PACKAGE_VERSION="1.0.4"

print_header() {
    echo -e "${BLUE}"
    echo "🤖 Smart Commits AI - Universal Installer"
    echo "========================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

check_python() {
    print_info "Checking for Python installation..."
    
    local python_cmd=""
    
    # Try different Python commands
    for cmd in python3 python py; do
        if command -v "$cmd" &> /dev/null; then
            local version=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            local major=$(echo $version | cut -d. -f1)
            local minor=$(echo $version | cut -d. -f2)
            
            if [[ $major -eq 3 && $minor -ge 8 ]]; then
                python_cmd="$cmd"
                print_success "Found Python $version: $cmd"
                break
            fi
        fi
    done
    
    if [[ -z "$python_cmd" ]]; then
        print_error "Python 3.8+ not found!"
        echo ""
        echo "Please install Python 3.8 or later:"
        case $(detect_os) in
            "macos")
                echo "  brew install python"
                echo "  or download from: https://python.org"
                ;;
            "linux")
                echo "  sudo apt update && sudo apt install python3 python3-pip"
                echo "  or: sudo yum install python3 python3-pip"
                ;;
            "windows")
                echo "  Download from: https://python.org"
                echo "  or: winget install Python.Python.3"
                ;;
        esac
        exit 1
    fi
    
    echo "$python_cmd"
}

check_pip() {
    local python_cmd="$1"
    print_info "Checking for pip..."
    
    if $python_cmd -m pip --version &> /dev/null; then
        print_success "pip is available"
    else
        print_error "pip not found!"
        echo ""
        echo "Please install pip:"
        echo "  $python_cmd -m ensurepip --upgrade"
        echo "  or download get-pip.py from: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
}

install_package() {
    local python_cmd="$1"
    print_info "Installing $PACKAGE_NAME v$PACKAGE_VERSION..."
    
    if $python_cmd -m pip install "$PACKAGE_NAME==$PACKAGE_VERSION"; then
        print_success "Installation successful!"
    else
        print_error "Installation failed!"
        echo ""
        echo "Try manual installation:"
        echo "  $python_cmd -m pip install --user $PACKAGE_NAME"
        echo "  or: $python_cmd -m pip install --upgrade pip && $python_cmd -m pip install $PACKAGE_NAME"
        exit 1
    fi
}

verify_installation() {
    print_info "Verifying installation..."
    
    if command -v smart-commits-ai &> /dev/null; then
        local version=$(smart-commits-ai --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        print_success "Verification successful: smart-commits-ai v$version"
    else
        print_warning "Command not found in PATH"
        echo ""
        echo "You may need to add Python's bin directory to your PATH:"
        case $(detect_os) in
            "macos"|"linux")
                echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
                echo "  # Add this to your ~/.bashrc or ~/.zshrc"
                ;;
            "windows")
                echo "  Add Python Scripts directory to your PATH"
                echo "  Usually: C:\\Users\\YourName\\AppData\\Local\\Programs\\Python\\Python3X\\Scripts"
                ;;
        esac
        echo ""
        echo "Or run directly with:"
        echo "  python -m ai_commit_generator.cli --help"
    fi
}

setup_project() {
    print_info "Setting up Smart Commits AI in current directory..."
    
    if [[ -d ".git" ]]; then
        print_info "Git repository detected"
        
        # Install Git hook
        if smart-commits-ai install 2>/dev/null; then
            print_success "Git hook installed"
        else
            print_warning "Could not install Git hook automatically"
            echo "Run 'smart-commits-ai install' manually after fixing PATH"
        fi
        
        # Create example .env file
        if [[ ! -f ".env" ]]; then
            cat > .env << EOF
# Add your AI API key here
# Get free key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_key_here

# Alternative providers:
# OPENROUTER_API_KEY=your_openrouter_key_here
# COHERE_API_KEY=your_cohere_key_here
EOF
            print_success "Created .env template"
            print_warning "Please add your API key to .env file"
        fi
        
        # Create example config file
        if [[ ! -f ".commitgen.yml" ]]; then
            smart-commits-ai config --show > .commitgen.yml 2>/dev/null || true
            if [[ -f ".commitgen.yml" ]]; then
                print_success "Created .commitgen.yml configuration"
            fi
        fi
        
    else
        print_warning "Not in a Git repository"
        echo "Navigate to your project directory and run 'smart-commits-ai install'"
    fi
}

print_next_steps() {
    echo ""
    echo -e "${GREEN}🎉 Installation Complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Get an API key:"
    echo "   • Groq (free): https://console.groq.com/keys"
    echo "   • OpenRouter: https://openrouter.ai/keys"
    echo "   • Cohere: https://dashboard.cohere.ai/api-keys"
    echo ""
    echo "2. Add your API key to .env file:"
    echo "   echo 'GROQ_API_KEY=your_key_here' >> .env"
    echo ""
    echo "3. Test the installation:"
    echo "   smart-commits-ai status"
    echo ""
    echo "4. Start using AI-generated commits:"
    echo "   git add ."
    echo "   git commit  # AI will generate the message!"
    echo ""
    echo "For help: smart-commits-ai --help"
}

main() {
    print_header
    
    # Detect OS
    local os=$(detect_os)
    print_info "Detected OS: $os"
    
    # Check Python
    local python_cmd=$(check_python)
    
    # Check pip
    check_pip "$python_cmd"
    
    # Install package
    install_package "$python_cmd"
    
    # Verify installation
    verify_installation
    
    # Setup in current project if it's a Git repo
    setup_project
    
    # Print next steps
    print_next_steps
}

# Run main function
main "$@"

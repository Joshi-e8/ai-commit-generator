#!/usr/bin/env python3
"""Build standalone executables for different platforms."""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build standalone executable."""
    print("🔨 Building standalone executable...")

    # Detect platform
    import platform
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch in ['aarch64', 'arm64']:
        arch = 'arm64'

    executable_name = f"smart-commits-ai-{system}-{arch}"
    if system == "windows":
        executable_name += ".exe"

    # Create the build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", executable_name,
        "--add-data", "src/ai_commit_generator:ai_commit_generator",
        "--add-data", ".commitgen.yml:.",
        "--hidden-import", "ai_commit_generator.cli",
        "--hidden-import", "ai_commit_generator.core",
        "--hidden-import", "ai_commit_generator.config",
        "--hidden-import", "ai_commit_generator.api_clients",
        "--hidden-import", "ai_commit_generator.git_hook",
        "--hidden-import", "yaml",
        "--hidden-import", "requests",
        "--hidden-import", "click",
        "--hidden-import", "rich",
        "--clean",
        "--noconfirm",
        "src/ai_commit_generator/cli.py"
    ]

    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        print(f"📁 Location: dist/{executable_name}")
        print(f"🎯 Platform: {system}-{arch}")

        # Test the executable
        test_cmd = [f"dist/{executable_name}", "--version"]
        try:
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Executable test passed: {result.stdout.strip()}")
            else:
                print(f"⚠️ Executable test failed: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Could not test executable: {e}")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def main():
    """Main build process."""
    print("🚀 Building Smart Commits AI Standalone Executable")
    print("=" * 50)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build Complete!")
        print("\nNext steps:")
        print("1. Test the executable: ./dist/smart-commits-ai --version")
        print("2. Distribute to your team")
        print("3. No Python installation required!")
    else:
        print("\n❌ Build failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

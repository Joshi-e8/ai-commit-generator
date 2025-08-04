#!/usr/bin/env python3
"""
Architecture Fix Script for Smart Commits AI
Automatically fixes charset-normalizer architecture issues on Apple Silicon
"""

import subprocess
import sys
import platform
import os

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def is_apple_silicon():
    """Check if running on Apple Silicon"""
    return platform.system() == "Darwin" and platform.machine() == "arm64"

def fix_architecture_issue():
    """Fix the charset-normalizer architecture issue"""
    print("🔧 Smart Commits AI - Architecture Fix")
    print("=" * 50)
    
    if not is_apple_silicon():
        print("✅ No architecture fix needed (not Apple Silicon)")
        return True
    
    print("🍎 Apple Silicon detected - checking for architecture issues...")
    
    # Test if charset-normalizer works
    try:
        import charset_normalizer
        print("✅ charset-normalizer is working correctly")
        return True
    except ImportError as e:
        if "incompatible architecture" in str(e) or "dlopen" in str(e):
            print("🚨 Architecture compatibility issue detected")
            print("🔄 Fixing charset-normalizer and requests packages...")
            
            # Uninstall problematic packages
            print("   Uninstalling incompatible packages...")
            success, stdout, stderr = run_command("pip3 uninstall -y charset-normalizer requests")
            if not success:
                print(f"❌ Failed to uninstall packages: {stderr}")
                return False
            
            # Reinstall with correct architecture
            print("   Reinstalling with correct architecture...")
            success, stdout, stderr = run_command("pip3 install --no-cache-dir --force-reinstall charset-normalizer requests")
            if not success:
                print(f"❌ Failed to reinstall packages: {stderr}")
                return False
            
            print("✅ Architecture fix completed successfully!")
            return True
        else:
            print(f"❌ Different import error: {e}")
            return False

def main():
    """Main function"""
    if fix_architecture_issue():
        print("\n🎉 Smart Commits AI is ready to use!")
        print("Run 'smart-commits-ai --help' to get started")
        sys.exit(0)
    else:
        print("\n❌ Architecture fix failed")
        print("Please run manually:")
        print("pip3 uninstall -y charset-normalizer requests")
        print("pip3 install --no-cache-dir --force-reinstall charset-normalizer requests")
        sys.exit(1)

if __name__ == "__main__":
    main()
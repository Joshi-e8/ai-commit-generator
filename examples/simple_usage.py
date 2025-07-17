#!/usr/bin/env python3
"""Simple usage example for AI Commit Generator.

This example shows how to use the AI Commit Generator programmatically
without installing it as a Git hook.
"""

import os
import tempfile
from pathlib import Path

from ai_commit_generator.api_clients import APIError, create_client
from ai_commit_generator.config import Config, ConfigError
from ai_commit_generator.core import CommitGenerator


def example_basic_usage():
    """Example of basic usage with default configuration."""
    print("🤖 AI Commit Generator - Basic Usage Example")
    print("=" * 50)

    try:
        # Create a commit generator with default config
        generator = CommitGenerator()

        # Check if we're in a Git repository
        print(f"📁 Repository: {generator.config.repo_root}")
        print(f"⚙️  Provider: {generator.config.provider}")
        print(f"🤖 Model: {generator.config.model}")

        # Check if API key is configured
        try:
            api_key = generator.config.api_key
            print(f"🔑 API Key: {api_key[:8]}... (configured)")
        except ConfigError as e:
            print(f"❌ {e}")
            print("\n💡 To fix this:")
            print(f"   echo 'GROQ_API_KEY=your_key_here' >> .env")
            return

        # Generate a commit message for current staged changes
        print("\n🔍 Checking for staged changes...")
        message = generator.generate_commit_message()

        if message:
            print(f"✅ Generated message: {message}")
        else:
            print("⚠️  No staged changes found or merge commit detected")
            print("\n💡 To test this:")
            print("   echo 'test change' > test.txt")
            print("   git add test.txt")
            print("   python examples/simple_usage.py")

    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_config():
    """Example of using custom configuration."""
    print("\n🔧 Custom Configuration Example")
    print("=" * 50)

    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = Path(temp_dir)
        git_dir = repo_dir / ".git"
        git_dir.mkdir()

        # Create custom config file
        config_file = repo_dir / ".commitgen.yml"
        config_content = """
api:
  provider: groq

commit:
  max_chars: 50
  types: [feat, fix, docs, refactor]

debug:
  enabled: true
"""
        config_file.write_text(config_content.strip())

        # Create config with custom settings
        config = Config(repo_root=repo_dir)

        print(f"📁 Temp repo: {config.repo_root}")
        print(f"⚙️  Provider: {config.provider}")
        print(f"📏 Max chars: {config.max_chars}")
        print(f"🏷️  Types: {config.commit_types}")
        print(f"🐛 Debug: {config.debug_enabled}")


def example_api_client():
    """Example of using API clients directly."""
    print("\n🌐 API Client Example")
    print("=" * 50)

    # Check if API key is available
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("💡 Set it with: export GROQ_API_KEY=your_key_here")
        return

    try:
        # Create API client directly
        client = create_client(
            provider="groq", api_key=api_key, model="llama3-70b-8192"
        )

        # Example prompt
        prompt = """Generate a conventional commit message under 72 characters for the following git diff.

Use one of these types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

If applicable, include a scope in parentheses after the type.

Format: type(scope): description

Be concise and descriptive. Focus on WHAT changed, not HOW.

Git diff:
+++ b/src/auth.py
@@ -10,6 +10,12 @@ def login(username, password):
     if not username or not password:
         raise ValueError("Username and password required")
     
+    # Add rate limiting
+    if check_rate_limit(username):
+        raise RateLimitError("Too many login attempts")
+    
     user = authenticate(username, password)
     if user:
         return generate_token(user)

Respond with ONLY the commit message, no explanations or additional text."""

        print("🤖 Generating commit message...")
        message = client.generate_commit_message(prompt)
        print(f"✅ Generated: {message}")

    except APIError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main():
    """Run all examples."""
    example_basic_usage()
    example_custom_config()
    example_api_client()

    print("\n" + "=" * 50)
    print("🎉 Examples completed!")
    print("\n📚 Next steps:")
    print("   1. Install the Git hook: smart-commits-ai install")
    print("   2. Configure your API key in .env")
    print("   3. Start committing with AI-generated messages!")


if __name__ == "__main__":
    main()

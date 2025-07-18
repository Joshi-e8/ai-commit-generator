#!/usr/bin/env python3
"""
Security Fixes for Smart Commits AI
Implements secure versions of vulnerable functions.
"""

import os
import re
import stat
import logging
import subprocess
import functools
from pathlib import Path
from typing import Optional, Dict, Any, Pattern
import yaml

class SecurityError(Exception):
    """Base exception for security-related errors."""
    pass

class InputValidator:
    """Secure input validation utilities."""
    
    # Secure regex patterns
    COMMIT_MESSAGE_PATTERN: Pattern = re.compile(r'^[a-zA-Z0-9\s\(\)\:\-\.\,\!]{5,250}$')
    SAFE_PATH_PATTERN: Pattern = re.compile(r'^[a-zA-Z0-9\-_\./]+$')
    API_KEY_PATTERN: Pattern = re.compile(r'^[a-zA-Z0-9\-_]{20,}$')
    
    @staticmethod
    def validate_commit_message(message: str) -> bool:
        """Validate commit message format and content."""
        if not message or not isinstance(message, str):
            return False
        
        # Check length
        if len(message) < 5 or len(message) > 250:
            return False
        
        # Check pattern
        if not InputValidator.COMMIT_MESSAGE_PATTERN.match(message):
            return False
        
        # Check for suspicious content
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'data:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
            r'\x00',  # Null bytes
            r'\.\./',  # Path traversal
            r'\\\\',   # UNC paths
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return False
        
        return True
    
    @staticmethod
    def validate_file_path(base_path: Path, file_path: Path) -> Path:
        """Validate file path is within base directory and safe."""
        try:
            # Resolve paths
            resolved_base = base_path.resolve()
            resolved_file = (base_path / file_path).resolve()
            
            # Ensure file is within base directory
            resolved_file.relative_to(resolved_base)
            
            # Check for suspicious path components
            path_str = str(resolved_file)
            if any(component in path_str for component in ['..', '~', '$']):
                raise SecurityError(f"Unsafe path component in: {file_path}")
            
            return resolved_file
            
        except ValueError:
            raise SecurityError(f"Path traversal attempt: {file_path}")
        except Exception as e:
            raise SecurityError(f"Invalid file path: {file_path} - {e}")
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format."""
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Check length and pattern
        if len(api_key) < 20 or len(api_key) > 200:
            return False
        
        return bool(InputValidator.API_KEY_PATTERN.match(api_key))
    
    @staticmethod
    def sanitize_repo_path(path: str) -> Path:
        """Sanitize and validate repository path."""
        if not path or not isinstance(path, str):
            raise SecurityError("Invalid repository path")
        
        # Convert to Path and resolve
        try:
            clean_path = Path(path).resolve()
        except Exception as e:
            raise SecurityError(f"Invalid path: {e}")
        
        # Check if path exists
        if not clean_path.exists():
            raise SecurityError("Repository path does not exist")
        
        # Check if it's a Git repository
        if not (clean_path / ".git").exists():
            raise SecurityError("Not a Git repository")
        
        # Additional security checks
        path_str = str(clean_path)
        if any(suspicious in path_str for suspicious in ['/proc/', '/sys/', '/dev/']):
            raise SecurityError("Access to system directories not allowed")
        
        return clean_path

class SecureLogger:
    """Secure logging utilities that mask sensitive data."""
    
    SENSITIVE_PATTERNS = [
        (re.compile(r'(api[_-]?key["\']?\s*[:=]\s*["\']?)([a-zA-Z0-9\-_]{20,})(["\']?)', re.IGNORECASE), r'\1[REDACTED]\3'),
        (re.compile(r'(token["\']?\s*[:=]\s*["\']?)([a-zA-Z0-9\-_]{20,})(["\']?)', re.IGNORECASE), r'\1[REDACTED]\3'),
        (re.compile(r'(password["\']?\s*[:=]\s*["\']?)([^\s"\']{8,})(["\']?)', re.IGNORECASE), r'\1[REDACTED]\3'),
        (re.compile(r'(secret["\']?\s*[:=]\s*["\']?)([^\s"\']{8,})(["\']?)', re.IGNORECASE), r'\1[REDACTED]\3'),
        (re.compile(r'Bearer\s+([a-zA-Z0-9\-_]{20,})', re.IGNORECASE), r'Bearer [REDACTED]'),
    ]
    
    @staticmethod
    def sanitize_message(message: str) -> str:
        """Remove sensitive data from log messages."""
        if not isinstance(message, str):
            return str(message)
        
        sanitized = message
        for pattern, replacement in SecureLogger.SENSITIVE_PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)
        
        return sanitized
    
    @staticmethod
    def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
        """Safely mask sensitive data for display."""
        if not data or not isinstance(data, str):
            return "[INVALID]"
        
        if len(data) <= visible_chars:
            return "*" * len(data)
        
        return data[:visible_chars] + "*" * (len(data) - visible_chars)

class SensitiveDataFilter(logging.Filter):
    """Logging filter to remove sensitive data."""
    
    def filter(self, record):
        """Filter sensitive data from log records."""
        if hasattr(record, 'msg'):
            record.msg = SecureLogger.sanitize_message(str(record.msg))
        
        if hasattr(record, 'args') and record.args:
            record.args = tuple(
                SecureLogger.sanitize_message(str(arg)) if isinstance(arg, str) else arg
                for arg in record.args
            )
        
        return True

def secure_subprocess_run(cmd: list, cwd: Optional[Path] = None, timeout: int = 30, **kwargs) -> subprocess.CompletedProcess:
    """Secure wrapper for subprocess.run with validation and timeouts."""
    
    # Validate command
    if not cmd or not isinstance(cmd, list):
        raise SecurityError("Invalid command")
    
    # Validate all command components are strings
    if not all(isinstance(arg, str) for arg in cmd):
        raise SecurityError("All command arguments must be strings")
    
    # Validate working directory
    if cwd is not None:
        if not isinstance(cwd, Path):
            cwd = Path(cwd)
        cwd = cwd.resolve()
        if not cwd.exists():
            raise SecurityError(f"Working directory does not exist: {cwd}")
    
    # Set secure defaults
    secure_kwargs = {
        'capture_output': True,
        'text': True,
        'check': True,
        'timeout': timeout,
        'shell': False,  # Never use shell
        **kwargs
    }
    
    try:
        return subprocess.run(cmd, cwd=cwd, **secure_kwargs)
    except subprocess.TimeoutExpired:
        raise SecurityError(f"Command timed out after {timeout} seconds")
    except subprocess.CalledProcessError as e:
        raise SecurityError(f"Command failed: {e}")

def secure_file_write(file_path: Path, content: str, mode: int = 0o600) -> None:
    """Securely write content to file with proper permissions."""
    
    # Validate file path
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    
    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file with secure permissions
    try:
        # Create file with restrictive permissions
        file_path.touch(mode=mode)
        
        # Write content
        file_path.write_text(content, encoding='utf-8')
        
        # Ensure permissions are set correctly
        file_path.chmod(mode)
        
    except Exception as e:
        raise SecurityError(f"Failed to write file securely: {e}")

def secure_yaml_load(file_path: Path) -> Dict[str, Any]:
    """Securely load YAML file with validation."""
    
    if not file_path.exists():
        return {}
    
    # Validate file size (prevent DoS)
    file_size = file_path.stat().st_size
    if file_size > 1024 * 1024:  # 1MB limit
        raise SecurityError("Configuration file too large")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Use safe_load to prevent code execution
            content = yaml.safe_load(f)
            
        # Validate content type
        if content is None:
            return {}
        
        if not isinstance(content, dict):
            raise SecurityError("Configuration must be a dictionary")
        
        return content
        
    except yaml.YAMLError as e:
        raise SecurityError(f"Invalid YAML syntax: {e}")
    except Exception as e:
        raise SecurityError(f"Failed to load configuration: {e}")

def secure_error_handler(func):
    """Decorator for secure error handling that doesn't leak information."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SecurityError:
            # Re-raise security errors as-is
            raise
        except Exception as e:
            # Log full error for debugging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            
            # Raise generic error to user
            raise SecurityError("An internal error occurred. Check logs for details.")
    
    return wrapper

class SecureConfig:
    """Secure configuration management."""
    
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = self._find_and_validate_repo_root(repo_root)
        self.config_file = self._validate_config_path()
        self.env_file = self._validate_env_path()
        
        # Set up secure logging
        self._setup_secure_logging()
        
        # Load configuration
        self.config = self._load_secure_config()
    
    def _find_and_validate_repo_root(self, repo_root: Optional[Path]) -> Path:
        """Find and validate repository root."""
        if repo_root is None:
            # Find repo root by traversing up
            current = Path.cwd()
            while current != current.parent:
                if (current / ".git").exists():
                    repo_root = current
                    break
                current = current.parent
            
            if repo_root is None:
                raise SecurityError("Not in a Git repository")
        
        return InputValidator.sanitize_repo_path(str(repo_root))
    
    def _validate_config_path(self) -> Path:
        """Validate configuration file path."""
        return InputValidator.validate_file_path(self.repo_root, Path(".commitgen.yml"))
    
    def _validate_env_path(self) -> Path:
        """Validate environment file path."""
        return InputValidator.validate_file_path(self.repo_root, Path(".env"))
    
    def _setup_secure_logging(self) -> None:
        """Set up secure logging configuration."""
        logger = logging.getLogger()
        
        # Add sensitive data filter to all handlers
        for handler in logger.handlers:
            handler.addFilter(SensitiveDataFilter())
    
    def _load_secure_config(self) -> Dict[str, Any]:
        """Load configuration securely."""
        # Load base configuration
        config = self._get_default_config()
        
        # Load user configuration if exists
        if self.config_file.exists():
            user_config = secure_yaml_load(self.config_file)
            config = self._merge_config(config, user_config)
        
        # Load environment variables
        self._load_secure_env()
        
        # Validate final configuration
        self._validate_config(config)
        
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get secure default configuration."""
        return {
            "api": {
                "provider": "groq",
                "timeout": 30,
                "max_retries": 3,
                "verify_ssl": True,
            },
            "commit": {
                "max_chars": 72,
                "types": ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"],
            },
            "processing": {
                "max_diff_size": 4000,  # Reduced for security
                "exclude_patterns": [
                    "*.key", "*.pem", "*.p12", "*.env*", "secrets/*",
                    "*.log", "*.tmp", "node_modules/**", ".git/**"
                ],
            },
            "security": {
                "validate_inputs": True,
                "sanitize_logs": True,
                "max_log_size": 10485760,  # 10MB
            },
            "debug": {
                "enabled": False,
                "save_requests": False,
            }
        }
    
    def _merge_config(self, base: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Securely merge user configuration with base configuration."""
        # Deep merge dictionaries
        result = base.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _load_secure_env(self) -> None:
        """Load environment variables securely."""
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            # Validate environment variable names
                            if re.match(r'^[A-Z_][A-Z0-9_]*$', key):
                                os.environ[key] = value
            except Exception as e:
                raise SecurityError(f"Failed to load environment file: {e}")
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration values."""
        # Validate API configuration
        if "api" in config:
            api_config = config["api"]
            
            # Validate provider
            valid_providers = ["groq", "openrouter", "cohere"]
            if api_config.get("provider") not in valid_providers:
                raise SecurityError(f"Invalid API provider. Must be one of: {valid_providers}")
            
            # Validate timeout
            timeout = api_config.get("timeout", 30)
            if not isinstance(timeout, int) or timeout <= 0 or timeout > 300:
                raise SecurityError("API timeout must be between 1 and 300 seconds")
        
        # Validate commit configuration
        if "commit" in config:
            commit_config = config["commit"]
            
            # Validate max_chars
            max_chars = commit_config.get("max_chars", 72)
            if not isinstance(max_chars, int) or max_chars < 10 or max_chars > 500:
                raise SecurityError("max_chars must be between 10 and 500")
        
        # Validate processing configuration
        if "processing" in config:
            proc_config = config["processing"]
            
            # Validate max_diff_size
            max_diff = proc_config.get("max_diff_size", 4000)
            if not isinstance(max_diff, int) or max_diff < 100 or max_diff > 50000:
                raise SecurityError("max_diff_size must be between 100 and 50000")

# Example usage and testing
if __name__ == "__main__":
    # Test input validation
    validator = InputValidator()
    
    # Test commit message validation
    valid_messages = [
        "feat: add new feature",
        "fix(auth): resolve login issue",
        "docs: update README",
    ]
    
    invalid_messages = [
        "<script>alert('xss')</script>",
        "'; DROP TABLE commits; --",
        "A" * 1000,  # Too long
        "",  # Empty
        "test\x00null",  # Null byte
    ]
    
    print("Testing commit message validation:")
    for msg in valid_messages:
        print(f"✅ '{msg}': {validator.validate_commit_message(msg)}")
    
    for msg in invalid_messages:
        print(f"❌ '{msg[:50]}...': {validator.validate_commit_message(msg)}")
    
    # Test sensitive data masking
    logger = SecureLogger()
    sensitive_data = "GROQ_API_KEY=sk-1234567890abcdef"
    print(f"\nOriginal: {sensitive_data}")
    print(f"Sanitized: {logger.sanitize_message(sensitive_data)}")
    print(f"Masked: {logger.mask_sensitive_data('sk-1234567890abcdef')}")

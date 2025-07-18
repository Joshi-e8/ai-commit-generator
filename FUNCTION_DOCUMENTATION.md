# 📚 Smart Commits AI - Detailed Function Documentation

## 📋 Table of Contents

1. [Core Module (`core.py`)](#core-module-corepy)
2. [API Clients Module (`api_clients.py`)](#api-clients-module-api_clientspy)
3. [Configuration Module (`config.py`)](#configuration-module-configpy)
4. [CLI Module (`cli.py`)](#cli-module-clipy)
5. [Git Hook Module (`git_hook.py`)](#git-hook-module-git_hookpy)
6. [Security Considerations](#security-considerations)
7. [Error Handling](#error-handling)

---

## 🔧 Core Module (`core.py`)

### Class: `CommitGenerator`

Main orchestrator for AI-powered commit message generation.

#### `__init__(self, config: Optional[Config] = None)`
**Purpose**: Initialize the commit generator with configuration.
**Parameters**:
- `config` (Optional[Config]): Configuration object. If None, creates from current directory.
**Security Notes**: 
- Validates configuration on initialization
- Sets up secure logging configuration
**Example**:
```python
generator = CommitGenerator()
# or with custom config
config = Config(repo_root=Path("/path/to/repo"))
generator = CommitGenerator(config)
```

#### `_setup_logging(self) -> None`
**Purpose**: Configure logging based on configuration settings.
**Security Notes**:
- ⚠️ **VULNERABILITY**: May log sensitive information in debug mode
- **Mitigation**: Implement log sanitization
**Implementation**:
```python
def _setup_logging(self) -> None:
    if self.config.debug_enabled:
        # Add sensitive data filter
        handler = logging.FileHandler(self.config.log_file)
        handler.addFilter(SensitiveDataFilter())
        logging.basicConfig(handlers=[handler])
```

#### `generate_commit_message(self, commit_msg_file: Optional[str] = None) -> str`
**Purpose**: Main entry point for generating commit messages.
**Parameters**:
- `commit_msg_file` (Optional[str]): Path to commit message file for Git hook usage
**Returns**: Generated commit message string
**Security Notes**:
- ⚠️ **VULNERABILITY**: File path not validated
- **Mitigation**: Validate file path before writing
**Flow**:
1. Validate configuration
2. Check for merge commits
3. Get staged Git diff
4. Process and filter diff
5. Generate message with AI
6. Write to file if specified

#### `_is_merge_commit(self) -> bool`
**Purpose**: Detect if current commit is a merge commit.
**Returns**: True if merge commit detected
**Security Notes**: ✅ **SECURE** - Only reads Git metadata
**Implementation**:
```python
def _is_merge_commit(self) -> bool:
    try:
        merge_head = self.config.repo_root / ".git" / "MERGE_HEAD"
        return merge_head.exists()
    except Exception as e:
        logger.warning(f"Could not check for merge commit: {e}")
        return False
```

#### `_get_staged_diff(self) -> str`
**Purpose**: Retrieve Git diff of staged changes.
**Returns**: Git diff output as string
**Security Notes**:
- ⚠️ **VULNERABILITY**: Command injection via repo_root
- **Mitigation**: Validate and sanitize repo_root path
**Secure Implementation**:
```python
def _get_staged_diff(self) -> str:
    # Validate repo_root
    repo_root = Path(self.config.repo_root).resolve()
    if not repo_root.exists() or not (repo_root / ".git").exists():
        raise GitError("Invalid Git repository")
    
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            timeout=30  # Add timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise GitError("Git command timed out")
```

#### `_process_diff(self, diff: str) -> str`
**Purpose**: Process and filter diff content for AI consumption.
**Parameters**:
- `diff` (str): Raw Git diff output
**Returns**: Processed diff content
**Security Notes**: ✅ **SECURE** - String processing only
**Features**:
- Filters excluded file patterns
- Truncates large diffs
- Removes sensitive file content

#### `_filter_excluded_files(self, diff: str) -> str`
**Purpose**: Remove files matching exclude patterns from diff.
**Parameters**:
- `diff` (str): Git diff content
**Returns**: Filtered diff content
**Security Notes**: ✅ **SECURE** - Pattern matching only
**Patterns**: Configurable via `exclude_patterns` setting

#### `_should_exclude_file(self, filename: str) -> bool`
**Purpose**: Check if file should be excluded based on patterns.
**Parameters**:
- `filename` (str): File path to check
**Returns**: True if file should be excluded
**Security Notes**: ✅ **SECURE** - Uses fnmatch for pattern matching

#### `_generate_with_ai(self, diff: str) -> str`
**Purpose**: Generate commit message using AI API.
**Parameters**:
- `diff` (str): Processed Git diff content
**Returns**: Generated commit message
**Security Notes**:
- ⚠️ **VULNERABILITY**: Sends code diff to external API
- **Mitigation**: Ensure diff filtering removes sensitive content
**Flow**:
1. Build AI prompt
2. Create API client
3. Retry logic with exponential backoff
4. Validate generated message
5. Return fallback if all attempts fail

#### `_build_prompt(self, diff: str) -> str`
**Purpose**: Construct prompt for AI generation.
**Parameters**:
- `diff` (str): Git diff content
**Returns**: Formatted prompt string
**Security Notes**: ✅ **SECURE** - Template formatting only

#### `_clean_message(self, message: str) -> str`
**Purpose**: Clean and normalize AI-generated message.
**Parameters**:
- `message` (str): Raw AI response
**Returns**: Cleaned commit message
**Security Notes**:
- ⚠️ **VULNERABILITY**: Limited input validation
- **Mitigation**: Add comprehensive sanitization
**Secure Implementation**:
```python
def _clean_message(self, message: str) -> str:
    # Remove potentially dangerous characters
    message = re.sub(r'[^\w\s\(\)\:\-\.\,]', '', message)
    message = message.strip()
    message = message.split("\n")[0]  # First line only
    message = message.strip("\"'")
    
    # Validate length
    if len(message) > self.config.max_chars:
        message = message[:self.config.max_chars].rstrip()
    
    return message
```

#### `_validate_message(self, message: str) -> bool`
**Purpose**: Validate generated commit message format.
**Parameters**:
- `message` (str): Commit message to validate
**Returns**: True if message is valid
**Security Notes**: ✅ **SECURE** - Regex validation only
**Validation Rules**:
- Minimum 5 characters
- Matches conventional commit format
- Uses configured commit types

---

## 🌐 API Clients Module (`api_clients.py`)

### Abstract Class: `APIClient`

Base class for all AI provider clients.

#### `__init__(self, api_key: str, model: str, max_retries: int = 3, retry_delay: int = 1)`
**Purpose**: Initialize API client with common configuration.
**Parameters**:
- `api_key` (str): API key for authentication
- `model` (str): Model name to use
- `max_retries` (int): Maximum retry attempts
- `retry_delay` (int): Delay between retries
**Security Notes**:
- ⚠️ **VULNERABILITY**: API key stored in memory
- **Mitigation**: Clear sensitive data after use

#### `_make_request(self, url: str, headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]`
**Purpose**: Make HTTP request with error handling and retries.
**Parameters**:
- `url` (str): API endpoint URL
- `headers` (Dict): Request headers
- `data` (Dict): Request payload
**Returns**: Response JSON data
**Security Notes**:
- ⚠️ **VULNERABILITY**: No request timeout
- ⚠️ **VULNERABILITY**: SSL verification not explicitly enabled
- **Mitigation**: Add timeout and SSL verification
**Secure Implementation**:
```python
def _make_request(self, url: str, headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = self.session.post(
            url, 
            headers=headers, 
            json=data, 
            timeout=30,  # Add timeout
            verify=True  # Ensure SSL verification
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.SSLError:
        raise APIError("SSL verification failed")
    except requests.exceptions.Timeout:
        raise APIError("Request timed out")
    # ... rest of error handling
```

### Class: `GroqClient(APIClient)`

Groq API client implementation.

#### `generate_commit_message(self, prompt: str) -> str`
**Purpose**: Generate commit message using Groq API.
**Parameters**:
- `prompt` (str): AI prompt
**Returns**: Generated message
**Security Notes**: ✅ **SECURE** - Uses HTTPS and bearer token auth
**API Endpoint**: `https://api.groq.com/openai/v1/chat/completions`

### Class: `OpenRouterClient(APIClient)`

OpenRouter API client implementation.

#### `generate_commit_message(self, prompt: str) -> str`
**Purpose**: Generate commit message using OpenRouter API.
**Parameters**:
- `prompt` (str): AI prompt
**Returns**: Generated message
**Security Notes**: ✅ **SECURE** - Uses HTTPS and bearer token auth
**API Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
**Headers**: Includes referer and title for tracking

### Class: `CohereClient(APIClient)`

Cohere API client implementation.

#### `generate_commit_message(self, prompt: str) -> str`
**Purpose**: Generate commit message using Cohere API.
**Parameters**:
- `prompt` (str): AI prompt
**Returns**: Generated message
**Security Notes**: ✅ **SECURE** - Uses HTTPS and bearer token auth
**API Endpoint**: `https://api.cohere.ai/v1/chat`

### Function: `create_client(provider: str, api_key: str, model: str, **kwargs) -> APIClient`
**Purpose**: Factory function to create appropriate API client.
**Parameters**:
- `provider` (str): Provider name (groq, openrouter, cohere)
- `api_key` (str): API key
- `model` (str): Model name
- `**kwargs`: Additional client arguments
**Returns**: Configured API client instance
**Security Notes**: ✅ **SECURE** - Validates provider before creation

---

## ⚙️ Configuration Module (`config.py`)

### Class: `Config`

Configuration manager for the application.

#### `__init__(self, repo_root: Optional[Path] = None)`
**Purpose**: Initialize configuration from files and environment.
**Parameters**:
- `repo_root` (Optional[Path]): Git repository root. Auto-detected if None.
**Security Notes**:
- ⚠️ **VULNERABILITY**: Path traversal in config file loading
- **Mitigation**: Validate file paths

#### `_find_repo_root(self) -> Path`
**Purpose**: Locate Git repository root directory.
**Returns**: Path to repository root
**Security Notes**: ✅ **SECURE** - Only traverses upward in directory tree

#### `_load_config(self) -> Dict[str, Any]`
**Purpose**: Load configuration from YAML file.
**Returns**: Configuration dictionary
**Security Notes**:
- ⚠️ **VULNERABILITY**: YAML deserialization without validation
- **Mitigation**: Use safe_load and validate content
**Secure Implementation**:
```python
def _load_config(self) -> Dict[str, Any]:
    config = self.DEFAULT_CONFIG.copy()
    
    if self.config_file.exists():
        # Validate file path
        if not self._is_safe_path(self.config_file):
            raise ConfigError("Unsafe configuration file path")
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            
            # Validate configuration structure
            self._validate_config_structure(user_config)
            config = self._merge_config(config, user_config)
        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML: {e}")
    
    return config
```

#### `_load_env(self) -> None`
**Purpose**: Load environment variables from .env file.
**Security Notes**:
- ⚠️ **VULNERABILITY**: .env file path not validated
- **Mitigation**: Validate file path before loading

#### `api_key` (Property)
**Purpose**: Get API key for current provider.
**Returns**: API key string
**Security Notes**:
- ⚠️ **VULNERABILITY**: API key exposed in error messages
- **Mitigation**: Mask API key in logs and errors

#### `validate(self) -> None`
**Purpose**: Validate configuration values.
**Security Notes**: ✅ **SECURE** - Comprehensive validation
**Validations**:
- Provider is supported
- API key is configured
- Numeric values are positive
- File paths are safe

---

## 💻 CLI Module (`cli.py`)

### Decorator: `handle_errors(func)`
**Purpose**: Centralized error handling for CLI commands.
**Security Notes**:
- ⚠️ **VULNERABILITY**: Exposes stack traces in debug mode
- **Mitigation**: Sanitize error output

### Command: `install(force: bool, config: bool)`
**Purpose**: Install Git hook and configuration files.
**Parameters**:
- `force` (bool): Overwrite existing files
- `config` (bool): Install configuration templates
**Security Notes**:
- ⚠️ **VULNERABILITY**: File overwrite without validation
- **Mitigation**: Validate target paths

### Command: `generate(output: Optional[str], dry_run: bool)`
**Purpose**: Generate commit message for staged changes.
**Parameters**:
- `output` (Optional[str]): Output file path
- `dry_run` (bool): Don't write to file
**Security Notes**:
- ⚠️ **VULNERABILITY**: Output path not validated
- **Mitigation**: Validate and sanitize output path

### Command: `config(show: bool, validate: bool)`
**Purpose**: Display and validate configuration.
**Parameters**:
- `show` (bool): Display current configuration
- `validate` (bool): Validate configuration
**Security Notes**:
- ⚠️ **VULNERABILITY**: API key partially exposed
- **Mitigation**: Properly mask sensitive data

---

## 🔗 Git Hook Module (`git_hook.py`)

### Class: `GitHookManager`

Manages Git hook installation and lifecycle.

#### `install_hook(self, force: bool = False) -> bool`
**Purpose**: Install prepare-commit-msg Git hook.
**Parameters**:
- `force` (bool): Overwrite existing hook
**Returns**: True if installed successfully
**Security Notes**:
- ⚠️ **VULNERABILITY**: Insecure file permissions
- **Mitigation**: Set restrictive permissions (0o750)

#### `_generate_hook_content(self) -> str`
**Purpose**: Generate Git hook script content.
**Returns**: Hook script as string
**Security Notes**:
- ⚠️ **VULNERABILITY**: Command injection in Python path
- **Mitigation**: Validate Python executable path

#### `_get_python_command(self) -> str`
**Purpose**: Determine appropriate Python command.
**Returns**: Python executable path
**Security Notes**:
- ⚠️ **VULNERABILITY**: Uses subprocess.run with shell
- **Mitigation**: Avoid shell execution

---

## 🛡️ Security Considerations

### Input Validation
- Validate all file paths
- Sanitize user inputs
- Validate configuration values
- Check API responses

### Error Handling
- Mask sensitive data in logs
- Provide generic error messages
- Log detailed errors securely
- Implement proper exception handling

### File Operations
- Set restrictive permissions
- Validate file paths
- Prevent path traversal
- Use secure temporary files

### Network Security
- Enable SSL verification
- Set request timeouts
- Implement rate limiting
- Validate API responses

---

**Security Status**: 🔴 **REQUIRES IMMEDIATE ATTENTION**
**Priority**: Implement security fixes before production use

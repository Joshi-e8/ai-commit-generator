# Smart Commits AI - GitHub Action Usage

## 🚀 Quick Start

Add this to your workflow file (`.github/workflows/ai-commits.yml`):

```yaml
name: AI Commit Messages
on: [push, pull_request]

jobs:
  ai-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate AI Commit Message
        id: smart-commits
        uses: joshi-e8/smart-commits-ai-action@v1
        with:
          api_key: ${{ secrets.GROQ_API_KEY }}
          provider: 'groq'
      
      - name: Display Generated Message
        run: |
          echo "Generated: ${{ steps.smart-commits.outputs.commit_message }}"
          echo "Success: ${{ steps.smart-commits.outputs.success }}"
```

## 📋 Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `api_key` | API key for AI provider | ✅ Yes | - |
| `provider` | AI provider (groq, openrouter, cohere) | ❌ No | `groq` |
| `model` | AI model to use | ❌ No | `llama3-70b-8192` |
| `max_chars` | Maximum characters for commit message | ❌ No | `250` |
| `commit_types` | Comma-separated list of commit types | ❌ No | `feat,fix,docs,style,refactor,perf,test,build,ci,chore,revert,remove,config` |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| `commit_message` | Generated commit message |
| `success` | Whether message generation was successful (`true`/`false`) |

## 🔧 Advanced Usage

### Custom Configuration

```yaml
- name: Generate AI Commit Message
  uses: joshi-e8/smart-commits-ai-action@v1
  with:
    api_key: ${{ secrets.GROQ_API_KEY }}
    provider: 'groq'
    model: 'llama3-70b-8192'
    max_chars: '200'
    commit_types: 'feat,fix,docs,refactor,test'
```

### Auto-commit Workflow

```yaml
name: Auto AI Commits
on:
  push:
    branches: [ feature/* ]

jobs:
  auto-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Generate AI Commit Message
        id: smart-commits
        uses: joshi-e8/smart-commits-ai-action@v1
        with:
          api_key: ${{ secrets.GROQ_API_KEY }}
      
      - name: Auto-commit with AI message
        if: steps.smart-commits.outputs.success == 'true'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "${{ steps.smart-commits.outputs.commit_message }}" || exit 0
          git push
```

### Multiple Providers

```yaml
strategy:
  matrix:
    provider: [groq, openrouter, cohere]
    
steps:
  - name: Generate with ${{ matrix.provider }}
    uses: joshi-e8/smart-commits-ai-action@v1
    with:
      api_key: ${{ secrets[format('{0}_API_KEY', matrix.provider | upper)] }}
      provider: ${{ matrix.provider }}
```

## 🔑 Setup API Keys

1. Get API key from your chosen provider:
   - **Groq**: https://console.groq.com/keys
   - **OpenRouter**: https://openrouter.ai/keys
   - **Cohere**: https://dashboard.cohere.ai/api-keys

2. Add to GitHub Secrets:
   - Go to repository Settings → Secrets and variables → Actions
   - Add secret: `GROQ_API_KEY` (or `OPENROUTER_API_KEY`, `COHERE_API_KEY`)

## 🎯 Use Cases

### Code Review Enhancement
```yaml
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  enhance-pr:
    steps:
      - name: Generate commit messages for PR
        uses: joshi-e8/smart-commits-ai-action@v1
        # ... rest of configuration
```

### Release Automation
```yaml
on:
  push:
    tags: ['v*']

jobs:
  release:
    steps:
      - name: Generate release commit message
        uses: joshi-e8/smart-commits-ai-action@v1
        # ... rest of configuration
```

### Development Workflow
```yaml
on:
  workflow_dispatch:
    inputs:
      custom_prompt:
        description: 'Custom prompt for AI'
        required: false

jobs:
  dev-commits:
    steps:
      - name: Generate development commit
        uses: joshi-e8/smart-commits-ai-action@v1
        # ... rest of configuration
```

## 🚨 Troubleshooting

### Common Issues

**"No staged changes found"**
- Ensure files are staged before running the action
- Add `git add .` step before the action

**"API key not working"**
- Verify the secret name matches the provider
- Check API key validity at provider's website

**"Generation failed"**
- Check API rate limits
- Verify model availability for your provider

### Debug Mode

```yaml
- name: Generate AI Commit Message (Debug)
  uses: joshi-e8/smart-commits-ai-action@v1
  with:
    api_key: ${{ secrets.GROQ_API_KEY }}
  env:
    ACTIONS_STEP_DEBUG: true
```

## 📚 Examples Repository

See more examples at: https://github.com/joshi-e8/smart-commits-ai-examples

---

**Transform your CI/CD with AI-powered commit messages!** 🚀

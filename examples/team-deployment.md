# Team Deployment Guide

This guide shows how to deploy the AI commit generator across your development team.

## Deployment Options

### Option 1: Shared Network Drive

**Best for:** Small teams with shared file systems

```bash
# 1. Copy tool to shared location
cp -r ai-commit-generator /shared/tools/

# 2. Team members install from shared location
cd /path/to/their/project
/shared/tools/ai-commit-generator/install_hook.sh

# 3. Each developer adds their own API key
echo "GROQ_API_KEY=their_individual_key" >> .env
```

### Option 2: Internal Git Repository

**Best for:** Teams using Git for tool distribution

```bash
# 1. Create internal repository
git init ai-commit-generator
cd ai-commit-generator
# ... copy all files here ...
git add .
git commit -m "feat: add AI commit message generator"
git remote add origin https://github.com/your-org/ai-commit-generator.git
git push -u origin main

# 2. Team members clone and install
git clone https://github.com/your-org/ai-commit-generator.git
cd their-project
../ai-commit-generator/install_hook.sh
```

### Option 3: Package Distribution

**Best for:** Larger organizations with package management

```bash
# 1. Create distributable package
tar -czf ai-commit-generator-v1.0.tar.gz ai-commit-generator/

# 2. Host on internal server
# Upload to https://tools.company.com/ai-commit-generator-v1.0.tar.gz

# 3. Team members download and install
curl -sSL https://tools.company.com/ai-commit-generator-v1.0.tar.gz | tar -xz
cd their-project
./ai-commit-generator/install_hook.sh
```

## Team Configuration

### Shared API Keys (Not Recommended)

```bash
# Create shared .env template
cat > .env.template << 'EOF'
# Shared team API key (rotate regularly)
GROQ_API_KEY=gsk_shared_team_key_here
EOF

# Team members copy template
cp .env.template .env
```

### Individual API Keys (Recommended)

```bash
# Each developer gets their own key from https://console.groq.com/keys
# Add to their personal .env file
GROQ_API_KEY=gsk_individual_developer_key
```

### Project-Specific Configuration

Create a team-wide `.commitgen.yml`:

```yaml
# Team configuration
api:
  provider: groq

commit:
  max_chars: 72
  types: [feat, fix, docs, style, refactor, perf, test, build, ci, chore]
  
  # Project-specific scopes
  scopes:
    - frontend
    - backend
    - api
    - ui
    - auth
    - db
    - config
    - tests

prompt:
  template: |
    You are a senior developer on our team working on a React/Node.js application.
    
    Generate a conventional commit message for:
    {{diff}}
    
    Requirements:
    - Use format: type(scope): description
    - Maximum {{max_chars}} characters
    - Be specific about what changed
    - Focus on business value when possible
```

## Rollout Strategy

### Phase 1: Pilot (Week 1)
- Select 2-3 experienced developers
- Install on non-critical projects
- Gather feedback and refine configuration
- Document any issues and solutions

### Phase 2: Team Rollout (Week 2)
- Install for entire development team
- Conduct 15-minute training session
- Monitor adoption and provide support
- Adjust configuration based on feedback

### Phase 3: Organization (Week 3+)
- Roll out to all engineering teams
- Create internal documentation wiki
- Establish support process and FAQ
- Track metrics and success stories

## Training Session Outline (15 minutes)

### Introduction (3 minutes)
- What is the AI commit generator?
- Benefits: consistency, time-saving, professional standards
- Demo: before/after commit messages

### Installation (5 minutes)
- Live demo of installation process
- Show API key setup
- Test with sample commit

### Usage (5 minutes)
- Normal Git workflow (no changes needed)
- How to override AI messages when needed
- Configuration customization

### Q&A and Troubleshooting (2 minutes)
- Common issues and solutions
- Where to get help
- Feedback collection

## Support Process

### Internal Support Channels
- **Slack**: #dev-tools or #ai-commit-help
- **Email**: devtools@company.com
- **Wiki**: Internal documentation page
- **Office Hours**: Weekly 30-minute support session

### Escalation Process
1. **Self-service**: Check documentation and examples
2. **Peer support**: Ask in team Slack channel
3. **Tool maintainer**: Contact designated team member
4. **External support**: Groq/OpenRouter/Cohere documentation

### Common Support Issues

**Installation Problems**
- Missing dependencies (jq, curl)
- Permission issues with Git hooks
- Network/firewall blocking API calls

**Configuration Issues**
- API key format or permissions
- YAML syntax errors in .commitgen.yml
- Provider-specific model names

**Usage Questions**
- How to customize prompts
- When to override AI messages
- Project-specific scope configuration

## Success Metrics

Track these metrics to measure deployment success:

### Adoption Metrics
- Number of developers with tool installed
- Percentage of commits using AI-generated messages
- Time from installation to first successful commit

### Quality Metrics
- Conventional commit compliance rate
- Manual review of commit message quality
- Reduction in "fix", "update", "changes" type messages

### Developer Experience
- Time saved per commit (survey)
- Developer satisfaction scores
- Support ticket volume and resolution time

### Code Review Impact
- Faster code review process
- Better understanding of changes from commit history
- Reduced back-and-forth on commit message formatting

## Maintenance

### Regular Tasks
- **Monthly**: Review API usage and costs
- **Quarterly**: Rotate shared API keys (if used)
- **Bi-annually**: Update tool to latest version
- **Annually**: Review and update team configuration

### Monitoring
- API rate limits and usage patterns
- Error rates and common failure modes
- Developer feedback and feature requests
- Security considerations and key management

## Cost Considerations

### Groq (Recommended)
- **Free tier**: Very generous limits
- **Cost**: $0 for most teams
- **Scaling**: Upgrade to paid if needed

### OpenRouter
- **Pay-per-use**: ~$0.01-0.10 per commit
- **Monthly cost**: $5-50 for active team
- **Benefits**: Access to premium models

### Cohere
- **Free tier**: Good for small teams
- **Enterprise**: Contact for pricing
- **Benefits**: SOC2 compliance, dedicated support

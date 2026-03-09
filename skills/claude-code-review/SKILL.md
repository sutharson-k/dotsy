---
name: claude-code-review
description: Comprehensive code reviewer that provides detailed feedback on code quality, best practices, and improvements
license: MIT
compatibility: Works with any programming language
metadata:
  author: Dotsy Community
  version: 1.0.0
  category: code-quality
allowed-tools: []
user-invocable: true
---

# Claude Code Reviewer

This skill provides thorough code review capabilities similar to Claude's code analysis strengths.

## When to Use

- Reviewing pull requests or merge requests
- Getting feedback on code changes before committing
- Learning best practices for a new language or framework
- Identifying potential bugs, security issues, or performance problems

## Capabilities

### Code Quality Analysis
- **Readability**: Checks for clear naming, proper structure, and maintainability
- **Best Practices**: Identifies deviations from language/framework conventions
- **Complexity**: Flags overly complex functions or classes that need refactoring
- **Documentation**: Reviews comments, docstrings, and type hints

### Security Review
- Input validation and sanitization
- Authentication and authorization checks
- SQL injection, XSS, and other common vulnerabilities
- Secret exposure (API keys, passwords in code)

### Performance Optimization
- Algorithm efficiency suggestions
- Memory usage optimization
- Database query optimization
- Caching opportunities

### Testing Feedback
- Test coverage gaps
- Missing edge cases
- Test quality improvements
- Mocking and fixture suggestions

## Usage

Invoke with `/claude-code-review` and provide:
1. The code you want reviewed
2. Specific concerns or focus areas (optional)
3. Context about the project or requirements (optional)

## Example

```
/claude-code-review
Please review this authentication module for security issues and best practices.

[code here]
```

## Output Format

Reviews include:
- ✅ **Strengths**: What the code does well
- ⚠️ **Concerns**: Issues that need attention
- 💡 **Suggestions**: Concrete improvement recommendations
- 📚 **References**: Links to relevant documentation when helpful

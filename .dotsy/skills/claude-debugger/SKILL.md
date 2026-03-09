---
name: claude-debugger
description: Expert debugging assistant that systematically diagnoses and fixes bugs with detailed explanations
license: MIT
compatibility: Works with any programming language and debugging scenario
metadata:
  author: Dotsy Community
  version: 1.0.0
  category: debugging
allowed-tools: []
user-invocable: true
---

# Claude Debugger

This skill provides systematic debugging expertise, combining Claude's analytical reasoning with proven debugging methodologies.

## When to Use

- Tracking down elusive bugs
- Understanding error messages and stack traces
- Fixing race conditions and concurrency issues
- Debugging production incidents
- Learning debugging techniques for a new language
- Performance troubleshooting

## Capabilities

### Error Analysis
- **Stack Trace Interpretation**: Decodes error messages and traces
- **Log Analysis**: Identifies patterns in application logs
- **Error Classification**: Categorizes bugs (logic, runtime, compile-time, etc.)
- **Root Cause Analysis**: Traces symptoms back to source

### Systematic Debugging
- **Hypothesis Generation**: Proposes possible causes
- **Test Case Creation**: Builds minimal reproductions
- **Binary Search Debugging**: Isolates problematic code sections
- **State Inspection**: Examines variable values and program state

### Common Bug Categories

#### Logic Errors
- Off-by-one errors
- Incorrect conditionals
- Wrong algorithm implementation
- Edge case handling

#### Runtime Errors
- Null/undefined references
- Type mismatches
- Resource leaks
- Memory issues

#### Concurrency Issues
- Race conditions
- Deadlocks
- Thread safety
- Async/await problems

#### Integration Bugs
- API contract violations
- Database transaction issues
- Network timeouts
- Authentication failures

### Debugging Tools Guidance
- **Debugger Usage**: Breakpoints, watch expressions, step-through
- **Logging Strategy**: What, when, and how to log
- **Profiling**: CPU, memory, I/O analysis
- **Monitoring**: APM tools, metrics, alerts

## Usage

Invoke with `/claude-debugger` and provide:
1. Error message or symptom description
2. Relevant code snippets
3. Steps to reproduce (if known)
4. What you've already tried

## Example

```
/claude-debugger
Getting a NullPointerException in my user authentication flow.
The error happens when users log in with special characters in their email.

Stack trace:
[stack trace here]

Code:
[code here]

I've tried sanitizing the input but the error persists.
```

## Output Format

Debugging sessions include:
- 🔍 **Problem Analysis**: Understanding of the issue
- 🎯 **Likely Causes**: Ranked hypotheses
- 🧪 **Reproduction Steps**: How to consistently trigger the bug
- 🔧 **Fix Recommendations**: Concrete solutions with code
- 📖 **Explanation**: Why the bug occurred and how the fix works
- 🛡️ **Prevention**: How to avoid similar bugs in the future

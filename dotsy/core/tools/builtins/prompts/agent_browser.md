# Agent Browser Tool

Use the `agent_browser` tool to automate browser actions using agent-browser CLI. This tool enables AI-driven web automation for testing, scraping, and interaction.

## Installation

First, install agent-browser CLI:

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
```

## When to Use

Use this tool when you need to:
- Test web applications you're building
- Navigate and interact with websites
- Take screenshots of web pages
- Extract content from web pages
- Automate repetitive web tasks
- Debug production UI issues

## Parameters

- `action` (required): Action to perform
  - `open` - Navigate to URL
  - `snapshot` - Get page accessibility tree
  - `click` - Click an element
  - `fill` - Fill input field
  - `type` - Type text (with keyboard events)
  - `screenshot` - Take screenshot
  - `scroll` - Scroll page/element
  - `hover` - Hover over element
  - `wait` - Wait for condition
- `url`: URL to navigate to (for 'open')
- `element_ref`: Element reference like '@e1', '@e2' (for click/fill/type)
- `text`: Text to input (for fill/type)
- `screenshot_path`: Path to save screenshot
- `wait_for`: Wait for element/text/URL
- `provider`: Browser provider (local, browserbase, browser-use, kernel, ios)

## Examples

### Open a Website
```
Open https://example.com
```

### Get Page Snapshot
```
Get page snapshot as JSON
```

### Click Element
```
Click element @e5
```

### Fill Form
```
Fill @e3 with "test@example.com"
```

### Take Screenshot
```
Take screenshot and save to page.png
```

### Complete Workflow
```
1. Open https://github.com/login
2. Fill @username with "myuser"
3. Fill @password with "mypass"
4. Click @submit
5. Take screenshot
```

## Output Format

### Success Response
```json
{
  "success": true,
  "action": "open",
  "output": "Navigated to https://example.com",
  "snapshot": { ... },  // For snapshot action
  "screenshot_path": "page.png"  // For screenshot action
}
```

### Error Response
```json
{
  "success": false,
  "action": "click",
  "error": "Element @e5 not found"
}
```

## Configuration

Add to `~/.dotsy/config.toml`:

```toml
[tools.agent_browser]
permission = "ask"  # Always ask before browser actions
headless = true     # Run in headless mode
timeout_seconds = 30

# Domain allowlist for security
domain_allowlist = [
    "localhost",
    "127.0.0.1",
    "*.yourdomain.com",
    "github.com"
]

# Browser provider
provider = "local"  # local, browserbase, browser-use, kernel, ios

# Profile path for persistent sessions
profile_path = "~/.dotsy/browser-profile"
```

## Security Features

### Domain Allowlist
Prevents navigation to unauthorized domains:
```toml
domain_allowlist = ["localhost", "*.yourcompany.com"]
```

### Permission System
Always ask before executing browser actions:
```toml
permission = "ask"
```

### Session Management
Clear session data on exit or use persistent profiles:
```toml
profile_path = "~/.dotsy/browser-profile"  # Persistent
# Or omit for temporary sessions
```

## Cloud Browser Providers

### Browserbase
```toml
provider = "browserbase"
```
Set env vars:
```bash
export BROWSERBASE_API_KEY="your-key"
export BROWSERBASE_PROJECT_ID="your-project"
```

### Browser Use
```toml
provider = "browser-use"
```
Set env var:
```bash
export BROWSER_USE_API_KEY="your-key"
```

### iOS Simulator
```toml
provider = "ios"
```
Requires Appium:
```bash
npm install -g appium
appium driver install xcuitest
```

## Element References

agent-browser uses ref-based selection for reliable element targeting:

1. Get snapshot first: `agent-browser snapshot --json`
2. Parse response to find element refs (e.g., `@e1`, `@e2`)
3. Use refs in actions: `click @e5`

Example snapshot structure:
```json
{
  "nodes": [
    { "ref": "@e1", "role": "button", "name": "Submit" },
    { "ref": "@e2", "role": "textbox", "name": "Email" }
  ]
}
```

## Annotated Screenshots

Take screenshots with numbered element labels:
```bash
agent-browser screenshot --annotated
```

This helps AI correlate text-based refs with visual elements.

## Troubleshooting

### "agent-browser not found"
```bash
npm install -g agent-browser
```

### "Chromium not downloaded"
```bash
agent-browser install
```

### "Element not found"
- Get fresh snapshot before interacting
- Check if page fully loaded (use `wait` action)
- Verify element ref is current (refs change on re-render)

### "Domain not in allowlist"
Add domain to config:
```toml
domain_allowlist = ["example.com"]
```

## Comparison with Alternatives

| Feature | agent-browser | Puppeteer MCP | Playwright |
|---------|--------------|---------------|------------|
| Speed | ⚡⚡⚡ (Rust) | ⚡⚡ (Node) | ⚡⚡ (Node) |
| Ref Selection | ✅ Yes | ❌ No | ❌ No |
| Annotated Screenshots | ✅ Yes | ❌ No | ⚠️ Manual |
| Multi-Provider | ✅ 5+ | ❌ Local only | ⚠️ Limited |
| iOS Support | ✅ Yes | ❌ No | ⚠️ Complex |

## Best Practices

1. **Always get snapshot first** before interacting
2. **Use wait actions** for dynamic content
3. **Enable headless mode** for automation
4. **Set domain allowlist** for security
5. **Clear sessions** after sensitive operations
6. **Use annotated screenshots** for debugging

## Resources

- Documentation: https://agent-browser.dev
- GitHub: https://github.com/vercel-labs/agent-browser
- NPM: https://www.npmjs.com/package/agent-browser

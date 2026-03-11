# Browser Automation Tool (browser-use)

Use the `agent_browser` tool to automate browser actions using the browser-use library. This tool enables AI-driven web automation for testing, scraping, and interaction.

## Installation

First, install browser-use:

```bash
pip install browser-use
```

browser-use uses Playwright under the hood and will automatically download Chromium on first run.

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
  - `snapshot` - Get page content
  - `click` - Click an element
  - `fill` - Fill input field
  - `type` - Type text (with keyboard events)
  - `screenshot` - Take screenshot
  - `scroll` - Scroll page/element
  - `hover` - Hover over element
  - `wait` - Wait for condition
- `url`: URL to navigate to (for 'open')
- `element_ref`: CSS selector or XPath (for click/fill/type)
- `text`: Text to input (for fill/type)
- `screenshot_path`: Path to save screenshot
- `wait_for`: Wait for element/text/URL

## Examples

### Open a Website
```
Open https://example.com
```

### Get Page Content
```
Get page snapshot
```

### Click Element
```
Click element with selector 'button.submit'
```

### Fill Form
```
Fill input[name="email"] with "test@example.com"
```

### Take Screenshot
```
Take screenshot and save to page.png
```

### Complete Workflow
```
1. Open https://github.com/login
2. Fill input[name="login"] with "myuser"
3. Fill input[name="password"] with "mypass"
4. Click button[type="submit"]
5. Take screenshot
```

## Output Format

### Success Response
```json
{
  "success": true,
  "action": "open",
  "output": "Navigated to https://example.com",
  "snapshot": { "content": "...", "title": "..." },
  "screenshot_path": "page.png"
}
```

### Error Response
```json
{
  "success": false,
  "action": "click",
  "error": "Element not found: button.submit"
}
```

## Configuration

Add to `~/.dotsy/config.toml`:

```toml
[tools.agent_browser]
permission = "ask"  # Always ask before browser actions
headless = true     # Run in headless mode
timeout_seconds = 60

# Domain allowlist for security
domain_allowlist = [
    "localhost",
    "127.0.0.1",
    "*.yourdomain.com",
    "github.com"
]
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

## Element Selectors

browser-use supports standard web selectors:

- **CSS Selectors**: `button.submit`, `input[name="email"]`, `#login-form`
- **XPath**: `//button[text()='Submit']`
- **Text content**: `text=Login`

Example workflow:
```
1. Get snapshot to see page structure
2. Identify element selectors
3. Use selectors in actions: click 'button.submit'
```

## Best Practices

1. **Navigate first** - Always use `open` action before interacting
2. **Use specific selectors** - Prefer unique IDs or specific CSS selectors
3. **Wait for dynamic content** - Use `wait` action for lazy-loaded elements
4. **Enable headless mode** - For automated/background tasks
5. **Set domain allowlist** - For security in production
6. **Handle errors gracefully** - Check `success` field in responses

## Troubleshooting

### "browser-use not installed"
```bash
pip install browser-use
```

### "Element not found"
- Verify selector is correct (use browser dev tools)
- Check if page fully loaded (use `wait` action)
- Get fresh snapshot to see current page structure

### "Domain not in allowlist"
Add domain to config:
```toml
domain_allowlist = ["example.com"]
```

### Browser doesn't close
The tool automatically cleans up browser resources after each action.

## Comparison with Alternatives

| Feature | browser-use | Puppeteer MCP | Playwright |
|---------|-------------|---------------|------------|
| Language | Python | Node.js | Node.js/Python |
| LLM Integration | ✅ Built-in | ⚠️ Manual | ⚠️ Manual |
| Auto-wait | ✅ Yes | ✅ Yes | ✅ Yes |
| Multi-provider | ✅ Yes | ❌ Local only | ⚠️ Limited |
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## Resources

- Documentation: https://browser-use.com
- GitHub: https://github.com/browser-use/browser-use
- PyPI: https://pypi.org/project/browser-use/

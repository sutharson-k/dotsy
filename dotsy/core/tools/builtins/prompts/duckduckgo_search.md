# DuckDuckGo Search Tool

Use the `duckduckgo_search` tool to search the web using DuckDuckGo's privacy-focused search API. This tool provides access to real-time web information, news, and articles without requiring an API key.

## When to Use

Use this tool when you need to:
- Find current information not in your training data
- Search for recent news, events, or developments
- Look up documentation, tutorials, or technical information
- Verify facts or find multiple sources on a topic
- Search for specific websites or resources

## Parameters

- `query` (required): The search query string
- `max_results` (optional, default: 10): Number of results to return (1-50)

## Examples

### Basic Search
```
Search for Python 3.12 release features
```

### Search with Result Limit
```
Find recent AI developments (max 5 results)
```

### Specific Topic Search
```
TypeScript 5.0 breaking changes
```

## Output Format

The tool returns a list of search results, each containing:
- `title`: Page title
- `snippet`: Brief description/excerpt
- `url`: Link to the page

## Example Response

```json
{
  "results": [
    {
      "title": "Python 3.12.0 Release",
      "snippet": "Python 3.12.0 is the latest stable release...",
      "url": "https://www.python.org/downloads/"
    }
  ],
  "query": "Python 3.12 features",
  "result_count": 1
}
```

## Advantages

✅ **No API Key Required** - Completely free to use
✅ **Privacy-Focused** - DuckDuckGo doesn't track users
✅ **Unlimited Usage** - No rate limits or quotas
✅ **Open Source** - Uses open web standards
✅ **Real-time Results** - Access to current web content

## Limitations

- Results are from DuckDuckGo's index (may differ from Google)
- HTML parsing may occasionally miss results
- Best for general web searches (not academic/specialized)

## Configuration

No configuration needed! The tool works out of the box.

Optional settings in `~/.dotsy/config.toml`:

```toml
[tools.duckduckgo_search]
max_results = 10  # Default number of results
timeout_seconds = 10  # Request timeout
```

## Comparison with Other Search Tools

| Feature | DuckDuckGo | BochaAI | Google |
|---------|------------|---------|--------|
| API Key | ❌ None | ✅ Required | ✅ Required |
| Cost | Free | Paid | Paid tier |
| Privacy | ✅ High | Medium | Low |
| Rate Limits | None | Yes | Yes |
| Open Source | ✅ Yes | ❌ No | ❌ No |

# Bocha Search Tool

Use the `bocha_search` tool to search the web using BochaAI's search API. This tool provides access to real-time web information, news, and articles.

## When to Use

- Finding current information not in your training data
- Researching recent events or news
- Looking up documentation or API references
- Fact-checking information
- Finding sources and references

## Arguments

- `query` (required): The search query string
- `max_results` (optional): Maximum number of results to return (default: 10)
- `search_type` (optional): Type of search - "web" (default) or "news"

## Examples

### Basic Web Search

```
Search for "Python async best practices 2026"
```

### News Search

```
Search for "AI developments" with search_type="news"
```

### Limited Results

```
Search for "Rust programming" with max_results=5
```

## Configuration

To use this tool, you need a BochaAI API key:

1. Get an API key from BochaAI (check their documentation for the correct API endpoint)
2. Set the environment variable: `BOCHAAI_API_KEY=your-api-key`
3. Or add to your config.toml:

```toml
[tools.bocha_search]
permission = "always"
api_key_env_var = "BOCHAAI_API_KEY"
api_base_url = "https://api.bochaai.com/v1"  # Verify this URL with BochaAI docs
default_max_results = 10
```

**Note:** The API endpoint URL may vary depending on BochaAI's API structure. Common endpoints tried:
- `/web-search`
- `/v1/web-search`
- `/search`
- `/v1/search`

Check BochaAI's official documentation for the correct endpoint.

## Response Format

The tool returns:
- `query`: The original search query
- `results`: List of search results with title, url, snippet, and date
- `result_count`: Number of results returned
- `was_truncated`: Whether results were limited by max_results
- `search_type`: The type of search performed

## Error Handling

The tool will raise errors for:
- Missing API key
- Network timeouts
- Invalid API responses
- Rate limiting

## Tips

- Be specific in your search queries for better results
- Use quotes for exact phrase matching
- Use search_type="news" for recent news articles
- Limit max_results for faster responses when you only need a few results

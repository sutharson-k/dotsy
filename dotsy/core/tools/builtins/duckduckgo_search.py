"""DuckDuckGo Search integration for Dotsy.

This module provides web search capabilities using DuckDuckGo's search API.
DuckDuckGo is a privacy-focused search engine that doesn't track users.

Features:
- No API key required
- Free and unlimited usage
- Privacy-focused (no tracking)
- Returns web search results with titles, snippets, and URLs
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError

from dotsy.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolError,
)
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData
from dotsy.core.types import ToolCallEvent, ToolResultEvent, ToolStreamEvent


class DuckDuckGoSearchConfig(BaseToolConfig):
    """Configuration for DuckDuckGo search tool."""

    max_results: int = 10
    timeout_seconds: int = 10


class DuckDuckGoSearchState(BaseToolState):
    """State for DuckDuckGo search tool."""


class DuckDuckGoSearchArgs(BaseModel):
    """Arguments for DuckDuckGo search."""

    query: str = Field(
        description="The search query to look up on the web.",
    )
    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results to return (1-50).",
    )


class DuckDuckGoSearchResult(BaseModel):
    """Result from DuckDuckGo search."""

    results: list[dict[str, str]]
    query: str
    result_count: int


class DuckDuckGoSearch(
    BaseTool[
        DuckDuckGoSearchArgs,
        DuckDuckGoSearchResult,
        DuckDuckGoSearchConfig,
        DuckDuckGoSearchState,
    ],
    ToolUIData[DuckDuckGoSearchArgs, DuckDuckGoSearchResult],
):
    """Search the web using DuckDuckGo's search API.

    Privacy-focused web search with no API key required.
    Returns relevant web pages, articles, and information.
    """

    TOOL_NAME = "duckduckgo_search"
    TOOL_DESCRIPTION = (
        "Search the web using DuckDuckGo's privacy-focused search API. "
        "Returns relevant web pages, articles, and information. "
        "No API key required - free and unlimited usage."
    )

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        return ToolCallDisplay(
            summary=f"Searching DuckDuckGo for: {parameters.get('query', 'N/A')}",
        )

    async def invoke(
        self,
        ctx: InvokeContext | None = None,
        **parameters: Any,
    ) -> AsyncGenerator[ToolStreamEvent | DuckDuckGoSearchResult, None]:
        try:
            args = DuckDuckGoSearchArgs.model_validate(parameters)
        except ValidationError as e:
            raise ToolError(f"Invalid search parameters: {e}") from e

        tool_call_id = ctx.tool_call_id if ctx else "duckduckgo-001"

        yield ToolStreamEvent(
            tool_name=self.TOOL_NAME,
            tool_call_id=tool_call_id,
            message=f"Searching DuckDuckGo for: {args.query}",
        )

        try:
            results = await self._search_duckduckgo(
                query=args.query,
                max_results=args.max_results,
            )

            yield ToolStreamEvent(
                tool_name=self.TOOL_NAME,
                tool_call_id=tool_call_id,
                message="Search results retrieved",
            )

        except httpx.TimeoutException as e:
            raise ToolError(f"DuckDuckGo search timed out: {e}") from e
        except httpx.RequestError as e:
            raise ToolError(f"DuckDuckGo search request failed: {e}") from e
        except Exception as e:
            raise ToolError(f"DuckDuckGo search failed: {e}") from e

    async def _search_duckduckgo(
        self,
        query: str,
        max_results: int = 10,
        timeout: int = 10,
    ) -> DuckDuckGoSearchResult:
        """Search DuckDuckGo using their HTML search results.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            timeout: Request timeout in seconds
            
        Returns:
            DuckDuckGoSearchResult with search results
        """
        # Use DuckDuckGo's HTML search interface
        base_url = "https://html.duckduckgo.com/html/"
        params = {
            "q": query,
            "kl": "wt-wt",  # All regions
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        }

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                base_url,
                params=params,
                headers=headers,
                follow_redirects=True,
            )
            response.raise_for_status()

            # Parse HTML results
            results = self._parse_html_results(response.text, max_results)

        return DuckDuckGoSearchResult(
            results=results,
            query=query,
            result_count=len(results),
        )

    def _parse_html_results(
        self, 
        html_content: str, 
        max_results: int
    ) -> list[dict[str, str]]:
        """Parse DuckDuckGo HTML search results.
        
        Args:
            html_content: Raw HTML from DuckDuckGo
            max_results: Maximum number of results to extract
            
        Returns:
            List of result dictionaries with title, snippet, url
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        # DuckDuckGo HTML results use result__a class for links
        for result in soup.select('div.result__body')[:max_results]:
            try:
                # Extract title
                title_elem = result.select_one('h2.result__title a.result__a')
                title = title_elem.get_text(strip=True) if title_elem else "No title"

                # Extract URL
                link = title_elem.get('href') if title_elem else ""
                # DuckDuckGo uses redirect URLs, extract the actual URL
                if link and str(link).startswith('/l/?kh='):
                    # Parse the actual URL from the redirect
                    actual_url = str(link).split('udd=')[-1] if 'udd=' in link else link
                else:
                    actual_url = link

                # Extract snippet
                snippet_elem = result.select_one('a.result__snippet')
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                if title and snippet:
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": actual_url,
                    })
            except Exception:
                # Skip malformed results
                continue

        return results

    @classmethod
    def get_call_display(cls, event: ToolCallEvent) -> ToolCallDisplay:
        if not isinstance(event.args, DuckDuckGoSearchArgs):
            return ToolCallDisplay(summary="Searching web...")
        return ToolCallDisplay(
            summary=f"Searching DuckDuckGo for: {event.args.query}",
        )

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        if not isinstance(event.result, DuckDuckGoSearchResult):
            return ToolResultDisplay(success=True, message="Search complete")
        return ToolResultDisplay(
            success=True,
            message=f"Found {event.result.result_count} results from DuckDuckGo",
        )

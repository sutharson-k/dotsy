from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any, ClassVar

import httpx
from pydantic import BaseModel, Field

from dotsy.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolError,
    ToolPermission,
)
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData
from dotsy.core.types import ToolStreamEvent


class BochaSearchConfig(BaseToolConfig):
    permission: ToolPermission = ToolPermission.ALWAYS

    api_key_env_var: str = Field(
        default="BOCHAAI_API_KEY",
        description="Environment variable containing the BochaAI API key.",
    )
    api_base_url: str = Field(
        default="https://api.bochaai.com/v1",
        description="Base URL for the BochaAI API.",
    )
    default_max_results: int = Field(
        default=10, description="Default maximum number of search results to return."
    )
    default_timeout: int = Field(
        default=30, description="Default timeout for the search request in seconds."
    )


class BochaSearchState(BaseToolState):
    search_history: list[str] = Field(default_factory=list)


class BochaSearchArgs(BaseModel):
    query: str = Field(..., description="The search query string.")
    max_results: int | None = Field(
        default=None,
        description="Override the default maximum number of results (default: 10).",
    )
    search_type: str = Field(
        default="web",
        description="Type of search: 'web' for general web search, 'news' for news search.",
    )


class BochaSearchResult(BaseModel):
    query: str
    results: list[dict[str, Any]]
    result_count: int
    was_truncated: bool = Field(
        description="True if results were cut short by max_results."
    )
    search_type: str


class BochaSearch(
    BaseTool[BochaSearchArgs, BochaSearchResult, BochaSearchConfig, BochaSearchState],
    ToolUIData[BochaSearchArgs, BochaSearchResult],
):
    """Search the web using BochaAI's search API. Returns relevant web pages, articles, and information."""

    description: ClassVar[str] = (
        "Search the web using BochaAI's search API. Returns relevant web pages, articles, and information."
    )

    async def run(
        self, args: BochaSearchArgs, ctx: InvokeContext | None = None
    ) -> AsyncGenerator[ToolStreamEvent | BochaSearchResult, None]:
        import os

        api_key = os.getenv(self.config.api_key_env_var)

        if not api_key:
            raise ToolError(
                f"BochaAI API key not found. Set the {self.config.api_key_env_var} environment variable."
            )

        max_results = args.max_results or self.config.default_max_results

        yield ToolStreamEvent(
            tool_name=self.get_name(), message=f"Searching BochaAI for: {args.query}"
        )

        try:
            results = await self._search_bocha(
                query=args.query,
                api_key=api_key,
                api_base=self.config.api_base_url,
                max_results=max_results,
                search_type=args.search_type,
                timeout=self.config.default_timeout,
            )

            # Update state
            self.state.search_history.append(args.query)

            yield results

        except httpx.TimeoutException as e:
            raise ToolError(f"BochaAI search timed out: {e}") from e
        except httpx.RequestError as e:
            raise ToolError(f"BochaAI search request failed: {e}") from e
        except Exception as e:
            raise ToolError(f"BochaAI search failed: {e}") from e

    async def _search_bocha(
        self,
        query: str,
        api_key: str,
        api_base: str,
        max_results: int,
        search_type: str,
        timeout: int,
    ) -> BochaSearchResult:
        # Try different endpoint patterns
        endpoints_to_try = [
            f"{api_base}/web-search",
            f"{api_base}/v1/web-search",
            f"{api_base}/search",
            f"{api_base}/v1/search",
        ]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {"query": query, "count": max_results}

        last_error = None
        async with httpx.AsyncClient() as client:
            for endpoint in endpoints_to_try:
                try:
                    response = await client.post(
                        endpoint, headers=headers, json=payload, timeout=timeout
                    )

                    if response.status_code == 404:
                        last_error = f"Endpoint not found: {endpoint}"
                        continue

                    response.raise_for_status()
                    data = response.json()
                    break

                except httpx.HTTPStatusError as e:
                    last_error = f"HTTP error {e.response.status_code}: {e}"
                    if e.response.status_code == 404:
                        continue
                    raise
                except Exception as e:
                    last_error = str(e)
                    continue
            else:
                # All endpoints failed with 404
                raise ToolError(
                    f"BochaAI API endpoints not found. Tried: {', '.join(endpoints_to_try)}. "
                    f"Last error: {last_error}. "
                    "Please verify your API key and base URL."
                )

        # Parse BochaAI response
        results = data.get("results", [])
        was_truncated = len(results) > max_results
        truncated_results = results[:max_results]

        # Format results for display
        formatted_results = []
        for result in truncated_results:
            formatted_results.append(
                {
                    "title": result.get("title", "No title"),
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", result.get("description", "")),
                    "date": result.get("date", result.get("publishedAt", "")),
                }
            )

        return BochaSearchResult(
            query=query,
            results=formatted_results,
            result_count=len(formatted_results),
            was_truncated=was_truncated,
            search_type=search_type,
        )

    @classmethod
    def get_call_display(cls, event: ToolCallEvent) -> ToolCallDisplay:
        args = event.args
        return ToolCallDisplay(
            summary=f"Searching for: {args.query}",
            details=f"Search type: {args.search_type}",
        )

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        result = event.result
        if isinstance(result, BochaSearchResult):
            details = "\n".join(
                f"• {r['title']}\n  {r['url']}" for r in result.results[:5]
            )
            if result.was_truncated:
                details += f"\n... and {result.result_count - 5} more results"
            return ToolResultDisplay(
                summary=f"Found {result.result_count} results", details=details
            )
        return ToolResultDisplay(summary="Search completed")

"""Tools for form filling operations."""

from __future__ import annotations


from playwright.async_api import async_playwright
from src.browser import BrowserState, BrowserContext


async def get_page_information(url: str, context: BrowserContext) -> BrowserState:
    """Analyze form structure and extract field information."""
    try:
        await context.navigate_to(url)
        state = await context.get_state()
    except Exception as e:
        print(f"Error during page extraction: {str(e)}")
        raise
    return state

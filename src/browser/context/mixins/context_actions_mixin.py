import asyncio
import base64
import json
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.browser.context.context import BrowserContext, BrowserSession


class ContextActionsMixin:
    """Mixin class for browser context actions"""

    session: Optional["BrowserSession"]

    async def navigate_to(self: "BrowserContext", url: str) -> None:
        """Navigate to a URL"""
        session = await self.get_session()
        page = session.current_page
        await page.goto(url)
        await asyncio.sleep(self.config.minimum_wait_page_load_time)  # type: ignore

    async def refresh_page(self: "BrowserContext") -> None:
        """Refresh the current page"""
        session = await self.get_session()
        page = session.current_page
        await page.reload()
        await asyncio.sleep(self.config.minimum_wait_page_load_time)  # type: ignore

    async def get_page_html(self: "BrowserContext") -> str:
        """Get the current page HTML content"""
        session = await self.get_session()
        page = session.current_page
        return await page.content()

    async def execute_javascript(self: "BrowserContext", script: str) -> None:
        """Execute JavaScript code on the page"""
        session = await self.get_session()
        page = session.current_page
        await page.evaluate(script)

    async def take_screenshot(self: "BrowserContext", full_page: bool = False) -> str:
        """
        Returns a base64 encoded screenshot of the current page.
        """
        page = await self.get_current_page()

        screenshot = await page.screenshot(
            full_page=full_page,
            animations="disabled",
        )

        screenshot_b64 = base64.b64encode(screenshot).decode("utf-8")

        return screenshot_b64

    async def save_cookies(self: "BrowserContext"):
        """Save current cookies to file"""
        if self.session and self.session.context and self.config.cookies_file:
            try:
                cookies = await self.session.context.cookies()
                print(f"Saving {len(cookies)} cookies to {self.config.cookies_file}")
                with open(self.config.cookies_file, "w") as f:
                    json.dump(cookies, f)
            except Exception as e:
                print(f"Failed to save cookies: {str(e)}")

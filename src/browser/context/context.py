"""
Playwright browser but better?.
"""

import asyncio
import json
import os
import uuid
from typing import TYPE_CHECKING, Any, Optional, Type

from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Page
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import CoreSchema

from ..dom.builder import DomBuilder
from ..dom.data_structures import DOMElementNode, DOMState
from .context_config import BrowserContextConfig
from .mixins import (
    ContextActionsMixin,
    ContextInteractMixin,
    CSSSelectorMixin,
    DomActionsMixin,
)
from .state import BrowserError, BrowserSession, BrowserState

if TYPE_CHECKING:
    from ..browser import Browser


# TODO: Should this be a singleton , should it not be a singelton questions questions
class BrowserContext(
    ContextActionsMixin, CSSSelectorMixin, DomActionsMixin, ContextInteractMixin
):
    def __init__(
        self,
        browser: "Browser",
        config: BrowserContextConfig = BrowserContextConfig(),
    ):
        self.context_id = str(uuid.uuid4())
        print(f"Initializing new browser context with id: {self.context_id}")
        self.config = config
        self.browser = browser

        self.session: BrowserSession | None = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self._initialize_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def close(self):
        """Close the browser instance"""
        print("Closing browser context")
        try:
            if self.session is None:
                return

            await self.save_cookies()
            try:
                await self.session.context.close()
            except Exception as e:
                print(f"Failed to close context: {e}")
        finally:
            self.session = None

    async def _initialize_session(self):
        """Initialize the browser session"""
        print("Initializing browser context")

        playwright_browser = await self.browser.get_playwright_browser()

        context = await self._create_context(playwright_browser)

        existing_pages = context.pages
        if existing_pages:
            page = existing_pages[-1]
            print("Reusing existing page")
        else:
            page = await context.new_page()
            print("Created new page")

        initial_state = self._get_initial_state(page)

        self.session = BrowserSession(
            context=context,
            current_page=page,
            cached_state=initial_state,
        )
        return self.session

    async def get_session(self) -> BrowserSession:
        """Initialization of the browser and related components"""
        if self.session is None:
            return await self._initialize_session()
        return self.session

    async def get_current_page(self) -> Page:
        """Get the current page"""
        session = await self.get_session()
        return session.current_page

    async def _create_context(self, browser: PlaywrightBrowser):
        """Creates a new browser context and loads cookies if available."""
        if self.browser.config.chrome_instance_path and len(browser.contexts) > 0:
            context = browser.contexts[0]
        else:
            context = await browser.new_context(
                user_agent=self.config.user_agent,
                java_script_enabled=True,
                locale=self.config.locale,
            )

        if self.config.cookies_file and os.path.exists(self.config.cookies_file):
            with open(self.config.cookies_file, "r") as f:
                cookies = json.load(f)
                print(f"Loaded {len(cookies)} cookies from {self.config.cookies_file}")
                await context.add_cookies(cookies)

        return context

    async def get_state(self) -> BrowserState:
        """
        Get the current state of the browser
        needed for the agent to make decisions
        when
        """
        session = await self.get_session()
        session.cached_state = await self._update_state()

        if self.config.cookies_file:
            asyncio.create_task(self.save_cookies())

        return session.cached_state

    async def _update_state(self, focus_element: int = -1) -> BrowserState:
        """Update and return state."""
        try:
            page = await self.get_current_page()
            await page.evaluate("1")
        except Exception as e:
            raise BrowserError("Browser is invalid")

        try:
            dom_service = DomBuilder(page)
            content: DOMState = await dom_service.get_clickable_elements(
                focus_element=focus_element,
                highlight_elements=self.config.highlight_elements,
            )

            screenshot_b64 = await self.take_screenshot()
            pixels_above, pixels_below = await self.get_scroll_info(page)

            self.current_state = BrowserState(
                element_tree=content.element_tree,
                selector_map=content.selector_map,
                url=page.url,
                title=await page.title(),
                screenshot=screenshot_b64,
                pixels_above=pixels_above,
                pixels_below=pixels_below,
            )

            return self.current_state
        except Exception as e:
            print(f"Failed to update state: {str(e)}")
            if hasattr(self, "current_state"):
                return self.current_state
            raise

    async def reset_context(self):
        """
        Resets the browser session
        Call this when you don't want to kill the context but just kill the state
        """
        session = await self.get_session()

        pages = session.context.pages
        for page in pages:
            await page.close()

        session.cached_state = self._get_initial_state()
        session.current_page = await session.context.new_page()

    def _get_initial_state(self, page: Optional[Page] = None) -> BrowserState:
        """Get the initial state of the browser"""
        return BrowserState(
            element_tree=DOMElementNode(
                tag_name="root",
                is_visible=True,
                parent=None,
                xpath="",
                attributes={},
                children=[],
            ),
            selector_map={},
            url=page.url if page else "",
            title="",
            screenshot=None,
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls: Type["BrowserContext"],
        source: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate_browser_context(value: Any) -> "BrowserContext":
            if isinstance(value, cls):
                return value
            raise TypeError(
                f"Expected an instance of {cls.__name__}, got {type(value)}"
            )

        return core_schema.no_info_plain_validator_function(validate_browser_context)

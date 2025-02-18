"""
Playwright browser on steroids.
"""

import asyncio
from dataclasses import dataclass, field

from playwright._impl._api_structures import ProxySettings
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Playwright, async_playwright

from .context.context import BrowserContext, BrowserContextConfig


@dataclass
class BrowserConfig:
    r"""
    Configuration for the Browser.

    headless: bool = True
    Whether to run browser in headless mode

    chrome_instance_path: str | None = None
    Path to a Chrome instance to use to connect to your normal browser
    """

    headless: bool = False
    disable_security: bool = False
    chrome_instance_path: str | None = None
    proxy: ProxySettings | None = field(default=None)
    new_context_config: BrowserContextConfig = field(
        default_factory=BrowserContextConfig
    )
    _force_keep_browser_alive: bool = False


def singleton(cls):
    """
    Decorator to enforce a singleton pattern on a class.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Browser:
    """
    Playwright browser with some added stuff as a Singleton.
    """

    def __init__(self, config: BrowserConfig = BrowserConfig()):
        self.config = config
        self.playwright: Playwright | None = None
        self.playwright_browser: PlaywrightBrowser | None = None

        self.disable_security_args = []
        if self.config.disable_security:
            self.disable_security_args = [
                "--disable-web-security",
                "--disable-site-isolation-trials",
                "--disable-features=IsolateOrigins,site-per-process",
            ]

    async def new_context(
        self, config: BrowserContextConfig = BrowserContextConfig()
    ) -> BrowserContext:
        """Create a browser context."""
        return BrowserContext(config=config, browser=self)

    async def get_playwright_browser(self) -> PlaywrightBrowser:
        """Get the Playwright browser instance."""
        if self.playwright_browser is None:
            return await self._init()
        return self.playwright_browser

    async def _init(self):
        """Initialize the browser session."""
        playwright = await async_playwright().start()
        browser = await self._setup_browser(playwright)

        self.playwright = playwright
        self.playwright_browser = browser

        return self.playwright_browser

    def run_async(self, coro):
        event_loop = asyncio.get_event_loop()
        return event_loop.run_until_complete(coro)

    async def _setup_browser_with_instance(
        self, playwright: Playwright
    ) -> PlaywrightBrowser:
        """Sets up and returns a Playwright Browser instance with anti-detection measures."""
        if not self.config.chrome_instance_path:
            raise ValueError("Chrome instance path is required")
        import subprocess

        import requests

        try:
            response = requests.get("http://localhost:9222/json/version", timeout=2)
            if response.status_code == 200:
                print("Reusing existing Chrome instance")
                browser = await playwright.chromium.connect_over_cdp(
                    endpoint_url="http://localhost:9222",
                    timeout=20000,
                )
                return browser
        except requests.ConnectionError:
            print("No existing Chrome instance found, starting a new one")

        subprocess.Popen(
            [
                self.config.chrome_instance_path,
                "--remote-debugging-port=9222",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        for _ in range(10):
            try:
                response = requests.get("http://localhost:9222/json/version", timeout=2)
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                pass
            await asyncio.sleep(1)

        try:
            browser = await playwright.chromium.connect_over_cdp(
                endpoint_url="http://localhost:9222",
                timeout=20000,  # 20 second timeout for connection
            )
            return browser
        except Exception as e:
            print(f"Failed to start a new Chrome instance: {str(e)}")
            raise RuntimeError(
                "To start chrome in Debug mode, you need to close all existing Chrome instances and try again "
                "otherwise we cannot connect to the instance."
            )

    async def _setup_standard_browser(
        self, playwright: Playwright
    ) -> PlaywrightBrowser:
        """Sets up and returns a Playwright Browser instance."""
        browser = await playwright.chromium.launch(
            headless=self.config.headless,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-background-timer-throttling",
                "--disable-popup-blocking",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-window-activation",
                "--disable-focus-on-load",
                "--no-first-run",
                "--no-default-browser-check",
                "--no-startup-window",
                "--window-position=0,0",
            ]
            + self.disable_security_args,
            proxy=self.config.proxy,
        )
        return browser

    async def _setup_browser(self, playwright: Playwright) -> PlaywrightBrowser:
        """Sets up and returns a Playwright Browser instance."""
        try:
            if self.config.chrome_instance_path:
                return await self._setup_browser_with_instance(playwright)
            else:
                return await self._setup_standard_browser(playwright)
        except Exception as e:
            print(f"Failed to initialize Playwright browser: {str(e)}")
            raise

    async def close(self):
        """Close the browser instance."""
        try:
            if self.playwright_browser:
                await self.playwright_browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Failed to close browser properly: {e}")
        finally:
            self.playwright_browser = None
            self.playwright = None

    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            if self.playwright_browser or self.playwright:
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    loop.create_task(self.close())
                else:
                    asyncio.run(self.close())
        except Exception as e:
            print(f"Failed to cleanup browser in destructor: {e}")

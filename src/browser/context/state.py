from dataclasses import dataclass, field
from typing import Optional

from playwright.async_api import BrowserContext as PlaywrightBrowserContext
from playwright.async_api import Page

from src.browser.dom.data_structures import DOMState


@dataclass
class BrowserState(DOMState):
    url: str
    title: str
    screenshot: Optional[str] = None
    pixels_above: int = 0
    pixels_below: int = 0
    browser_errors: list[str] = field(default_factory=list)


@dataclass
class BrowserSession:
    context: PlaywrightBrowserContext
    current_page: Page
    cached_state: BrowserState


class BrowserError(Exception):
    """Base class for all browser errors"""

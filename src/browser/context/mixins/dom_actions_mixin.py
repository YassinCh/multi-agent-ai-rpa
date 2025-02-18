from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.browser.context.context import BrowserContext, BrowserSession

from playwright.async_api import ElementHandle, FrameLocator, Page

from src.browser.dom.data_structures import DOMElementNode, SelectorMap


class DomActionsMixin:
    """Mixin class for browser context actions"""

    session: Optional["BrowserSession"]

    async def get_selector_map(self: "BrowserContext") -> SelectorMap:
        session = await self.get_session()
        return session.cached_state.selector_map

    async def get_element_by_index(
        self: "BrowserContext", index: int
    ) -> ElementHandle | None:
        selector_map = await self.get_selector_map()
        element_handle = await self.get_locate_element(selector_map[index])
        return element_handle

    async def get_dom_element_by_index(
        self: "BrowserContext", index: int
    ) -> DOMElementNode:
        selector_map = await self.get_selector_map()
        return selector_map[index]

    async def get_locate_element(
        self: "BrowserContext", element: DOMElementNode
    ) -> Optional[ElementHandle]:
        current_frame = await self.get_current_page()

        parents: list[DOMElementNode] = []
        current = element
        while current.parent is not None:
            parent = current.parent
            parents.append(parent)
            current = parent

        parents.reverse()

        iframes = [item for item in parents if item.tag_name == "iframe"]
        for parent in iframes:
            css_selector = self._enhanced_css_selector_for_element(
                parent,
                include_dynamic_attributes=self.config.include_dynamic_attributes,
            )
            current_frame = current_frame.frame_locator(css_selector)

        css_selector = self._enhanced_css_selector_for_element(
            element, include_dynamic_attributes=self.config.include_dynamic_attributes
        )

        try:
            if isinstance(current_frame, FrameLocator):
                element_handle = await current_frame.locator(
                    css_selector
                ).element_handle()
                return element_handle
            else:
                element_handle = await current_frame.query_selector(css_selector)
                if element_handle:
                    await element_handle.scroll_into_view_if_needed()
                    return element_handle
                return None
        except Exception as e:
            print(f"Failed to locate element: {str(e)}")

    async def get_scroll_info(self: "BrowserContext", page: Page) -> tuple[int, int]:
        """Get scroll position information for the current page."""
        scroll_y = await page.evaluate("window.scrollY")
        viewport_height = await page.evaluate("window.innerHeight")
        total_height = await page.evaluate("document.documentElement.scrollHeight")
        pixels_above = scroll_y
        pixels_below = total_height - (scroll_y + viewport_height)
        return pixels_above, pixels_below

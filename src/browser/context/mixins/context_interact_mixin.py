from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.browser.context.context import BrowserContext, BrowserSession


from src.browser.context.state import BrowserError, BrowserSession
from src.browser.dom.data_structures import DOMElementNode


class ContextInteractMixin:
    """Mixin class for browser context actions"""

    session: Optional["BrowserSession"]

    async def _input_text_element_node(
        self: "BrowserContext", element_node: DOMElementNode, text: str
    ):
        """
        Input text into an element with proper error handling and state management.
        Handles different types of input fields and ensures proper element state before input.
        """
        try:
            if element_node.highlight_index is not None:
                await self._update_state(focus_element=element_node.highlight_index)

            page = await self.get_current_page()
            element_handle = await self.get_locate_element(element_node)

            if element_handle is None:
                raise BrowserError(f"Element: {repr(element_node)} not found")

            await element_handle.wait_for_element_state("stable", timeout=2000)
            await element_handle.scroll_into_view_if_needed(timeout=2100)

            is_contenteditable = await element_handle.get_property("isContentEditable")

            try:
                if await is_contenteditable.json_value():
                    await element_handle.evaluate('el => el.textContent = ""')
                    await element_handle.type(text, delay=5)
                else:
                    await element_handle.fill(text)
            except Exception:
                print("Could not type text into element. Trying to click and type.")
                await element_handle.click()
                await element_handle.type(text, delay=5)

        except Exception as e:
            print(
                f"Failed to input text into element: {repr(element_node)}. Error: {str(e)}"
            )
            raise BrowserError(
                f"Failed to input text into index {element_node.highlight_index}"
            )

    async def _click_element_node(
        self: "BrowserContext", element_node: DOMElementNode
    ) -> Optional[str]:
        """
        Optimized method to click an element using xpath.
        """
        page = await self.get_current_page()

        try:
            if element_node.highlight_index is not None:
                await self._update_state(focus_element=element_node.highlight_index)

            element_handle = await self.get_locate_element(element_node)

            if element_handle is None:
                raise BrowserError(f"Element: {repr(element_node)} not found")

            async def perform_click(click_func):
                """Performs the actual click, handling both download
                and navigation scenarios."""
                await click_func()
                await page.wait_for_load_state()

            try:
                return await perform_click(lambda: element_handle.click(timeout=1500))

            except Exception:
                try:
                    return await perform_click(
                        lambda: page.evaluate("(el) => el.click()", element_handle)
                    )
                except Exception as e:
                    raise BrowserError(f"Failed to click element: {str(e)}")
        except Exception as e:
            raise BrowserError(
                f"Failed to click element: {repr(element_node)}. Error: {str(e)}"
            )

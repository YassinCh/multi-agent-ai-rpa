import gc
from importlib import resources
from typing import Optional

from playwright.async_api import Page

from .data_structures import (
    DOMBaseNode,
    DOMElementNode,
    DOMState,
    DOMTextNode,
    SelectorMap,
)


class DomBuilder:
    def __init__(self, page: Page):
        self.page = page
        self.xpath_cache = {}

        self.js_code = resources.read_text("src.browser.dom", "buildDomTree.js")

    async def get_clickable_elements(
        self,
        highlight_elements: bool = True,
        focus_element: int = -1,
    ) -> DOMState:
        element_tree, selector_map = await self._build_dom_tree(
            highlight_elements, focus_element
        )

        dom_state = DOMState(element_tree=element_tree, selector_map=selector_map)

        return dom_state

    async def _build_dom_tree(
        self,
        highlight_elements: bool,
        focus_element: int,
    ) -> tuple[DOMElementNode, SelectorMap]:
        if await self.page.evaluate("1+1") != 2:
            raise ValueError("No Javascript SAD!")

        # Lets do some javascript
        args = {
            "doHighlightElements": highlight_elements,
            "focusHighlightIndex": focus_element,
        }

        eval_page = await self.page.evaluate(self.js_code, args)

        js_node_map = eval_page["map"]
        js_root_id = eval_page["rootId"]

        selector_map = {}
        node_map = {}

        for id, node_data in js_node_map.items():
            node, children_ids = self._parse_node(node_data)
            if node is None:
                continue

            node_map[id] = node

            if isinstance(node, DOMElementNode) and node.highlight_index is not None:
                selector_map[node.highlight_index] = node

            if isinstance(node, DOMElementNode):
                for child_id in children_ids:
                    if child_id not in node_map:
                        continue

                    child_node = node_map[child_id]

                    child_node.parent = node
                    node.children.append(child_node)

        html_to_dict = node_map[js_root_id]

        if html_to_dict is None or not isinstance(html_to_dict, DOMElementNode):
            raise ValueError("Failed to parse HTML to dictionary")

        return html_to_dict, selector_map

    def _parse_node(
        self,
        node_data: dict,
    ) -> tuple[Optional[DOMBaseNode], list[int]]:
        if not node_data:
            return None, []

        if node_data.get("type") == "TEXT_NODE":
            text_node = DOMTextNode(
                text=node_data["text"],
                is_visible=node_data["isVisible"],
                parent=None,
            )
            return text_node, []

        element_node = DOMElementNode(
            tag_name=node_data["tagName"],
            xpath=node_data["xpath"],
            attributes=node_data.get("attributes", {}),
            children=[],
            is_visible=node_data.get("isVisible", False),
            is_interactive=node_data.get("isInteractive", False),
            is_top_element=node_data.get("isTopElement", False),
            highlight_index=node_data.get("highlightIndex"),
            shadow_root=node_data.get("shadowRoot", False),
            parent=None,
        )

        children_ids = node_data.get("children", [])

        return element_node, children_ids

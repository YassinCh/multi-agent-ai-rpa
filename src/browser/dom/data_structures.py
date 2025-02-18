from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from .views import DOMElementNode

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional


@dataclass(frozen=False)
class DOMBaseNode:
    is_visible: bool
    parent: Optional["DOMElementNode"]


@dataclass(frozen=False)
class DOMTextNode(DOMBaseNode):
    text: str
    type: str = "TEXT_NODE"

    def has_parent_with_highlight_index(self) -> bool:
        current = self.parent
        while current is not None:
            if current.highlight_index is not None:
                return True
            current = current.parent
        return False


@dataclass(frozen=False)
class DOMElementNode(DOMBaseNode):
    """
    So this is the code for a DOM Element which is the object to use to interact with elements
    """

    tag_name: str
    xpath: str
    attributes: Dict[str, str]
    children: List[DOMBaseNode]
    is_interactive: bool = False
    is_top_element: bool = False
    shadow_root: bool = False
    highlight_index: Optional[int] = None

    def __repr__(self) -> str:
        tag_str = f"<{self.tag_name}"

        for key, value in self.attributes.items():
            tag_str += f' {key}="{value}"'
        tag_str += ">"

        extras = []
        if self.is_interactive:
            extras.append("interactive")
        if self.is_top_element:
            extras.append("top")
        if self.shadow_root:
            extras.append("shadow-root")
        if self.highlight_index is not None:
            extras.append(f"highlight:{self.highlight_index}")

        if extras:
            tag_str += f' [{", ".join(extras)}]'

        return tag_str

    def get_all_text_till_next_clickable_element(self, max_depth: int = -1) -> str:
        text_parts = []

        def collect_text(node: DOMBaseNode, current_depth: int) -> None:
            if max_depth != -1 and current_depth > max_depth:
                return

            if (
                isinstance(node, DOMElementNode)
                and node != self
                and node.highlight_index is not None
            ):
                return

            if isinstance(node, DOMTextNode):
                text_parts.append(node.text)
            elif isinstance(node, DOMElementNode):
                for child in node.children:
                    collect_text(child, current_depth + 1)

        collect_text(self, 0)
        return "\n".join(text_parts).strip()

    def clickable_elements_to_string(self, include_attributes: list[str] = []) -> str:
        """Convert the processed DOM content to HTML."""
        formatted_text = []

        def process_node(node: DOMBaseNode, depth: int) -> None:
            if isinstance(node, DOMElementNode):
                if node.highlight_index is not None:
                    attributes_str = ""
                    if include_attributes:
                        attributes_str = " " + " ".join(
                            f'{key}="{value}"'
                            for key, value in node.attributes.items()
                            if key in include_attributes
                        )
                    formatted_text.append(
                        f"[{node.highlight_index}]<{node.tag_name}{attributes_str}>{node.get_all_text_till_next_clickable_element()}</{node.tag_name}>"
                    )

                for child in node.children:
                    process_node(child, depth + 1)

            elif isinstance(node, DOMTextNode):
                if not node.has_parent_with_highlight_index():
                    formatted_text.append(f"[]{node.text}")

        process_node(self, 0)
        return "\n".join(formatted_text)

    def get_file_upload_element(
        self, check_siblings: bool = True
    ) -> Optional["DOMElementNode"]:
        if self.tag_name == "input" and self.attributes.get("type") == "file":
            return self

        for child in self.children:
            if isinstance(child, DOMElementNode):
                result = child.get_file_upload_element(check_siblings=False)
                if result:
                    return result

        if check_siblings and self.parent:
            for sibling in self.parent.children:
                if sibling is not self and isinstance(sibling, DOMElementNode):
                    result = sibling.get_file_upload_element(check_siblings=False)
                    if result:
                        return result

        return None

    def get_advanced_css_selector(self) -> str:
        from srcr.browser.context import BrowserContext

        return BrowserContext._enhanced_css_selector_for_element(self)


SelectorMap = dict[int, DOMElementNode]


@dataclass
class DOMState:
    element_tree: DOMElementNode
    selector_map: SelectorMap

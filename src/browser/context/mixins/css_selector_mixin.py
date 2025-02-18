import re
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.browser.context.context import BrowserContext, BrowserSession

from src.browser.dom.data_structures import DOMElementNode


class CSSSelectorMixin:
    """Mixin class for browser context actions"""

    session: Optional["BrowserSession"]

    @classmethod
    def _convert_simple_xpath_to_css_selector(cls: "BrowserContext", xpath: str) -> str:
        """
        Converts simple XPath expressions to CSS selectors
        This is needed mostly for iframes and stuff
        """
        if not xpath:
            return ""
        xpath = xpath.lstrip("/")

        parts = xpath.split("/")
        css_parts = []

        for part in parts:
            if not part:
                continue

            if "[" in part:
                base_part = part[: part.find("[")]
                index_part = part[part.find("[") :]

                indices = [i.strip("[]") for i in index_part.split("]")[:-1]]

                for idx in indices:
                    try:
                        if idx.isdigit():
                            index = int(idx) - 1
                            base_part += f":nth-of-type({index + 1})"
                        elif idx == "last()":
                            base_part += ":last-of-type"
                        elif "position()" in idx:
                            if ">1" in idx:
                                base_part += ":nth-of-type(n+2)"
                    except ValueError:
                        continue

                css_parts.append(base_part)
            else:
                css_parts.append(part)

        base_selector = " > ".join(css_parts)
        return base_selector

    @classmethod
    def _enhanced_css_selector_for_element(
        cls,
        element: DOMElementNode,
        include_dynamic_attributes: bool = True,
    ) -> str:
        """
        Creates a CSS selector for a DOM element.
        """
        try:
            css_selector = cls._convert_simple_xpath_to_css_selector(element.xpath)

            if (
                "class" in element.attributes
                and element.attributes["class"]
                and include_dynamic_attributes
            ):
                valid_class_name_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_-]*$")

                classes = element.attributes["class"].split()
                for class_name in classes:
                    if not class_name.strip():
                        continue

                    if valid_class_name_pattern.match(class_name):
                        css_selector += f".{class_name}"
                    else:
                        continue

            SAFE_ATTRIBUTES = {
                "id",
                "name",
                "type",
                "placeholder",
                "aria-label",
                "aria-labelledby",
                "aria-describedby",
                "role",
                "for",
                "autocomplete",
                "required",
                "readonly",
                "alt",
                "title",
                "src",
                "href",
                "target",
            }

            if include_dynamic_attributes:
                dynamic_attributes = {
                    "data-id",
                    "data-qa",
                    "data-cy",
                    "data-testid",
                }
                SAFE_ATTRIBUTES.update(dynamic_attributes)

            for attribute, value in element.attributes.items():
                if attribute == "class":
                    continue

                if not attribute.strip():
                    continue

                if attribute not in SAFE_ATTRIBUTES:
                    continue

                safe_attribute = attribute.replace(":", r"\:")

                if value == "":
                    css_selector += f"[{safe_attribute}]"
                elif any(char in value for char in "\"'<>`\n\r\t"):
                    collapsed_value = re.sub(r"\s+", " ", value).strip()
                    safe_value = collapsed_value.replace('"', '\\"')
                    css_selector += f'[{safe_attribute}*="{safe_value}"]'
                else:
                    css_selector += f'[{safe_attribute}="{value}"]'

            return css_selector

        except Exception:
            tag_name = element.tag_name or "*"
            return f"{tag_name}[highlight_index='{element.highlight_index}']"

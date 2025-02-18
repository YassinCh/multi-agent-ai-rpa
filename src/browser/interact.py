import asyncio
import json

import markdownify

from .context.context import BrowserContext


class BrowserInteract:
    """
    This class provides methods to let the agent interact with the browser
    TODO: Make the parameters needed into pydantic stuff so that the action can be validated by pydantic AI
    TODO: Make sure the msg is very descriptive as it is what is being shown to the agent
    TODO: Probably it would be nicer to return some ActionResult object to give to the agent
    Right now everything in this class is returning a msg for the agent
    """

    async def go_to_url(url, browser: BrowserContext):
        page = await browser.get_current_page()
        await page.goto(url)
        await page.wait_for_load_state()
        msg = f"Navigated to {url}"
        print(msg)
        return msg

    async def go_back(_, browser: BrowserContext):
        await browser.go_back()
        msg = "Navigated back"
        print(msg)
        return msg

    async def click_element(index: int, browser: BrowserContext):
        session = await browser.get_session()
        state = session.cached_state

        if index not in state.selector_map:
            raise Exception(
                f"Element with index {index} does not exist - retry or use alternative actions"
            )

        element_node = state.selector_map[index]

        msg = None

        try:
            download_path = await browser._click_element_node(element_node)
            if download_path:
                msg = f" Downloaded file to {download_path}"
            else:
                msg = f" Clicked button with index {index}: {element_node.get_all_text_till_next_clickable_element(max_depth=2)}"

            print(msg)
            return msg
        except Exception as e:
            print(
                f"Element not clickable with index {index} - most likely the page changed"
            )
            return str(e)

    async def input_text(
        index: int,
        text: str,
        browser: BrowserContext,
        has_sensitive_data: bool = False,
    ):
        selector_map = await browser.get_selector_map()
        dom_element = selector_map[index]

        if index not in selector_map:
            raise Exception(
                f"Element index {index} does not exist - retry or use alternative actions"
            )

        dom_element = selector_map[index]
        await browser._input_text_element_node(dom_element, text)
        if not has_sensitive_data:
            msg = f"Input {text} into index {index}"
        else:
            msg = f"Input sensitive data into index {index}"
        print(msg)
        return msg

    async def extract_content(goal: str, browser: BrowserContext):
        page = await browser.get_current_page()

        content = markdownify.markdownify(await page.content())

        try:
            msg = f"Extracted from page\n: {content}\n"
            print(msg)
            return msg
        except Exception as e:
            print(f"Error extracting content: {e}")
            msg = f" Extracted from page\n: {content}\n"
            print(msg)
            return msg

    async def scroll_to_text(text: str, browser: BrowserContext):
        page = await browser.get_current_page()
        try:
            locators = [
                page.get_by_text(text, exact=False),
                page.locator(f"text={text}"),
                page.locator(f"//*[contains(text(), '{text}')]"),
            ]

            for locator in locators:
                try:
                    if await locator.count() > 0 and await locator.first.is_visible():
                        await locator.first.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        msg = f"Scrolled to text: {text}"
                        print(msg)
                        return msg
                except Exception as e:
                    print(f"Locator attempt failed: {str(e)}")
                    continue

            msg = f"Text '{text}' not found or not visible on page"
            print(msg)
            return msg

        except Exception as e:
            msg = f"Failed to scroll to text '{text}': {str(e)}"
            print(msg)
            return msg

    async def get_dropdown_options(index: int, browser: BrowserContext) -> str:
        """Get all options from a native dropdown"""
        page = await browser.get_current_page()
        selector_map = await browser.get_selector_map()
        dom_element = selector_map[index]

        try:
            all_options = []
            frame_index = 0

            for frame in page.frames:
                try:
                    options = await frame.evaluate(
                        """
                        (xpath) => {
                            const select = document.evaluate(xpath, document, null,
                                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (!select) return null;

                            return {
                                options: Array.from(select.options).map(opt => ({
                                    text: opt.text, //do not trim, because we are doing exact match in select_dropdown_option
                                    value: opt.value,
                                    index: opt.index
                                })),
                                id: select.id,
                                name: select.name
                            };
                        }
                    """,
                        dom_element.xpath,
                    )

                    if options:
                        print(f"Found dropdown in frame {frame_index}")
                        print(f'Dropdown ID: {options["id"]}, Name: {options["name"]}')

                        formatted_options = []
                        for opt in options["options"]:
                            # encoding ensures AI uses the exact string in select_dropdown_option
                            encoded_text = json.dumps(opt["text"])
                            formatted_options.append(
                                f'{opt["index"]}: text={encoded_text}'
                            )

                        all_options.extend(formatted_options)

                except Exception as frame_e:
                    print(f"Frame {frame_index} evaluation failed: {str(frame_e)}")

                frame_index += 1

            if all_options:
                msg = "\n".join(all_options)
                msg += "\nUse the exact text string in select_dropdown_option"
                print(msg)
                return msg
            else:
                msg = "No options found in any frame for dropdown"
                print(msg)
                return msg

        except Exception as e:
            print(f"Failed to get dropdown options: {str(e)}")
            msg = f"Error getting options: {str(e)}"
            print(msg)
            return msg

    async def select_dropdown_option(
        index: int,
        text: str,
        browser: BrowserContext,
    ):
        """Select dropdown option by the text of the option you want to select"""
        page = await browser.get_current_page()
        selector_map = await browser.get_selector_map()
        dom_element = selector_map[index]

        if dom_element.tag_name != "select":
            print(
                f"Element is not a select! Tag: {dom_element.tag_name}, Attributes: {dom_element.attributes}"
            )
            msg = f"Cannot select option: Element with index {index} is a {dom_element.tag_name}, not a select"
            return msg

        print(f"Attempting to select'{text}' using xpath: {dom_element.xpath}")

        xpath = "//" + dom_element.xpath

        try:
            frame_index = 0
            for frame in page.frames:
                try:
                    print(f"Trying frame {frame_index} URL: {frame.url}")
                    find_dropdown_js = """
                        (xpath) => {
                            try {
                                const select = document.evaluate(xpath, document, null,
                                    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (!select) return null;
                                if (select.tagName.toLowerCase() !== 'select') {
                                    return {
                                        error: `Found element but it's a ${select.tagName}, not a SELECT`,
                                        found: false
                                    };
                                }
                                return {
                                    id: select.id,
                                    name: select.name,
                                    found: true,
                                    tagName: select.tagName,
                                    optionCount: select.options.length,
                                    currentValue: select.value,
                                    availableOptions: Array.from(select.options).map(o => o.text.trim())
                                };
                            } catch (e) {
                                return {error: e.toString(), found: false};
                            }
                        }
                    """

                    dropdown_info = await frame.evaluate(
                        find_dropdown_js, dom_element.xpath
                    )

                    if dropdown_info:
                        if not dropdown_info.get("found"):
                            print(
                                f'Frame {frame_index} error: {dropdown_info.get("error")}'
                            )
                            continue

                        print(f"Found dropdown in frame {frame_index}: {dropdown_info}")

                        selected_option_values = (
                            await frame.locator("//" + dom_element.xpath)
                            .nth(0)
                            .select_option(label=text, timeout=1000)
                        )

                        msg = f"selected option {text} with value {selected_option_values}"
                        print(msg + f" in frame {frame_index}")

                        return msg

                except Exception as frame_e:
                    print(f"Frame {frame_index} attempt failed: {str(frame_e)}")
                    print(f"Frame type: {type(frame)}")
                    print(f"Frame URL: {frame.url}")

                frame_index += 1

            msg = f"Could not select option '{text}' in any frame"
            print(msg)
            return msg

        except Exception as e:
            msg = f"Selection failed: {str(e)}"
            print(msg)
            return msg

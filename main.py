from src.browser import Browser, BrowserConfig
from src.browser import BrowserInteract


async def main():
    # Initialize browser with non-headless mode
    config = BrowserConfig(
        headless=True, disable_security=False  # Set to False to see the browser
    )

    browser = Browser(config)

    try:
        print("Starting Context")
        context = await browser.new_context()

        async with context as context:
            print("Got context")
            await context.navigate_to("http://127.0.0.1:8000")
            print("Navigated")
            state = await context.get_state()

            print("\nFound Input Elements:")
            print("-" * 50)

            for index, node in state.selector_map.items():
                print(f"Input Element {index}:")
                print(f"  Type: {node.attributes.get('type', 'text')}")
                print(f"  Name: {node.attributes.get('name', 'N/A')}")
                print(f"  ID: {node.attributes.get('id', 'N/A')}")
                print(f"  Class: {node.attributes.get('class', 'N/A')}")
                print("-" * 50)
            test = node.get_advanced_css_selector()
            print(test)
            print("-" * 50)

            test2 = node.get_all_text_till_next_clickable_element()
            print(test2)
            test3 = node.clickable_elements_to_string()
            print(test3)

            msg = await BrowserInteract.input_text(5, "hello", context)
            print(msg)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

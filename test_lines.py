# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
# Generated on 2025-02-18T02:03:11.415367

import asyncio

from src.browser import Browser, BrowserConfig, BrowserInteract


async def main(url):
    config = BrowserConfig(headless=False, disable_security=False)
    browser = Browser(config)
    context = await browser.new_context()
    msg = ""
    async with context:
        try:
            await context.navigate_to(url)
            _ = await context.get_state()
            await BrowserInteract.input_text(1, "John", context)
            await BrowserInteract.input_text(3, "Doe", context)
            await BrowserInteract.input_text(5, "john.doe@example.com", context)
            await BrowserInteract.input_text(7, "123-456-7890", context)
            await BrowserInteract.input_text(15, "1997-10-19", context)
            await BrowserInteract.input_text(9, "123 Main St", context)
            print(msg)
        except Exception as e:
            print("Error during page:" + str(e))
            raise e

    print(msg)


url = "http://127.0.0.1:8000"
asyncio.run(main(url))

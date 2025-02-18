import asyncio

from src.browser import Browser, BrowserConfig, BrowserInteract


async def run_line(url: str, line: str):
    """
    Runs the action line in a seperate context
    TODO: I could pass in the current context, and undo the line?
    """
    config = BrowserConfig(headless=True, disable_security=False)
    browser = Browser(config)
    context = await browser.new_context()
    msg = ""
    async with context:
        try:
            await context.navigate_to(url)
            _ = await context.get_state()  # This makes sure the state cache is filled
            globals_dict = {
                "BrowserInteract": BrowserInteract,
                "context": context,
                "asyncio": asyncio,
            }
            locals_dict = {}

            code = f"""
async def __run():
    result = {line}
    return result
"""
            exec(code, globals_dict, locals_dict)

            msg = await locals_dict["__run"]()
            print(msg)
        except Exception as e:
            msg = f"An error occurred: {e}"
    return msg

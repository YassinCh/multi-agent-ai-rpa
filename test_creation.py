import asyncio

import aiofiles


async def create_test_py(lines, url):
    template = """import asyncio

from src.browser import Browser, BrowserConfig, BrowserInteract


async def main(url):
\tconfig = BrowserConfig(headless=False, disable_security=False)
\tbrowser = Browser(config)
\tcontext = await browser.new_context()
\tmsg = ""
\tasync with context:
\t\ttry:
\t\t\tawait context.navigate_to(url)
\t\t\t_ = await context.get_state()
{inserted_lines}
\t\texcept Exception as e:
\t\t\tprint("Error during page:" + str(e))
\t\t\traise e

\tprint(msg)

url = "{url}"
asyncio.run(main(url))
"""

    # Each inserted line will be indented with three tabs.
    indent = "\t\t\t"
    inserted_lines = "\n".join(indent + line for line in lines)

    # Fill in the template with the inserted lines and URL.
    content = template.format(inserted_lines=inserted_lines, url=url)

    # Asynchronously write the content to test.py.
    async with aiofiles.open("test.py", "w") as f:
        await f.write(content)


if __name__ == "__main__":
    # Example usage
    lines_to_insert = ["print('Line 1 executed')", "print('Line 2 executed')"]
    hardcoded_url = "http://example.com"
    asyncio.run(create_test_py(lines_to_insert, hardcoded_url))

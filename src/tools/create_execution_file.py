import datetime

import aiofiles


async def create_execution_file(lines: list, url: str):
    """
    Takes a list of browser execution lines
    and writes them to a Python file with an auto-generated disclaimer.
    """
    generated_date = datetime.datetime.now().isoformat()

    template = """# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
# Generated on {generated_date}

import asyncio

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

    # Fill in the template with the inserted lines, URL, and generated timestamp.
    content = template.format(
        inserted_lines=inserted_lines, url=url, generated_date=generated_date
    )

    # Asynchronously write the content to test_lines.py.
    async with aiofiles.open("test_lines.py", "w") as f:
        await f.write(content)

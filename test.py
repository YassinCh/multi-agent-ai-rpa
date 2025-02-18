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
			print('Line 1 executed')
			print('Line 2 executed')
		except Exception as e:
			print("Error during page:" + str(e))
			raise e

	print(msg)

url = "http://example.com"
asyncio.run(main(url))

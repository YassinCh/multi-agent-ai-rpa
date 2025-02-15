"""Tools for form filling operations."""

from __future__ import annotations

import asyncio
import sys
from typing import Annotated, List

from playwright.async_api import async_playwright
from langchain_core.tools import InjectedToolArg

from src.configuration import Configuration
from src.data import FormField


async def analyze_form(
    url: str, *, config: Annotated[Configuration, InjectedToolArg]
) -> List[FormField]:
    """Analyze form structure and extract field information."""
    print("Starting form analysis...")

    # if sys.platform.startswith("win"):
    #     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    form_fields = []
    try:
        print("Initializing Playwright...")
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=False)
            print("Creating new context and page...")
            context = await browser.new_context()
            page = await context.new_page()

            try:
                print(f"Navigating to {url}...")
                # Navigate and wait for network idle
                await page.goto(url, wait_until="networkidle", timeout=config.timeout)
                print("Navigation complete!")

                print("Waiting for form elements...")
                # Wait for form elements to be present
                await page.wait_for_selector(
                    "input, select, textarea", timeout=config.timeout
                )
                print("Form elements found!")

                print("Analyzing form fields...")
                for input_elem in await page.query_selector_all(
                    "input, select, textarea"
                ):
                    field_type = await input_elem.get_attribute(
                        "type"
                    ) or await input_elem.evaluate("el => el.tagName.toLowerCase()")
                    field_name = await input_elem.get_attribute("name")
                    field_id = await input_elem.get_attribute("id")

                    if not field_name:
                        continue

                    # Try to find label
                    label_text = None
                    if field_id:
                        label_elem = await page.query_selector(
                            f'label[for="{field_id}"]'
                        )
                        if label_elem:
                            label_text = await label_elem.text_content()

                    form_fields.append(
                        FormField(
                            name=field_name,
                            type=field_type,
                            id=field_id,
                            label=label_text,
                            placeholder=await input_elem.get_attribute("placeholder"),
                        )
                    )
                print(f"Found {len(form_fields)} form fields!")
            except Exception as e:
                print(f"Error during form analysis (inner): {str(e)}")
                raise
            finally:
                print("Cleaning up browser resources...")
                await context.close()
                await browser.close()
                print("Browser cleanup complete!")
    except Exception as e:
        print(f"Error during form analysis: {str(e)}")
        raise

    return form_fields

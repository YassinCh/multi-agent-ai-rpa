from dataclasses import dataclass


@dataclass
class BrowserContextConfig:
    """
    Browser Context Configuration
    """

    cookies_file: str | None = None
    minimum_wait_page_load_time: float = 0.5
    wait_for_network_idle_page_load_time: float = 1
    maximum_wait_page_load_time: float = 5
    locale: str | None = None
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    )

    highlight_elements: bool = True
    include_dynamic_attributes: bool = True

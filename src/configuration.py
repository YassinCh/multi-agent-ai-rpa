"""Define the configurable parameters for the form filling agent."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Optional

from langchain_core.runnables import RunnableConfig, ensure_config


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the RPA agent."""

    headless: bool = field(
        default=True,
        metadata={"description": "Whether to run the browser in headless mode."},
    )

    screenshot_dir: str = field(
        default="screenshots",
        metadata={"description": "Directory to save form screenshots in."},
    )

    timeout: int = field(
        default=30000,
        metadata={"description": "Timeout in milliseconds for browser operations."},
    )

    field_match_threshold: float = field(
        default=0.7,
        metadata={"description": "Threshold for field name matching confidence."},
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})

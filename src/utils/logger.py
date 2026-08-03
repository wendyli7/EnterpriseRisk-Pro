"""Central logging configuration for the project."""

from __future__ import annotations

import logging
import os


def configure_logging(level: str | None = None) -> None:
    """Configure one consistent console logger for command-line modules."""
    resolved_level = (level or os.getenv("ENTERPRISE_RISK_LOG_LEVEL", "INFO")).upper()
    numeric_level = getattr(logging, resolved_level, logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module logger without configuring global handlers."""
    return logging.getLogger(name)
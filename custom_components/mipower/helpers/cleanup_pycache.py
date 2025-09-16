# custom_components/mipower/helpers/cleanup_pycache.py
"""Utilities to safely remove __pycache__ directories under an integration."""

from __future__ import annotations

import shutil
from pathlib import Path
import logging
from typing import Iterable, Union

_LOGGER = logging.getLogger(__name__)

def _iter_pycache_dirs(base: Union[str, Path]):
    base_path = Path(base)
    if not base_path.exists():
        return
    for p in base_path.rglob("__pycache__"):
        if p.is_dir():
            yield p

def cleanup_pycache(base: Union[str, Path]) -> int:
    """
    Remove all __pycache__ directories under `base`.
    Returns the number of removed directories.
    """
    base_path = Path(base)
    removed = 0
    for pycache in _iter_pycache_dirs(base_path):
        try:
            shutil.rmtree(pycache)
            _LOGGER.info("cleanup_pycache: removed %s", pycache)
            removed += 1
        except Exception as exc:
            _LOGGER.warning("cleanup_pycache: failed to remove %s: %s", pycache, exc)
    _LOGGER.debug("cleanup_pycache: finished under %s, removed=%s", base_path, removed)
    return removed

def cleanup_if_no_entries(hass, domain: str, integration_dir: Union[str, Path]) -> int:
    """
    Helper: if there are <=1 entries for domain, perform cleanup; returns number removed.
    """
    try:
        entries = hass.config_entries.async_entries(domain)
        if len(entries) <= 1:
            return cleanup_pycache(integration_dir)
    except Exception as exc:
        _LOGGER.exception("cleanup_pycache.cleanup_if_no_entries error: %s", exc)
    return 0

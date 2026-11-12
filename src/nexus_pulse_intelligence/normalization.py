"""Deterministic helpers for URL and text normalization."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_TRACKING_KEYS = {"fbclid", "gclid", "dclid", "mc_cid", "mc_eid", "ref_src"}
_TRACKING_PREFIXES = ("utm_",)
_WHITESPACE = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^\w\s]", flags=re.UNICODE)


def canonicalize_url(url: str) -> str:
    """Normalize a URL for exact-duplicate checks without fetching it."""
    raw = url.strip()
    parts = urlsplit(raw)
    scheme = (parts.scheme or "https").lower()
    hostname = (parts.hostname or "").lower()
    if not hostname:
        raise ValueError("URL must contain a hostname")

    if hostname.startswith("www."):
        hostname = hostname[4:]

    port = parts.port
    netloc = hostname
    if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc = f"{hostname}:{port}"

    query_items = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        key_lower = key.lower()
        if key_lower in _TRACKING_KEYS or key_lower.startswith(_TRACKING_PREFIXES):
            continue
        query_items.append((key, value))
    query_items.sort()

    path = parts.path.rstrip("/") or "/"
    return urlunsplit((scheme, netloc, path, urlencode(query_items, doseq=True), ""))


def normalize_text(value: str) -> str:
    """Normalize text for robust comparison, preserving Unicode letters and digits."""
    value = unicodedata.normalize("NFKC", value).casefold()
    value = _NON_WORD.sub(" ", value)
    return _WHITESPACE.sub(" ", value).strip()


def text_fingerprint(value: str) -> str:
    """Return a stable SHA-256 fingerprint of normalized text."""
    normalized = normalize_text(value)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

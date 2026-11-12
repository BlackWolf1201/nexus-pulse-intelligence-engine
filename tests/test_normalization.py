from nexus_pulse_intelligence.normalization import (
    canonicalize_url,
    normalize_text,
    text_fingerprint,
)


def test_canonicalize_url_removes_tracking_and_fragment() -> None:
    assert canonicalize_url("https://www.example.com/news/?utm_source=x&id=42#top") == (
        "https://example.com/news?id=42"
    )


def test_canonicalize_url_rejects_missing_hostname() -> None:
    try:
        canonicalize_url("/relative/path")
    except ValueError as exc:
        assert "hostname" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_normalize_text_is_case_and_punctuation_insensitive() -> None:
    assert normalize_text("GTA VI: NOVO Rumor!") == "gta vi novo rumor"


def test_fingerprint_is_stable_after_normalization() -> None:
    assert text_fingerprint("New Game!") == text_fingerprint(" new   game ")

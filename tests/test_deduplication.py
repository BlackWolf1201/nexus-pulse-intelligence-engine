from nexus_pulse_intelligence.deduplication import (
    ArticleIdentity,
    DuplicateStatus,
    compare_articles,
)


def article(url: str, title: str, **kwargs: str) -> ArticleIdentity:
    return ArticleIdentity(source_id="source-a", url=url, title=title, **kwargs)


def test_same_canonical_url_is_exact_duplicate() -> None:
    result = compare_articles(
        article("https://www.example.com/story?utm_source=rss", "A story"),
        article("https://example.com/story", "Different title"),
    )
    assert result.status is DuplicateStatus.EXACT_DUPLICATE
    assert result.reason == "same_canonical_url"


def test_same_external_id_within_same_source_is_duplicate() -> None:
    result = compare_articles(
        article("https://example.com/a", "A", external_id="item-1"),
        article("https://example.com/b", "B", external_id="item-1"),
    )
    assert result.status is DuplicateStatus.EXACT_DUPLICATE


def test_similar_titles_are_flagged_not_discarded() -> None:
    result = compare_articles(
        article("https://example.com/a", "Sony announces a new PlayStation update"),
        article("https://other.example/b", "Sony announces new PlayStation update"),
    )
    assert result.status is DuplicateStatus.POSSIBLE_DUPLICATE


def test_distinct_titles_remain_distinct() -> None:
    result = compare_articles(
        article("https://example.com/a", "Nintendo releases a new console"),
        article("https://example.com/b", "AMD announces a graphics processor"),
    )
    assert result.status is DuplicateStatus.DISTINCT

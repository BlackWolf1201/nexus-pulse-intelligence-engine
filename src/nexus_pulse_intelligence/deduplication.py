"""Conservative duplicate detection. Similar stories are never auto-discarded here."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import StrEnum

from nexus_pulse_intelligence.normalization import canonicalize_url, normalize_text


class DuplicateStatus(StrEnum):
    DISTINCT = "distinct"
    EXACT_DUPLICATE = "exact_duplicate"
    POSSIBLE_DUPLICATE = "possible_duplicate"


@dataclass(frozen=True, slots=True)
class ArticleIdentity:
    source_id: str
    url: str
    title: str
    external_id: str | None = None
    content_fingerprint: str | None = None


@dataclass(frozen=True, slots=True)
class DuplicateResult:
    status: DuplicateStatus
    reason: str
    similarity: float = 0.0


def compare_articles(
    candidate: ArticleIdentity,
    existing: ArticleIdentity,
    *,
    possible_duplicate_threshold: float = 0.94,
) -> DuplicateResult:
    """Compare two articles conservatively; near matches require later review/grouping."""
    if not 0.0 <= possible_duplicate_threshold <= 1.0:
        raise ValueError("possible_duplicate_threshold must be between 0 and 1")

    if canonicalize_url(candidate.url) == canonicalize_url(existing.url):
        return DuplicateResult(DuplicateStatus.EXACT_DUPLICATE, "same_canonical_url", 1.0)

    if (
        candidate.external_id
        and existing.external_id
        and candidate.source_id == existing.source_id
        and candidate.external_id == existing.external_id
    ):
        return DuplicateResult(DuplicateStatus.EXACT_DUPLICATE, "same_source_external_id", 1.0)

    if (
        candidate.content_fingerprint
        and existing.content_fingerprint
        and candidate.content_fingerprint == existing.content_fingerprint
    ):
        return DuplicateResult(DuplicateStatus.EXACT_DUPLICATE, "same_content_fingerprint", 1.0)

    left = normalize_text(candidate.title)
    right = normalize_text(existing.title)
    if not left or not right:
        return DuplicateResult(DuplicateStatus.DISTINCT, "empty_title")

    similarity = SequenceMatcher(None, left, right, autojunk=False).ratio()
    if similarity >= possible_duplicate_threshold:
        return DuplicateResult(
    DuplicateStatus.POSSIBLE_DUPLICATE,
    "similar_title_review_required",
    similarity,
)


    return DuplicateResult(DuplicateStatus.DISTINCT, "no_duplicate_match", similarity)

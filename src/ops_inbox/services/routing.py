from __future__ import annotations

from dataclasses import dataclass

from src.ops_inbox.core.classifier import ClassificationResult
from src.ops_inbox.data.inbox_repository import InboxMessage

PRIORITY_BASE_SCORE = {
    "critical": 88,
    "high": 72,
    "medium": 48,
    "low": 24,
}

CATEGORY_WEIGHT = {
    "support_issue": 8,
    "complaint": 7,
    "billing": 5,
    "sales_lead": 3,
    "scheduling": 2,
    "account_management": 2,
    "vendor": 0,
}

SLA_BY_PRIORITY = {
    "critical": "Respond within 15 minutes",
    "high": "Respond within 2 business hours",
    "medium": "Respond by next business day",
    "low": "Review within 3 business days",
}


@dataclass(frozen=True)
class RoutingDecision:
    owner: str
    urgency_score: int
    sla: str
    reason: str
    needs_manager_review: bool


def build_routing_decision(
    message: InboxMessage,
    classification: ClassificationResult,
) -> RoutingDecision:
    score = _score(message, classification)
    owner = _owner(classification)
    manager_review = score >= 82 or classification.category == "complaint"

    return RoutingDecision(
        owner=owner,
        urgency_score=score,
        sla=SLA_BY_PRIORITY[classification.priority],
        reason=_reason(classification, score),
        needs_manager_review=manager_review,
    )


def _score(message: InboxMessage, classification: ClassificationResult) -> int:
    text = f"{message.subject} {message.body}".lower()
    score = PRIORITY_BASE_SCORE[classification.priority]
    score += CATEGORY_WEIGHT.get(classification.category, 0)

    if "today" in text or "immediately" in text:
        score += 5
    if "tomorrow" in text or "payment run" in text:
        score += 4
    if "manager" in text or "board review" in text:
        score += 4

    return max(0, min(score, 100))


def _owner(classification: ClassificationResult) -> str:
    if classification.category == "complaint" and classification.priority in {"critical", "high"}:
        return "Customer Success Manager"
    return classification.owner


def _reason(classification: ClassificationResult, score: int) -> str:
    category = classification.category.replace("_", " ")
    if score >= 85:
        return f"Immediate attention: {classification.priority} {category} with strong urgency signals."
    if score >= 70:
        return f"Prioritized for same-day handling: {classification.priority} {category}."
    if score >= 45:
        return f"Standard queue item: {classification.priority} {category}."
    return f"Low-risk queue item: {classification.priority} {category}."

from __future__ import annotations

import re
from dataclasses import dataclass

from src.ops_inbox.data.inbox_repository import InboxMessage

CATEGORY_RULES = {
    "support_issue": {
        "keywords": [
            "locked out",
            "stopped",
            "not working",
            "cannot access",
            "integration",
            "dashboard",
            "error",
            "engineer",
            "blocked",
        ],
        "owner": "Support Engineering",
    },
    "billing": {
        "keywords": [
            "invoice",
            "charge",
            "payment",
            "duplicate",
            "correct this",
            "amount",
            "billing",
        ],
        "owner": "Finance Ops",
    },
    "sales_lead": {
        "keywords": [
            "interested",
            "discuss",
            "available for a call",
            "automation",
            "found your",
            "locations",
        ],
        "owner": "Sales",
    },
    "scheduling": {
        "keywords": [
            "delivery",
            "schedule",
            "window",
            "slot",
            "friday",
            "thursday",
            "available",
        ],
        "owner": "Operations",
    },
    "vendor": {
        "keywords": [
            "vendor",
            "insurance certificate",
            "policy",
            "compliance",
            "renewed",
            "records",
        ],
        "owner": "Vendor Management",
    },
    "account_management": {
        "keywords": [
            "renewal",
            "contract",
            "pricing",
            "service levels",
            "add two more",
        ],
        "owner": "Account Management",
    },
    "complaint": {
        "keywords": [
            "complaint",
            "frustrating",
            "asked twice",
            "manager",
            "status update",
            "clear answer",
        ],
        "owner": "Customer Success",
    },
}

PRIORITY_RULES = {
    "critical": ["urgent", "immediately", "paused", "blocked", "production line"],
    "high": ["today", "tomorrow", "escalate", "board review", "payment run", "manager"],
    "medium": ["next week", "renewal", "confirm", "move", "question", "call"],
}


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    priority: str
    owner: str
    confidence: float
    matched_terms: tuple[str, ...]


def classify_message(message: InboxMessage) -> ClassificationResult:
    text = normalize_text(f"{message.subject} {message.body}")
    category, terms = _best_category(text)
    priority = _priority(text)
    confidence = _confidence(terms)

    return ClassificationResult(
        category=category,
        priority=priority,
        owner=CATEGORY_RULES[category]["owner"],
        confidence=confidence,
        matched_terms=tuple(terms),
    )


def classify_messages(messages: list[InboxMessage]) -> list[tuple[InboxMessage, ClassificationResult]]:
    return [(message, classify_message(message)) for message in messages]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def _best_category(text: str) -> tuple[str, list[str]]:
    scored = []
    for category, rule in CATEGORY_RULES.items():
        terms = [term for term in rule["keywords"] if term in text]
        scored.append((len(terms), category, terms))

    score, category, terms = max(scored, key=lambda item: (item[0], item[1]))
    if score == 0:
        return "support_issue", []
    return category, terms


def _priority(text: str) -> str:
    for priority, terms in PRIORITY_RULES.items():
        if any(term in text for term in terms):
            return priority
    return "low"


def _confidence(matched_terms: list[str]) -> float:
    if not matched_terms:
        return 0.35
    return min(0.95, round(0.45 + len(matched_terms) * 0.12, 2))

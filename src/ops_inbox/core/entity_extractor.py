from __future__ import annotations

import re
from dataclasses import dataclass

from src.ops_inbox.data.inbox_repository import InboxMessage

EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")
MONEY_PATTERN = re.compile(r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\$\s?\d+(?:\.\d{2})?")
INVOICE_PATTERN = re.compile(r"\b(?:INV|Invoice)[-\s]?\d{3,}\b", re.IGNORECASE)
OPERATION_ID_PATTERN = re.compile(r"\b[A-Z]{2,5}-\d{3,}\b")
DATE_WORD_PATTERN = re.compile(
    r"\b(?:today|tomorrow|next week|monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday|january|february|march|april|may|june|july|august|"
    r"september|october|november|december)\b(?:\s+\d{1,2})?",
    re.IGNORECASE,
)
TIME_PATTERN = re.compile(r"\b\d{1,2}(?::\d{2})?\s?(?:AM|PM)\b", re.IGNORECASE)


@dataclass(frozen=True)
class ExtractedEntities:
    emails: tuple[str, ...]
    phones: tuple[str, ...]
    money: tuple[str, ...]
    invoices: tuple[str, ...]
    operation_ids: tuple[str, ...]
    dates: tuple[str, ...]
    times: tuple[str, ...]

    @property
    def has_entities(self) -> bool:
        return any(
            [
                self.emails,
                self.phones,
                self.money,
                self.invoices,
                self.operation_ids,
                self.dates,
                self.times,
            ]
        )


def extract_entities(message: InboxMessage) -> ExtractedEntities:
    text = f"{message.sender_email} {message.subject} {message.body}"

    return ExtractedEntities(
        emails=_unique(EMAIL_PATTERN.findall(text)),
        phones=_unique(PHONE_PATTERN.findall(text)),
        money=_unique(_clean_money(value) for value in MONEY_PATTERN.findall(text)),
        invoices=_unique(value.upper().replace(" ", "-") for value in INVOICE_PATTERN.findall(text)),
        operation_ids=_unique(OPERATION_ID_PATTERN.findall(text)),
        dates=_unique(value.title() for value in DATE_WORD_PATTERN.findall(text)),
        times=_unique(value.upper().replace(" ", "") for value in TIME_PATTERN.findall(text)),
    )


def format_entities(entities: ExtractedEntities) -> list[str]:
    rows = [
        ("Email", entities.emails),
        ("Phone", entities.phones),
        ("Amount", entities.money),
        ("Invoice", entities.invoices),
        ("Ops ID", entities.operation_ids),
        ("Date", entities.dates),
        ("Time", entities.times),
    ]
    return [f"{label}: {', '.join(values)}" for label, values in rows if values]


def _unique(values) -> tuple[str, ...]:
    seen = []
    for value in values:
        clean = str(value).strip()
        if clean and clean not in seen:
            seen.append(clean)
    return tuple(seen)


def _clean_money(value: str) -> str:
    return re.sub(r"\s+", "", value)

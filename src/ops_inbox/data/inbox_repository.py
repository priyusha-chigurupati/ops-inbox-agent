from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.ops_inbox.config import DATA_DIR

SAMPLE_INBOX_PATH = DATA_DIR / "sample_inbox.json"
REQUIRED_FIELDS = {
    "id",
    "received_at",
    "sender_name",
    "sender_email",
    "sender_company",
    "subject",
    "body",
    "channel",
    "expected_category",
    "expected_priority",
}


@dataclass(frozen=True)
class InboxMessage:
    id: str
    received_at: datetime
    sender_name: str
    sender_email: str
    sender_company: str
    subject: str
    body: str
    channel: str
    expected_category: str
    expected_priority: str

    @property
    def preview(self) -> str:
        text = " ".join(self.body.split())
        return text if len(text) <= 140 else f"{text[:137]}..."


def load_sample_messages(path: Path = SAMPLE_INBOX_PATH) -> list[InboxMessage]:
    records = json.loads(path.read_text(encoding="utf-8"))
    return [parse_message(record) for record in records]


def parse_message(record: dict[str, str]) -> InboxMessage:
    missing = REQUIRED_FIELDS.difference(record)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Inbox record is missing required fields: {names}")

    return InboxMessage(
        id=record["id"],
        received_at=datetime.fromisoformat(record["received_at"]),
        sender_name=record["sender_name"],
        sender_email=record["sender_email"],
        sender_company=record["sender_company"],
        subject=record["subject"],
        body=record["body"],
        channel=record["channel"],
        expected_category=record["expected_category"],
        expected_priority=record["expected_priority"],
    )

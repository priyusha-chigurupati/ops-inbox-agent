from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO

from src.ops_inbox.core.classifier import classify_message
from src.ops_inbox.core.entity_extractor import extract_entities, format_entities
from src.ops_inbox.data.inbox_repository import InboxMessage
from src.ops_inbox.services.reply_drafts import build_reply_draft
from src.ops_inbox.services.routing import build_routing_decision


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    message_id: str
    subject: str
    category: str
    priority: str
    owner: str
    urgency_score: int
    sla: str
    next_step: str
    entities: str
    status: str = "Needs review"


def build_task_queue(messages: list[InboxMessage]) -> list[TaskRecord]:
    return [build_task_record(message) for message in messages]


def build_task_record(message: InboxMessage) -> TaskRecord:
    classification = classify_message(message)
    entities = extract_entities(message)
    routing = build_routing_decision(message, classification)
    draft = build_reply_draft(message, classification, entities, routing)

    return TaskRecord(
        task_id=f"task-{message.id.removeprefix('msg-')}",
        message_id=message.id,
        subject=message.subject,
        category=classification.category,
        priority=classification.priority,
        owner=routing.owner,
        urgency_score=routing.urgency_score,
        sla=routing.sla,
        next_step=draft.next_step,
        entities=" | ".join(format_entities(entities)),
    )


def task_queue_to_csv(tasks: list[TaskRecord]) -> str:
    output = StringIO()
    fieldnames = [
        "task_id",
        "message_id",
        "subject",
        "category",
        "priority",
        "owner",
        "urgency_score",
        "sla",
        "next_step",
        "entities",
        "status",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for task in tasks:
        writer.writerow({field: getattr(task, field) for field in fieldnames})
    return output.getvalue()

from __future__ import annotations

from dataclasses import dataclass

from src.ops_inbox.core.classifier import ClassificationResult
from src.ops_inbox.core.entity_extractor import ExtractedEntities
from src.ops_inbox.data.inbox_repository import InboxMessage
from src.ops_inbox.services.routing import RoutingDecision


@dataclass(frozen=True)
class ReplyDraft:
    subject: str
    body: str
    tone: str
    next_step: str


def build_reply_draft(
    message: InboxMessage,
    classification: ClassificationResult,
    entities: ExtractedEntities,
    routing: RoutingDecision,
) -> ReplyDraft:
    builder = {
        "billing": _billing_reply,
        "support_issue": _support_reply,
        "sales_lead": _sales_reply,
        "scheduling": _scheduling_reply,
        "vendor": _vendor_reply,
        "account_management": _account_reply,
        "complaint": _complaint_reply,
    }.get(classification.category, _general_reply)

    return builder(message, entities, routing)


def _billing_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    invoice = _first(entities.invoices, "the invoice")
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Clear and accountable",
        next_step="Finance Ops should verify the invoice and send the corrected amount.",
        body=(
            f"Hi {message.sender_name},\n\n"
            f"Thanks for flagging {invoice}. We are reviewing the charge details now and will "
            f"confirm the corrected invoice before your payment run.\n\n"
            f"Our target is to follow up based on this SLA: {routing.sla}.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _support_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    ref = _first(entities.operation_ids, "the affected workflow")
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Urgent and reassuring",
        next_step="Support Engineering should acknowledge, investigate, and post the next update.",
        body=(
            f"Hi {message.sender_name},\n\n"
            f"We received this and are routing it to Support Engineering now. We will investigate "
            f"{ref} and send the next update under this SLA: {routing.sla}.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _sales_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Helpful and consultative",
        next_step="Sales should qualify fit, timing, volume, and decision process.",
        body=(
            f"Hi {message.sender_name},\n\n"
            "Thanks for reaching out. We would be glad to learn more about your current workflow "
            "and where automation could reduce manual effort. Please send a few times that work "
            "next week, and we can schedule a short discovery call.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _scheduling_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    phone = _first(entities.phones, "the phone number on file")
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Practical and concise",
        next_step="Operations should confirm the revised delivery window.",
        body=(
            f"Hi {message.sender_name},\n\n"
            "Thanks for the update. We are checking the delivery options and will confirm whether "
            f"Friday morning or an earlier Thursday slot is available. If needed, we will call {phone}.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _vendor_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Brief and organized",
        next_step="Vendor Management should save the document and confirm compliance status.",
        body=(
            f"Hi {message.sender_name},\n\n"
            "Thanks for sending the updated certificate. We will add it to the vendor record and "
            "let you know if compliance needs any additional information.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _account_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Account-focused",
        next_step="Account Management should confirm pricing and expansion terms.",
        body=(
            f"Hi {message.sender_name},\n\n"
            "Thanks for checking in on the renewal. We are reviewing current pricing and service "
            "levels for the added locations and will send a clear summary for your team.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _complaint_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Empathetic and accountable",
        next_step="Customer Success Manager should respond with ownership and a timeline.",
        body=(
            f"Hi {message.sender_name},\n\n"
            "I am sorry for the missed follow-up. We are escalating this to a manager and will "
            "send you a clear status update and timeline today.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _general_reply(message: InboxMessage, entities: ExtractedEntities, routing: RoutingDecision) -> ReplyDraft:
    return ReplyDraft(
        subject=f"Re: {message.subject}",
        tone="Neutral and helpful",
        next_step="Review the request and assign the best owner.",
        body=(
            f"Hi {message.sender_name},\n\n"
            "Thanks for the note. We are reviewing the request and will route it to the right team "
            f"for follow-up. Target response: {routing.sla}.\n\n"
            "Best,\nOperations Team"
        ),
    )


def _first(values: tuple[str, ...], fallback: str) -> str:
    return values[0] if values else fallback

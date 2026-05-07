import unittest

from src.ops_inbox.core.classifier import classify_message
from src.ops_inbox.core.entity_extractor import extract_entities
from src.ops_inbox.data.inbox_repository import load_sample_messages
from src.ops_inbox.services.reply_drafts import build_reply_draft
from src.ops_inbox.services.routing import build_routing_decision


class ReplyDraftTest(unittest.TestCase):
    def test_billing_reply_mentions_invoice_and_payment_run_timing(self) -> None:
        draft = _draft_for(1)

        self.assertIn("INV-4481", draft.body)
        self.assertIn("payment run", draft.body)
        self.assertEqual(draft.tone, "Clear and accountable")

    def test_support_reply_mentions_operational_reference(self) -> None:
        draft = _draft_for(3)

        self.assertIn("PKG-88420", draft.body)
        self.assertIn("Support Engineering", draft.next_step)

    def test_complaint_reply_is_manager_oriented(self) -> None:
        draft = _draft_for(7)

        self.assertIn("sorry", draft.body.lower())
        self.assertIn("manager", draft.body.lower())
        self.assertEqual(draft.tone, "Empathetic and accountable")

    def test_each_sample_message_gets_a_reply_subject_and_body(self) -> None:
        for index, _message in enumerate(load_sample_messages()):
            draft = _draft_for(index)

            self.assertTrue(draft.subject.startswith("Re:"))
            self.assertGreater(len(draft.body), 80)
            self.assertGreater(len(draft.next_step), 20)


def _draft_for(index: int):
    message = load_sample_messages()[index]
    classification = classify_message(message)
    entities = extract_entities(message)
    routing = build_routing_decision(message, classification)
    return build_reply_draft(message, classification, entities, routing)

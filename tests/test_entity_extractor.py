import unittest

from src.ops_inbox.core.entity_extractor import extract_entities, format_entities
from src.ops_inbox.data.inbox_repository import load_sample_messages


class EntityExtractorTest(unittest.TestCase):
    def test_extracts_sender_email_from_each_message(self) -> None:
        messages = load_sample_messages()

        for message in messages:
            entities = extract_entities(message)
            self.assertIn(message.sender_email, entities.emails)

    def test_extracts_phone_number_from_scheduling_message(self) -> None:
        message = load_sample_messages()[0]
        entities = extract_entities(message)

        self.assertIn("918-555-0142", entities.phones)

    def test_extracts_invoice_and_amounts_from_billing_message(self) -> None:
        message = load_sample_messages()[1]
        entities = extract_entities(message)

        self.assertIn("INV-4481", entities.invoices)
        self.assertIn("$2,400", entities.money)
        self.assertIn("$4,800", entities.money)

    def test_extracts_operation_id_from_urgent_support_message(self) -> None:
        message = load_sample_messages()[3]
        entities = extract_entities(message)

        self.assertIn("PKG-88420", entities.operation_ids)

    def test_format_entities_hides_empty_sections(self) -> None:
        message = load_sample_messages()[1]
        rows = format_entities(extract_entities(message))

        self.assertTrue(any(row.startswith("Email:") for row in rows))
        self.assertTrue(any(row.startswith("Invoice:") for row in rows))
        self.assertFalse(any(row.startswith("Phone:") for row in rows))

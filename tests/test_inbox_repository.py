import unittest
from datetime import datetime

from src.ops_inbox.data.inbox_repository import load_sample_messages, parse_message


class InboxRepositoryTest(unittest.TestCase):
    def test_load_sample_messages_returns_realistic_records(self) -> None:
        messages = load_sample_messages()

        self.assertGreaterEqual(len(messages), 8)
        self.assertTrue(all(message.id.startswith("msg-") for message in messages))
        self.assertTrue(all(len(message.body) > 80 for message in messages))

    def test_sample_messages_cover_core_business_categories(self) -> None:
        categories = {message.expected_category for message in load_sample_messages()}

        self.assertIn("support_issue", categories)
        self.assertIn("billing", categories)
        self.assertIn("sales_lead", categories)
        self.assertIn("complaint", categories)
        self.assertIn("scheduling", categories)

    def test_parse_message_rejects_missing_required_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "sender_email"):
            parse_message({"id": "msg-bad"})

    def test_preview_is_short_and_readable(self) -> None:
        message = load_sample_messages()[0]

        self.assertLessEqual(len(message.preview), 140)
        self.assertNotIn("\n", message.preview)

    def test_received_at_is_parsed_as_datetime(self) -> None:
        message = load_sample_messages()[0]

        self.assertIsInstance(message.received_at, datetime)

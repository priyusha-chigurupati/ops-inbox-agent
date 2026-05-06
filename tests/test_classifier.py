import unittest

from src.ops_inbox.core.classifier import classify_message, classify_messages, normalize_text
from src.ops_inbox.data.inbox_repository import load_sample_messages


class ClassifierTest(unittest.TestCase):
    def test_classifier_matches_expected_categories_for_sample_data(self) -> None:
        results = classify_messages(load_sample_messages())

        mismatches = [
            (message.id, message.expected_category, result.category)
            for message, result in results
            if message.expected_category != result.category
        ]
        self.assertEqual(mismatches, [])

    def test_classifier_matches_expected_priorities_for_sample_data(self) -> None:
        results = classify_messages(load_sample_messages())

        mismatches = [
            (message.id, message.expected_priority, result.priority)
            for message, result in results
            if message.expected_priority != result.priority
        ]
        self.assertEqual(mismatches, [])

    def test_classification_result_includes_owner_and_reasoning_terms(self) -> None:
        message = load_sample_messages()[1]
        result = classify_message(message)

        self.assertEqual(result.owner, "Finance Ops")
        self.assertGreaterEqual(result.confidence, 0.5)
        self.assertIn("invoice", result.matched_terms)

    def test_normalize_text_removes_extra_spacing_and_case_noise(self) -> None:
        self.assertEqual(normalize_text("  URGENT\n\nNeed   Help "), "urgent need help")

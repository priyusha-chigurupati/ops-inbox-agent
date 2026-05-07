import unittest

from src.ops_inbox.core.classifier import classify_message
from src.ops_inbox.data.inbox_repository import load_sample_messages
from src.ops_inbox.services.routing import build_routing_decision


class RoutingTest(unittest.TestCase):
    def test_critical_support_issue_receives_fast_sla(self) -> None:
        message = load_sample_messages()[3]
        decision = build_routing_decision(message, classify_message(message))

        self.assertGreaterEqual(decision.urgency_score, 90)
        self.assertEqual(decision.sla, "Respond within 15 minutes")
        self.assertTrue(decision.needs_manager_review)

    def test_complaint_routes_to_customer_success_manager(self) -> None:
        message = load_sample_messages()[7]
        decision = build_routing_decision(message, classify_message(message))

        self.assertEqual(decision.owner, "Customer Success Manager")
        self.assertTrue(decision.needs_manager_review)

    def test_vendor_message_stays_low_urgency(self) -> None:
        message = load_sample_messages()[4]
        decision = build_routing_decision(message, classify_message(message))

        self.assertLess(decision.urgency_score, 40)
        self.assertEqual(decision.sla, "Review within 3 business days")
        self.assertFalse(decision.needs_manager_review)

    def test_billing_payment_run_gets_same_day_reason(self) -> None:
        message = load_sample_messages()[1]
        decision = build_routing_decision(message, classify_message(message))

        self.assertGreaterEqual(decision.urgency_score, 80)
        self.assertIn("same-day", decision.reason)

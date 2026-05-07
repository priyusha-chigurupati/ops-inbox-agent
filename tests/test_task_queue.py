import csv
import unittest
from io import StringIO

from src.ops_inbox.data.inbox_repository import load_sample_messages
from src.ops_inbox.services.task_queue import build_task_queue, task_queue_to_csv


class TaskQueueTest(unittest.TestCase):
    def test_build_task_queue_creates_one_task_per_message(self) -> None:
        messages = load_sample_messages()
        tasks = build_task_queue(messages)

        self.assertEqual(len(tasks), len(messages))
        self.assertTrue(all(task.status == "Needs review" for task in tasks))

    def test_task_records_include_routing_and_next_step(self) -> None:
        task = build_task_queue(load_sample_messages())[1]

        self.assertEqual(task.owner, "Finance Ops")
        self.assertGreaterEqual(task.urgency_score, 80)
        self.assertIn("Finance Ops", task.next_step)
        self.assertIn("Invoice: INV-4481", task.entities)

    def test_task_queue_csv_contains_expected_columns_and_rows(self) -> None:
        tasks = build_task_queue(load_sample_messages())
        csv_text = task_queue_to_csv(tasks)
        rows = list(csv.DictReader(StringIO(csv_text)))

        self.assertEqual(len(rows), len(tasks))
        self.assertEqual(rows[0]["task_id"], "task-1001")
        self.assertIn("urgency_score", rows[0])
        self.assertIn("next_step", rows[0])

    def test_csv_export_escapes_commas_in_entity_values(self) -> None:
        csv_text = task_queue_to_csv(build_task_queue(load_sample_messages()))

        self.assertIn('"Email: eric.patel@ridgewaylabs.com | Amount: $2,400, $4,800', csv_text)

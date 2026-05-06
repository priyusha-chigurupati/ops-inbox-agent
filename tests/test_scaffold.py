from pathlib import Path
import unittest

from src.ops_inbox import __version__
from src.ops_inbox.config import APP_NAME, DATA_DIR


class ScaffoldTest(unittest.TestCase):
    def test_project_metadata_is_available(self) -> None:
        self.assertEqual(APP_NAME, "Ops Inbox Agent")
        self.assertEqual(__version__, "0.1.0")

    def test_expected_project_folders_exist(self) -> None:
        root = Path(__file__).resolve().parents[1]
        expected = [
            root / "src" / "ops_inbox" / "core",
            root / "src" / "ops_inbox" / "data",
            root / "src" / "ops_inbox" / "services",
            root / "src" / "ops_inbox" / "ui",
            root / "tests",
            DATA_DIR,
        ]
        self.assertTrue(all(path.exists() for path in expected))


if __name__ == "__main__":
    unittest.main()

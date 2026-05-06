from pathlib import Path

APP_NAME = "Ops Inbox Agent"
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
DATABASE_PATH = DATA_DIR / "app.db"

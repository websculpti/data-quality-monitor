import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")

REPORT_DIR = BASE_DIR / os.getenv("REPORT_DIR", "reports")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


DATA_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR.mkdir(parents=True, exist_ok=True)
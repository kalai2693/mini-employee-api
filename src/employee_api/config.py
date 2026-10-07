from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = Path(os.getenv("DATA_FILE", "data/employees.json"))
if not DATA_FILE.is_absolute():
    DATA_FILE = BASE_DIR / DATA_FILE
EXTERNAL_API_URL = os.getenvEXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com/users")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "change-me")

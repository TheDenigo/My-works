import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

env_path = BASE_DIR / "API_ID_Key.env"
if not env_path.exists():
    raise FileNotFoundError(f"❌ Конфигурационный файл .env не найден: {env_path}")
load_dotenv(env_path, override=True)

VK_TOKEN = os.getenv("VK_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID") or 0)

if not VK_TOKEN:
    raise ValueError("❌ VK_TOKEN отсутствует в .env")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN отсутствует в .env")
if not GROUP_ID:
    raise ValueError("❌ GROUP_ID отсутствует в .env")

GOOGLE_SHEETS_CREDENTIALS = str(BASE_DIR / os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json"))
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "Bot Users")

GIFT_TYPE = os.getenv("GIFT_TYPE", "promo_code")
PROMO_CODE = os.getenv("PROMO_CODE", "DEFAULT-CODE")
GIFT_IMAGE_PATH = str(BASE_DIR / os.getenv("GIFT_IMAGE_PATH", ""))
GIFT_FILE_PATH = str(BASE_DIR / os.getenv("GIFT_FILE_PATH", ""))

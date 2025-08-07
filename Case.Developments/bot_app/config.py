import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ----------------------------
# 1) Определяем BASE_DIR один раз, чтобы всё лежало рядом:
if getattr(sys, "frozen", False):
    # Если упаковали в .exe → BASE_DIR = папка с исполняемым файлом
    BASE_DIR = Path(sys.executable).parent
else:
    # Если запускаем .py напрямую → BASE_DIR = папка с этим файлом
    BASE_DIR = Path(__file__).resolve().parent

# 2) Полный путь к .env-файлу (API_ID_Key.env):
env_path = BASE_DIR / "API_ID_Key.env"
if not env_path.exists():
    raise FileNotFoundError(f"❌ Файл конфигурации не найден: {env_path}")
load_dotenv(env_path, override=True)

# 3) Основные настройки из .env:
VK_TOKEN = os.getenv("VK_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID") or 0)

if not VK_TOKEN:
    raise ValueError("❌ VK_TOKEN не найден в API_ID_Key.env")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не найден в API_ID_Key.env")
if not GROUP_ID:
    raise ValueError("❌ GROUP_ID не найден в API_ID_Key.env")

# 4) Google Sheets:
GOOGLE_SHEETS_CREDENTIALS = str(
    BASE_DIR / os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")
)
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "Bot Users")

# 5) Настройки подарков:
GIFT_TYPE = os.getenv("GIFT_TYPE", "promo_code")
PROMO_CODE = os.getenv("PROMO_CODE", "DEFAULT-CODE")
GIFT_IMAGE_PATH = str(BASE_DIR / os.getenv("GIFT_IMAGE_PATH", ""))  # для "image"
GIFT_FILE_PATH = str(BASE_DIR / os.getenv("GIFT_FILE_PATH", ""))    # для "file"

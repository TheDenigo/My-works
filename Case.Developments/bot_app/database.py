import sqlite3
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS, SPREADSHEET_NAME

class Database:
    def __init__(self):
        # --- Часть 1: Google Sheets ---
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                GOOGLE_SHEETS_CREDENTIALS, scope
            )
            client = gspread.authorize(creds)
            self.sheet = client.open(SPREADSHEET_NAME).sheet1
        except Exception as e:
            raise RuntimeError(f"[DB ERROR] Ошибка подключения к Google Sheets: {e}")

        # --- Часть 2: SQLite (vk_log.db) ---
        # Файл создаётся в том же каталоге, что и этот скрипт:
        db_path = Path(__file__).resolve().parent / "vk_log.db"
        try:
            self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise RuntimeError(f"[DB ERROR] Не удалось открыть {db_path}: {e}")

        self._create_tables()

    def _create_tables(self):
        # vk_actions — чтобы логировать каждую реакцию (лайк/репост),
        # vk_sent_users — чтобы хранить, кому уже отправили приглашение
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vk_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vk_sent_users (
                user_id TEXT PRIMARY KEY
            )
            """
        )
        self.conn.commit()

    def check_user(self, user_id):
        """Проверить, есть ли user_id в Google Sheets (Telegram часть)."""
        try:
            return self.sheet.find(str(user_id)) is not None
        except Exception:
            return False

    def add_user(self, user_id, name, email, phone):
        """Добавить нового пользователя в Google Sheets."""
        try:
            self.sheet.append_row([user_id, name, email, phone, "Нет"])
        except Exception as e:
            print(f"[DB ERROR] Не удалось добавить пользователя в Google Sheets: {e}")

    def log_vk_action(self, user_id, action_type):
        """Занести лайк/репост в таблицу vk_actions (для статистики)."""
        try:
            self.cursor.execute(
                "INSERT INTO vk_actions (user_id, action_type) VALUES (?, ?)",
                (str(user_id), action_type),
            )
            self.conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Не удалось записать действие VK: {e}")

    def mark_user_invited(self, user_id):
        """Пометить в SQLite, что VK-приглашение уже отправлено (таблица vk_sent_users)."""
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO vk_sent_users (user_id) VALUES (?)",
                (str(user_id),),
            )
            self.conn.commit()
        except Exception as e:
            print(f"[DB ERROR] mark_user_invited: {e}")

    def was_user_invited(self, user_id):
        """Проверить, отправляли ли уже приглашение этому user_id."""
        try:
            self.cursor.execute(
                "SELECT 1 FROM vk_sent_users WHERE user_id = ? LIMIT 1",
                (str(user_id),),
            )
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"[DB ERROR] was_user_invited: {e}")
            return False

    def mark_gift_sent(self, user_id):
        """Отметить в Google Sheets, что подарок уже выдан (пятый столбец = 'да')."""
        try:
            values = self.sheet.get_all_values()
            for i, row in enumerate(values):
                if row and str(row[0]) == str(user_id):
                    # update_cell: i+1, 5 — индекс строки и номер столбца
                    self.sheet.update_cell(i + 1, 5, "да")
                    break
        except Exception as e:
            print(f"[DB ERROR] mark_gift_sent: {e}")

    def delete_user(self, user_id):
        """
        Удалить пользователя user_id из двух мест:
         1) SQLite (vk_sent_users) — чтобы VK-бот мог снова отправить приглашение.
         2) Google Sheets — полностью стираем строку [user_id, name, email, phone, gift_sent].
        """
        # SQLite
        try:
            self.cursor.execute(
                "DELETE FROM vk_sent_users WHERE user_id = ?", (str(user_id),)
            )
            self.conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Не удалось удалить из vk_sent_users: {e}")

        # Google Sheets
        try:
            values = self.sheet.get_all_values()
            for i, row in enumerate(values):
                if row and str(row[0]) == str(user_id):
                    self.sheet.delete_row(i + 1)
                    break
        except Exception as e:
            print(f"[DB ERROR] Ошибка при удалении из Google Sheets: {e}")

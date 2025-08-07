import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS
import sqlite3
import os

class Database:
    def __init__(self):
        # Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open("Bot Users").sheet1

        # SQLite
        self.db_path = "vk_log.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vk_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def check_user(self, user_id):
        try:
            return self.sheet.find(str(user_id)) is not None
        except:
            return False

    def add_user(self, user_id, name, email, phone):
        self.sheet.append_row([user_id, name, email, phone, "Нет"])

    def log_vk_action(self, user_id, action_type):
        try:
            self.cursor.execute(
                "INSERT INTO vk_actions (user_id, action_type) VALUES (?, ?)",
                (str(user_id), action_type)
            )
            self.conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Не удалось записать действие VK: {e}")

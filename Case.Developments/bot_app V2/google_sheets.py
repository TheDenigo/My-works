import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS, SPREADSHEET_NAME

class GoogleSheetsHelper:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(SPREADSHEET_NAME).sheet1

    def is_user_recorded(self, user_id):
        users = self.sheet.col_values(1)
        return str(user_id) in users

    def record_user(self, user_id, username, platform):
        if not self.is_user_recorded(user_id):
            self.sheet.append_row([str(user_id), username, platform, "✅"])

    def remove_user(self, user_id):
        users = self.sheet.col_values(1)
        if str(user_id) in users:
            row = users.index(str(user_id)) + 1
            self.sheet.delete_rows(row)

    def get_all_users(self):
        return self.sheet.get_all_records()

    def mark_gift_sent(self, user_id):
        users = self.sheet.col_values(1)
        if str(user_id) in users:
            row = users.index(str(user_id)) + 1
            self.sheet.update_cell(row, 4, "✅")

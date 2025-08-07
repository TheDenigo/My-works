import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from database import Database
import threading

from main import start_bot, stop_bot

# Настройка логирования в файл
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
from datetime import datetime
now = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(LOG_DIR, f"{now}.txt")
fh = logging.FileHandler(log_path, encoding="utf-8")
fh.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "%Y-%m-%d %H:%M:%S"
))
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(fh)


class TextHandler(logging.Handler):
    def __init__(self, text_widget: ScrolledText):
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter("%(asctime)s - %(message)s", "%H:%M:%S"))

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, self._append, msg)

    def _append(self, msg: str):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.yview(tk.END)


def open_env_editor(parent, log_widget, env_path):
    def save():
        content = editor.get("1.0", tk.END).strip()
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content)
        load_dotenv(env_path, override=True)
        log_widget.configure(state=tk.NORMAL)
        log_widget.insert(
            tk.END, f"✅ Конфигурация обновлена из {os.path.basename(env_path)}\n"
        )
        log_widget.configure(state=tk.DISABLED)
        log_widget.yview(tk.END)
        win.destroy()

    win = tk.Toplevel(parent)
    win.title("Редактировать .env")
    win.geometry("500x400")

    editor = tk.Text(win, font=("Consolas", 10))
    editor.pack(fill=tk.BOTH, expand=True)
    try:
        with open(env_path, encoding="utf-8") as f:
            editor.insert(tk.END, f.read())
    except FileNotFoundError:
        editor.insert(tk.END, "# Файл не найден")

    tk.Button(win, text="💾 Сохранить", command=save).pack(pady=5)


def open_sheet_viewer(parent):
    from tkinter import Toplevel, Listbox, Scrollbar

    win = Toplevel(parent)
    win.title("Просмотр пользователей (Google Sheets)")
    win.geometry("500x400")

    scrollbar = Scrollbar(win)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(win, yscrollcommand=scrollbar.set, font=("Consolas", 10))
    listbox.pack(fill=tk.BOTH, expand=True)

    try:
        db = Database()
        data = db.sheet.get_all_values()
        if len(data) > 1:
            listbox.insert(tk.END, "user_id | name | gift_sent")
            listbox.insert(tk.END, "-" * 40)
            for row in data[1:]:
                listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[4]}")
        else:
            listbox.insert(tk.END, "Google Sheets пуста")
    except Exception as e:
        listbox.insert(tk.END, f"Ошибка: {e}")

    scrollbar.config(command=listbox.yview)


def open_vk_log_viewer(parent):
    from tkinter import Toplevel, Listbox, Scrollbar

    win = Toplevel(parent)
    win.title("Список приглашённых (vk_sent_users)")
    win.geometry("400x300")

    scrollbar = Scrollbar(win)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(win, yscrollcommand=scrollbar.set, font=("Consolas", 10))
    listbox.pack(fill=tk.BOTH, expand=True)

    try:
        db = Database()
        rows = db.cursor.execute("SELECT user_id FROM vk_sent_users").fetchall()
        if rows:
            listbox.insert(tk.END, "user_id (получил VK-приглашение)")
            listbox.insert(tk.END, "-" * 40)
            for (uid,) in rows:
                listbox.insert(tk.END, uid)
        else:
            listbox.insert(tk.END, "vk_sent_users пуста")
    except Exception as e:
        listbox.insert(tk.END, f"Ошибка: {e}")

    scrollbar.config(command=listbox.yview)


class BotApp:
    def __init__(self, root):
        self.root = root
        root.title("VK + Telegram Бот")
        root.geometry("650x550")

        # Лог-окно
        self.log_area = ScrolledText(root, height=20, font=("Consolas", 10))
        self.log_area.pack(fill=tk.BOTH, padx=5, pady=(5, 10), expand=True)
        self.log_area.insert(tk.END, "✅ Готов к запуску…\n")
        self.log_area.configure(state=tk.DISABLED)

        # Подключаем логгер
        handler = TextHandler(self.log_area)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        for lib in ("httpx", "telegram.ext", "vk_api"):
            logging.getLogger(lib).addHandler(handler)
            logging.getLogger(lib).propagate = True

        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=(0, 10), fill=tk.X)

        self.start_btn = tk.Button(
            btn_frame, text="▶ Запустить бота", width=20, command=self.start_bot
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ Остановить бота",
            width=20,
            command=self.stop_bot,
            state=tk.DISABLED,
        )
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="⚙ Настройки (.env)",
            width=20,
            command=lambda: open_env_editor(
                root, self.log_area, Path().resolve() / "API_ID_Key.env"
            ),
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="📋 Показать Google Sheets",
            width=20,
            command=lambda: open_sheet_viewer(root),
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="🗂 Показать VK-лог (sqlite)",
            width=20,
            command=lambda: open_vk_log_viewer(root),
        ).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(btn_frame, text="").grid(row=1, column=2, padx=5, pady=5)

        # Удаление пользователя
        del_frame = tk.Frame(root)
        del_frame.pack(fill=tk.X, padx=5)
        tk.Label(del_frame, text="Удалить пользователя по ID:").grid(
            row=0, column=0, sticky=tk.W
        )
        self.delete_entry = tk.Entry(del_frame, width=25)
        self.delete_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            del_frame, text="❌ Удалить из базы", command=self.delete_user_by_id
        ).grid(row=0, column=2, padx=5, pady=5)

    def start_bot(self):
        self._log("🚀 Запуск ботов…")
        threading.Thread(target=start_bot, name="BotStartThread", daemon=True).start()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

    def stop_bot(self):
        self._log("⏹ Остановка ботов…")
        threading.Thread(target=stop_bot, name="BotStopThread", daemon=True).start()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)


    def delete_user_by_id(self):
        user_id = self.delete_entry.get().strip()
        if user_id:
            try:
                db = Database()
                db.delete_user(user_id)
                self._log(f"✅ Удалён пользователь {user_id} из базы")
            except Exception as e:
                self._log(f"⚠ Ошибка при удалении {user_id}: {e}")
        else:
            self._log("⚠ Введите user_id для удаления")

    def _log(self, message: str):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.configure(state=tk.DISABLED)
        self.log_area.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BotApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import multiprocessing
import logging
import sys
import os
import signal
from vk_bot import run_vk_bot
from telegram_bot import run_telegram_bot
from google_sheets import GoogleSheetsClient

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Глобальные процессы
vk_process = None
tg_process = None
sheets_client = GoogleSheetsClient()

def start_bots():
    global vk_process, tg_process
    if vk_process or tg_process:
        log("⚠️ Боты уже запущены.")
        return
    log("▶️ Запуск ботов...")
    vk_process = multiprocessing.Process(target=run_vk_bot)
    tg_process = multiprocessing.Process(target=run_telegram_bot)
    vk_process.start()
    tg_process.start()
    log("✅ Боты запущены!")

def stop_bots():
    global vk_process, tg_process
    log("⛔ Остановка ботов...")
    for process in [vk_process, tg_process]:
        if process and process.is_alive():
            os.kill(process.pid, signal.SIGTERM)
            process.join(timeout=5)
            if process.is_alive():
                process.terminate()
    vk_process = None
    tg_process = None
    log("✅ Боты остановлены.")

def log(message):
    log_text.insert(tk.END, f"{message}\n")
    log_text.see(tk.END)

def on_closing():
    if messagebox.askokcancel("Выход", "Остановить ботов и выйти?"):
        stop_bots()
        root.destroy()

def delete_user():
    user_id = simpledialog.askstring("Удаление пользователя", "Введите user_id для удаления:")
    if user_id:
        success = sheets_client.delete_user(user_id)
        if success:
            log(f"🗑️ Пользователь {user_id} удалён из таблицы.")
        else:
            log(f"⚠️ Пользователь {user_id} не найден или ошибка удаления.")

# Создание GUI
root = tk.Tk()
root.title("🎁 Бот-подарочник")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_start = tk.Button(frame, text="▶️ Запустить ботов", width=30, command=start_bots)
btn_start.grid(row=0, column=0, padx=5, pady=5)

btn_stop = tk.Button(frame, text="⛔ Остановить ботов", width=30, command=stop_bots)
btn_stop.grid(row=1, column=0, padx=5, pady=5)

btn_delete = tk.Button(frame, text="🗑️ Удалить пользователя", width=30, command=delete_user)
btn_delete.grid(row=2, column=0, padx=5, pady=5)

log_text = scrolledtext.ScrolledText(root, width=60, height=20, state='normal')
log_text.pack(padx=10, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

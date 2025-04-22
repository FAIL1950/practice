import requests
import os
import json
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from libs.context import ProcessingContextManager

BOT_TOKEN = '7693452682:AAEMbLLbkVbwBqDZnDfNcMlaHXPUtJpaaUU'
API_URL_1 = 'https://0a1a-178-215-166-252.ngrok-free.app/api/v1/get_summary'
API_URL_2 = 'https://0a1a-178-215-166-252.ngrok-free.app/api/v1/get_contents_and_theses'

# user_id -> selected_endpoint
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Оберіть одну з команд для аналізу:\n"
        "1) /get_summary — Сформувати короткий підсумок документа\n"
        "2) /get_contents_and_theses — Побудувати зміст документа і вибирати тези або цитати\n\n"
        "Після вибору, надішліть файл у форматі .txt"
    )

async def get_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = API_URL_1
    await update.message.reply_text("Ви обрали 'Сформувати короткий підсумок документа'. Надішліть .txt файл.")

async def get_contents_and_theses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = API_URL_2
    await update.message.reply_text("Ви обрали 'Побудувати зміст документа і вибирати тези або цитати'. Надішліть .txt файл.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    api_url = user_states.get(user_id)

    if not api_url:
        await update.message.reply_text("Спочатку виконайте команду /get_summary або /get_contents_and_theses.")
        return

    doc = update.message.document
    if not doc or not doc.file_name.lower().endswith('.txt'):
        await update.message.reply_text("Підтримується лише формат .txt. Будь ласка, надішліть .txt файл.")
        return

    await update.message.reply_text("Аналіз в процесі...")

    file = await context.bot.get_file(doc.file_id)

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, doc.file_name)

    await file.download_to_drive(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    try:
        response = requests.post(api_url, json={"text": text_content})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Сталася помилка при обробці документа: {e}")
        return

    try:
        result_json = response.json()
        result_text = result_json.get("summary") or result_json.get("contents_and_theses") or "Не вдалося отримати результат."
    except json.JSONDecodeError:
        result_text = "Не вдалося розпізнати відповідь сервера."

    user_states[user_id] = None
    await update.message.reply_text(f"Результат аналізу:\n\n{result_text}")


if __name__ == '__main__':
    with ProcessingContextManager() as ctx:
        ctx.another_log_msg("Telegram bot starting...")
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("get_summary", get_summary))
        app.add_handler(CommandHandler("get_contents_and_theses", get_contents_and_theses))
        app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        app.run_polling()
        ctx.another_log_msg("Telegram bot successfully started.")

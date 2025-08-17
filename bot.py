import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю!")

app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
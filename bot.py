import os
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ AVIATOR PREDICTION BOT\n\n"
        "Tap /signal for the next signal."
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    low = round(random.uniform(1.20, 3.50), 2)
    high = round(random.uniform(low + 0.50, low + 3.00), 2)

    await update.message.reply_text(
        "✈️ AVIATOR PREDICTION\n\n"
        f"🎯 NEXT ROUND SIGNAL: {low:.2f}x – {high:.2f}x"
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    app.run_polling()


if __name__ == "__main__":
    main()

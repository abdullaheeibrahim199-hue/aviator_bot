import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Aviator Signal Bot is online!\n\n"
        "Tap /signal for a signal."
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Generates an illustrative statistical-style signal.
    # It does NOT know the actual next Aviator result.
    low = round(random.uniform(1.20, 1.80), 2)
    high = round(random.uniform(2.00, 3.50), 2)

    if high <= low:
        high = round(low + 0.80, 2)

    confidence = random.choice(["MEDIUM", "MEDIUM", "HIGH"])

    message = (
        "✈️ AVIATOR SIGNAL\n\n"
        "🟢 GREEN SIGNAL\n"
        f"🎯 TARGET: {low:.2f}x – {high:.2f}x\n"
        f"📊 CONFIDENCE: {confidence}\n\n"
        "⚠️ This is an estimate only. "
        "It cannot know or guarantee the next RNG result."
    )

    await update.message.reply_text(message)

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

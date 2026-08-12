import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Aviator Signal Bot is online!\n\n"
        "Use /signal for a demo signal.\n"
        "Use /help for commands.\n\n"
        "⚠️ Demo only — not a prediction or guarantee."
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = round(random.uniform(1.10, 3.00), 2)

    await update.message.reply_text(
        f"🎮 DEMO SIGNAL\n\n"
        f"Suggested demo multiplier: {value}x\n\n"
        f"⚠️ Random/demo only. It cannot predict the real game."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/signal - Get a demo signal\n"
        "/help - Show help"
    )

def main():
    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

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
)
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = round(random.uniform(1.10, 3.00), 2)

    await update.message.reply_text(
        f"🎮 EXPERIMENTAL SIGNAL\n\n"
        f"Suggested multiplier: {value}x\n\n"
        f"⚠️ Random/experimental only — this cannot predict the real game."
    )

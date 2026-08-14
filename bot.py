import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Store REAL results here as they are recorded.
results = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ AVIATOR SIGNAL BOT\n\n"
        "Use /add 2.30 to record the real result.\n"
        "Use /signal to calculate a signal from the recorded results."
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /add 2.30")
        return

    try:
        value = float(context.args[0])

        if value < 1.00:
            raise ValueError

        results.append(value)

        await update.message.reply_text(
            f"✅ REAL RESULT RECORDED: {value:.2f}x\n"
            f"📊 Results recorded: {len(results)}"
        )

    except ValueError:
        await update.message.reply_text("Enter a valid multiplier, e.g. /add 2.30")


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text(
            "❌ No real results available yet.\n"
            "The bot cannot calculate a signal without data."
        )
        return

    recent = results[-10:]

    average = sum(recent) / len(recent)
    lowest = min(recent)
    highest = max(recent)

    # Deterministic calculation from REAL recorded results.
    target_low = round(max(1.10, average * 0.85), 2)
    target_high = round(average * 1.25, 2)

    if len(recent) >= 5:
        green = "🟢 GREEN SIGNAL"
    else:
        green = "🟡 LIMITED SIGNAL"

    await update.message.reply_text(
        "✈️ AVIATOR SIGNAL\n\n"
        f"{green}\n"
        f"🎯 TARGET: {target_low:.2f}x – {target_high:.2f}x\n\n"
        f"📊 Based on {len(recent)} REAL recorded results\n"
        f"📈 Average: {average:.2f}x\n"
        f"⬇️ Low: {lowest:.2f}x\n"
        f"⬆️ High: {highest:.2f}x"
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

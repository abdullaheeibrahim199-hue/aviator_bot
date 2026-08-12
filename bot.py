import os
from statistics import mean

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

results = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Aviator Tracker is online!\n\n"
        "Commands:\n"
        "/add 2.50 - record a result\n"
        "/stats - view statistics\n"
        "/signal - get a statistical estimate\n"
        "/clear - clear recorded results"
    )


async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /add 2.50")
        return

    try:
        value = float(context.args[0])

        if value < 1:
            await update.message.reply_text(
                "❌ The value must be at least 1.00x."
            )
            return

        results.append(value)

        await update.message.reply_text(
            f"✅ Recorded: {value:.2f}x\n"
            f"Rounds recorded: {len(results)}"
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid number.\nExample: /add 2.50"
        )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text(
            "No results recorded yet.\n\n"
            "Use /add 2.50 to record a result."
        )
        return

    average = mean(results)
    highest = max(results)
    lowest = min(results)
    last_10 = results[-10:]

    last_text = ", ".join(f"{x:.2f}x" for x in last_10)

    await update.message.reply_text(
        "📊 Aviator Statistics\n\n"
        f"Rounds: {len(results)}\n"
        f"Average: {average:.2f}x\n"
        f"Highest: {highest:.2f}x\n"
        f"Lowest: {lowest:.2f}x\n\n"
        f"Last 10: {last_text}"
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text(
            "⚠️ No recorded results yet.\n\n"
            "Record some rounds first using:\n"
            "/add 2.50"
        )
        return

    # Use the most recent 10 recorded results.
    recent = results[-10:]

    average = mean(recent)
    lowest = min(recent)
    highest = max(recent)

    # Simple statistical estimate from recorded history.
    estimate = round((average + lowest) / 2, 2)

    # Keep the displayed estimate within the observed range.
    estimate = max(lowest, min(estimate, highest))

    await update.message.reply_text(
        "📡 STATISTICAL SIGNAL\n\n"
        f"Recorded rounds: {len(results)}\n"
        f"Recent average: {average:.2f}x\n"
        f"Recent low: {lowest:.2f}x\n"
        f"Recent high: {highest:.2f}x\n\n"
        f"📍 Estimated range point: {estimate:.2f}x\n\n"
        "⚠️ This is calculated only from your recorded history. "
        "It cannot know or guarantee the next Aviator result."
    )


async def clear_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results.clear()

    await update.message.reply_text(
        "🗑️ All recorded results have been cleared."
    )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_result))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("clear", clear_results))

    print("🤖 Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()

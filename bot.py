import os
from statistics import mean
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

results = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Aviator Tracker is online!\n\n"
        "Commands:\n"
        "/add 2.50 - record a result\n"
        "/stats - view statistics\n"
        "/clear - clear recorded results"
    )


async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /add 2.50")
        return

    try:
        value = float(context.args[0])

        if value < 1:
            await update.message.reply_text("Enter a multiplier of 1.00 or higher.")
            return

        results.append(value)

        await update.message.reply_text(
            f"✅ Recorded: {value:.2f}x\n"
            f"Rounds recorded: {len(results)}"
        )

    except ValueError:
        await update.message.reply_text("Please enter a number, for example: /add 2.50")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text(
            "No results recorded yet.\n\n"
            "Use /add 2.50 to record a result."
        )
        return

    await update.message.reply_text(
        f"📊 Aviator Statistics\n\n"
        f"Rounds: {len(results)}\n"
        f"Average: {mean(results):.2f}x\n"
        f"Highest: {max(results):.2f}x\n"
        f"Lowest: {min(results):.2f}x\n\n"
        f"Last 10: {', '.join(f'{x:.2f}x' for x in results[-10:])}"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results.clear()
    await update.message.reply_text("🗑️ All recorded results have been cleared.")


def main():
    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_result))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("clear", clear))

    app.run_polling()


if __name__ == "__main__":
    main()

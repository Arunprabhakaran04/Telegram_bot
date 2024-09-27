from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from LLM import main
token:Final = "7642391641:AAG9pT9ZvxtBrf3JllHy9b7EvfKvO5_UO0M"
bot_username:Final = "@bananana_bot_bot"

#commands for the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the world of banana")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something so that i can respond.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom Command")

#respond to the bot -
def handle_response(text:str)->str:
    text = text.lower()
    if "hello" in text:
        return "Hey there !"
    if "chat" in text:
        print("Connecting you with the llm..")
        result = main(text)


    return "please use chat keyword in your message to query the llm."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text:str = update.message.text

    print(f'user{update.message.chat.id} in {message_type}: "{text}"')

    if message_type == "group":
        if bot_username in text:
            new_text = text.replace(bot_username,"").strip()
            response: str = handle_response(new_text)
        else:
            return

    else:
        response = handle_response(text)

    print("Bot : ", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update{update} caused the following error {context.error}')


if __name__ == "__main__":
    print("starting bot ..")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)
    print("polling the bot")
    app.run_polling(poll_interval=3)


from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from LLM import main
from dotenv import load_dotenv
import os
load_dotenv()
import requests
from serpapi import GoogleSearch

serpapi_key:Final = os.getenv("serpAPI_API_TOKEN")
token:Final = os.getenv("bot_token")
bot_username:Final = os.getenv("@bananana_bot_bot")


#commands for the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the world of banana")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something so that i can respond.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text.replace("/search", "").strip()
    await update.message.reply_text("Custom Command")
    if not user_query:
        await update.message.reply_text("Please provide a query. Example: /search How is the weather?")
        return
    params = {
        "q": user_query,  # User query
        "hl": "en",       # Language
        "gl": "us",       # Country
        "api_key": serpapi_key,
    }
    search = GoogleSearch(params)
    result = search.get_dict()
    if "organic_results" in result and len(result["organic_results"]) > 0:
        top_result = result["organic_results"][0]
        title = top_result.get("title", "No title found")
        snippet = top_result.get("snippet", "No snippet found")
        link = top_result.get("link", "#")

        # Construct the response message
        response_message = f"**Top result**: \n\n*{title}*\n{snippet}\n[Link]({link})"

    else:
        response_message = "Sorry, I couldn't find any results for your query."

    # Send the result back to the user
    await update.message.reply_text(response_message, parse_mode="Markdown")


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


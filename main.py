from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
load_dotenv()

from serpapi import GoogleSearch
import random
from datetime import datetime
from LLM import generate_text
from text_to_image_apimodel import generate_image

#importing keys
serpapi_key:Final = os.getenv("serpAPI_API_TOKEN")
SERP_API_URL = "https://serpapi.com/search"
token:Final = os.getenv("bot_token")
bot_username:Final = os.getenv("@bananana_bot_bot")


#commands for the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the world of banana")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Bot Commands*\n\n"
        "/start - Start the bot or restart the conversation.\n"
        "/help - Display this help message with available commands.\n"
        "/custom - Trigger a custom interaction with tips and fun facts.\n"
        "/ask [query] - Ask the bot any question, and query an llm for the answer.\n"
        "/search [query] - Perform a search and get top search results from the web.\n"
        "/generateimage [query] - generates an image from the user query.\n\n"
        "💡 *How to use*\n"
        "- Use `/ask` followed by your query to get answers from the web.\n"
        "- Type `/custom` to receive tech tips, fun facts, and bot suggestions.\n\n"
        "Feel free to explore the commands and let me know if you need help!"
    )

    await update.message.reply_text(help_text, parse_mode="Markdown")

tips_and_facts = [
    "Did you know? The first computer virus was created in 1983!",
    "Tip: Regularly update your software to protect against vulnerabilities.",
    "Fun fact: The first email ever sent was by Ray Tomlinson to himself in 1971.",
    "Tip: Use version control (like Git) for better collaboration and code management.",
    "Did you know? The first 1GB hard drive, released in 1980, weighed over 500 pounds!",
]

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    current_time = datetime.now().strftime("%H:%M")

    if 5 <= datetime.now().hour < 12:
        greeting = "Good morning"
    elif 12 <= datetime.now().hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    tip_or_fact = random.choice(tips_and_facts)

    response_message = (
        f"{greeting}, {user}!\n\n"
        f"🔍 You triggered a custom command at {current_time}.\n"
        f"💡 Here's something for you: {tip_or_fact}\n\n"
        f"You can also try these commands:\n"
        f"/ask [query] - Ask me anything!\n"
        f"/search [query] - Ask me anything you want to search the web!\n"
        f"/generateimage [query] - Give me a description and I will generate an image out of it.!\n"
        f"/help - Get help using the bot.\n"
        f"/start - Restart the bot."
    )

    await update.message.reply_text(response_message)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text.replace("/search", "").strip()

    if not user_query:
        await update.message.reply_text("Please provide a query. Example: /search What is AI?")
        return

    # parameters for SerpAPI search
    params = {
        "q": user_query,  # User query
        "hl": "en",  # Language
        "gl": "us",  # Country
        "api_key": serpapi_key,
    }

    search = GoogleSearch(params)
    result = search.get_dict()

    # Check for organic results
    if "organic_results" in result and len(result["organic_results"]) > 0:
        top_result = result["organic_results"][0]
        title = top_result.get("title", "No title found")
        snippet = top_result.get("snippet", "No snippet found")
        link = top_result.get("link", "#")

        response_message = f"**Top result**: \n\n*{title}*\n{snippet}\n[Link]({link})"
    else:
        response_message = "Sorry, I couldn't find any results for your query."

    await update.message.reply_text(response_message, parse_mode="Markdown")


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text.replace("/ask", "").strip()

    if not user_query:
        await update.message.reply_text("Please provide a query to ask. Example: /search What is AI?")
        return

    try:
        response = generate_text(user_query)
        await update.message.reply_text(f"Answer: {response}")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


# async def generateimage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_prompt = " ".join(context.args)
#
#     if not user_prompt:
#         await update.message.reply_text(
#             "Please provide a prompt for image generation. Example: /generateimage A sunset over mountains")
#         return
#
#     try:
#         image_path = generate_image(
#             user_prompt)
#
#         if image_path and os.path.exists(image_path):
#             await update.message.reply_photo(photo=open(image_path, 'rb'))
#         else:
#             await update.message.reply_text("Sorry, I couldn't generate the image.")
#
#     except Exception as e:
#         await update.message.reply_text(f"Error generating image: {str(e)}")

async def generateimage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.replace("/generateimage", "").strip()

    if not prompt:
        await update.message.reply_text("Please provide a prompt after the command, e.g. '/generateimage a cat on a chair'.")
        return

    # Notify the user that the image generation has started
    await update.message.reply_text("Generating image... Please wait, this may take a while for complex prompts.")

    # Call the external generate_image function
    image_path = generate_image(prompt)

    if image_path and os.path.exists(image_path):
        # Send the image back to the user
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.message.chat.id, photo=photo)

        await update.message.reply_text(f"Here is your generated image based on the prompt: {prompt}")

    else:
        await update.message.reply_text("Error: Unable to generate image. Please try again.")


#respond to the bot -
def handle_response(text: str) -> str:
    """
    This function processes user input and returns an appropriate response based on keywords.
    The function can be extended to handle more commands or keywords.
    """
    text = text.lower().strip()

    response_map = {
        "hello": "Hey there!",
        "hi": "Hello! How can I assist you today?",
        "help": "Here is the list of available commands: /start, /help, /search, /ask, /generateimage",
        "thanks": "You're welcome!",
        "bye": "Goodbye! Feel free to reach out anytime."
    }

    for keyword, response in response_map.items():
        if keyword in text:
            return response

    # Default response if no keyword matches
    return "I'm not sure I understand. Consider using the list of available commands or ask for help with /help."

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
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("generateimage", generateimage_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)
    print("polling the bot")
    app.run_polling(poll_interval=3)

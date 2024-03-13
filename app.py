import json
import os
from telegram import Update
from resp import get_resp
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
     chat_id=update.effective_chat.id, 
     text=f"""Hii {update.message.from_user.first_name}, how can I help you today?
     """
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
     chat_id=update.effective_chat.id, 
     text="""
     This bot supports the following commands:
      - /start: Welcoming users
      - /help: List of supported commands (you are here)
     """
    )
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Handle empty messages gracefully
    if not user_text:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='You sent an empty message.'
        )
        return

    response_text = get_resp(user_text)

    # Check if the response_text can be serialized to JSON
    try:
        json.dumps(response_text)
    except TypeError as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Error: Unable to send response due to non-serializable content. {e}'
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )



if __name__ == '__main__':
    application = Application.builder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)
    
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)

    application.run_polling()
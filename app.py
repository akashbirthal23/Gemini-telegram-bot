import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from resp import get_resp

load_dotenv()
token = os.getenv('token')

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'Hii {update.message.from_user.first_name}, how can I help you today?'
    )

def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="""
        This bot supports the following commands:
         - /start: Welcoming users
         - /help: List of supported commands (you are here)
        """
    )

def echo(update, context):
    user_text = update.message.text

    # Handle empty messages gracefully
    if not user_text:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='You sent an empty message.'
        )
        return

    response_text = get_resp(user_text)

    # Check if the response_text can be serialized to JSON
    try:
        json.dumps(response_text)
    except TypeError as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Error: Unable to send response due to non-serializable content. {e}'
        )
        return

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )

if __name__ == '__main__':
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()

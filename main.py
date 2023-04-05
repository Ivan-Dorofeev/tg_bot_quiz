import json
import logging
import os
import random

import telegram
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Привет, {user.mention_markdown_v2()}\!',
                                     reply_markup=ForceReply(selective=True))


def help_command(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Новый вопрос', 'Сдаться', 'Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text('Help!', reply_markup=reply_markup)


def echo(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Новый вопрос', 'Сдаться', 'Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    if update.message.text == 'Новый вопрос':
        """Отправляем рандомный вопрос викторины"""
        with open('questions_and_answers.json', 'r') as quiz_file:
            json_quiz = json.load(quiz_file)
        random_question_number = random.choice(list(json_quiz.keys()))
        random_question = json_quiz[random_question_number]['question']

        update.message.reply_text(random_question, reply_markup=reply_markup)
    else:
        update.message.reply_text(update.message.text, reply_markup=reply_markup)


def main(bot_token) -> None:
    updater = Updater(bot_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


def redis():
    #  redis-cli -u redis://<username>:<password>@redis-15696.c1.us-east1-2.gce.cloud.redislabs.com:15696
    pass


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    redis_name = os.environ['REDIS_USER_NAME']
    redis_password = os.environ['REDIS_USER_PASSWORD']
    main(bot_token)

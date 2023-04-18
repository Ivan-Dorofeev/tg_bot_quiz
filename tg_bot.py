import json
import logging
import os
import random
import redis
import telegram
from functools import partial
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

logger = logging.getLogger('tg_bot_logger')

WAIT_START_QUIZ, WAIT_ANSWER = range(2)

CUSTOM_KEYBOARD = [['Новый вопрос', 'Сдаться', 'Мой счёт']]
reply_markup = telegram.ReplyKeyboardMarkup(CUSTOM_KEYBOARD)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Привет, {user.mention_markdown_v2()}\!',
                                     reply_markup=reply_markup)
    return WAIT_START_QUIZ


def help_command(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Новый вопрос', 'Сдаться', 'Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text('Help!', reply_markup=reply_markup)
    return WAIT_START_QUIZ


def handle_new_question_request(update: Update, context: CallbackContext, conn, quiz_library):
    """Задаём рандомный вопрос"""

    user_id = update.message.from_user.id

    question_number, question_and_answer = quiz_library[random.choice(list(quiz_library.items()))]

    # Записываем пользователя и вопрос в базу
    conn.set(user_id, question_number)
    update.message.reply_text(question_and_answer['question'], reply_markup=reply_markup)

    return WAIT_ANSWER


def handle_solution_attempt(update: Update, context: CallbackContext, conn, quiz_library):
    """Проверяем ответ на рандомный вопрос"""
    user_id = update.message.from_user.id
    user_msg = update.message.text

    number_question_of_user = conn.get(user_id)
    if number_question_of_user:
        answer = quiz_library[number_question_of_user]['answer']

        user_msg_first_text = user_msg.split('.')[0]
        if user_msg_first_text in answer:
            update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
                                      reply_markup=reply_markup)
        else:
            update.message.reply_text(f'Увы, Не верно.', reply_markup=reply_markup)
            return WAIT_ANSWER
    else:
        update.message.reply_text('Нажми «Новый вопрос»', reply_markup=reply_markup)
        return WAIT_START_QUIZ


def cancel_quiz(update: Update, context: CallbackContext, conn, quiz_library):
    user_id = update.message.from_user.id

    number_question_of_user = conn.get(user_id)
    if number_question_of_user:
        answer = quiz_library[number_question_of_user]['answer']
        update.message.reply_text(f'Правильный ответ:\n{answer}', reply_markup=reply_markup)
        conn.delete(user_id)  # Удаляем пользователя и вопрос из базы

        handle_new_question_request(update=update, context=context, conn=conn, quiz_library=quiz_library)
    else:
        update.message.reply_text(f'Радо сдаваться, ты ещё не начал =). Нажми "Новый вопрос"')
        return WAIT_START_QUIZ


def run_bot(bot_token, conn, quiz_library) -> None:
    updater = Updater(bot_token)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            WAIT_START_QUIZ: [
                MessageHandler(Filters.regex('^(Новый вопрос)$'),
                               partial(handle_new_question_request, conn=conn, quiz_library=quiz_library))],

            WAIT_ANSWER: [
                MessageHandler(Filters.regex('^(Сдаться)$'),
                               partial(cancel_quiz, conn=conn, quiz_library=quiz_library)),
                MessageHandler(Filters.text, partial(handle_solution_attempt, conn=conn, quiz_library=quiz_library))
            ]
        },

        fallbacks=[
            MessageHandler(Filters.regex('^(Сдаться)$'), partial(cancel_quiz, conn=conn, quiz_library=quiz_library))]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    redis_host = os.environ['REDIS_USER_HOST']
    redis_port = os.environ['REDIS_USER_PORT']
    redis_password = os.environ['REDIS_USER_PASSWORD']

    with open('questions_and_answers.json', 'r') as quiz_file:
        quiz_library = json.load(quiz_file)

    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    run_bot(bot_token, conn, quiz_library)


if __name__ == '__main__':
    main()

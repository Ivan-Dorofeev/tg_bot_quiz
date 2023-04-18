import json
import logging
import os
import time

import redis
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from dotenv import load_dotenv
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

logger = logging.getLogger("vk_bot_logger")


def add_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.PRIMARY)
    return keyboard


def check_answer(event, vk_api, conn, json_quiz):
    """Проверяем ответ на рандомный вопрос"""
    user_id = event.user_id
    user_msg = event.text

    number_question_of_user = conn.get(user_id)
    if number_question_of_user:
        answer = json_quiz[number_question_of_user]['answer']

        user_msg_first_text = user_msg.split('.')[0]
        if user_msg_first_text in answer:
            keyboard = add_keyboard()
            vk_api.messages.send(
                user_id=user_id,
                message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
                random_id=random.randint(1, 1000),
                keyboard=keyboard.get_keyboard()
            )
        else:
            keyboard = add_keyboard()
            vk_api.messages.send(
                user_id=user_id,
                message='Увы, Не верно.',
                random_id=random.randint(1, 1000),
                keyboard=keyboard.get_keyboard()
            )
    else:
        keyboard = add_keyboard()
        vk_api.messages.send(
            user_id=user_id,
            message='Нажми «Новый вопрос»',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )


def new_question_request(event, vk_api, conn, quiz_library):
    """Задаём рандомный вопрос"""

    user_id = event.user_id

    question_number, question_and_answer = quiz_library[random.choice(list(quiz_library.items()))]

    # Записываем пользователя и вопрос в базу
    conn.set(user_id, question_number)

    keyboard = add_keyboard()
    vk_api.messages.send(
        user_id=user_id,
        message=question_and_answer['question'],
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def cancel_quiz(event, vk_api, conn, json_quiz):
    user_id = event.user_id

    number_question_of_user = conn.get(user_id)
    if number_question_of_user:
        answer = json_quiz[number_question_of_user]['answer']

        keyboard = add_keyboard()
        vk_api.messages.send(
            user_id=event.user_id,
            message=f'Правильный ответ:\n{answer}',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )

        conn.delete(user_id)  # Удаляем пользователя и вопрос из базы

        new_question_request(event, vk_api, conn, json_quiz)
    else:
        keyboard = add_keyboard()
        vk_api.messages.send(
            user_id=event.user_id,
            message='Радо сдаваться, ты ещё не начал =). Нажми "Новый вопрос"',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    vk_group_token = os.environ['VK_API_GROUP_TOKEN']
    redis_host = os.environ['REDIS_USER_HOST']
    redis_port = os.environ['REDIS_USER_PORT']
    redis_password = os.environ['REDIS_USER_PASSWORD']

    with open('questions_and_answers.json', 'r') as quiz_file:
        json_quiz = json.load(quiz_file)

    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text == "Сдаться":
                        cancel_quiz(event, vk_api, conn, json_quiz)
                    if event.text == "Новый вопрос":
                        new_question_request(event, vk_api, conn, json_quiz)
                    else:
                        check_answer(event, vk_api, conn, json_quiz)
        except ConnectionError:
            logger.warning('Ошибка соединения')
            time.sleep(60)
            continue
        except Exception as exc:
            logger.warning(exc)
            continue


if __name__ == '__main__':
    main()

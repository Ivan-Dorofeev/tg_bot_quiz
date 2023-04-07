# Бот-викторина для VK и Telegram

## Описание

Боту общается по заранее подготовленным фразам, который храним в своём аккаунте [Dialogflow](https://dialogflow.cloud.google.com/)

**VK**  - [VK Group](https://vk.com/im?media=&sel=-194790108)

![vk_gif](https://user-images.githubusercontent.com/58893102/222070436-49f7884e-103a-4a0b-b5e5-e9c2a1b997dd.gif)


**Telegram** - [TG Bot](https://t.me/verb_game_bot)

![tg_gif](https://user-images.githubusercontent.com/58893102/222070418-aae63936-bbc3-42fa-ba86-584a3de23b0f.gif)


## Установка

- скачать репозиторий
- установите необходимы библиотеки командой:

    ```pip install -r requirements.txt```
    
- создайте файл ```.env``` в корневом каталоге
- положите в него:

    ```TG_BOT_TOKEN``` - токен от телеграмм бота

    ```REDIS_USER_HOST``` - хост
    
    ```REDIS_USER_PORT``` - номер порта

    ```REDIS_USER_PASSWORD``` - пароль пользователя Redis
    
    ```VK_API_GROUP_TOKEN``` - токен своей группы в VK

- создайте JSON словарь с вопросами и ответами в таком формате (назовите его "questions_and_answers.json"):


## Запуск

- запустить VK-бота командой:
        ```python create_intent.py```

- запустить TG-бота командой:
       ```python create_intent.py```

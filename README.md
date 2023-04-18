# Бот-викторина для VK и Telegram

## Описание

Боту даётся словарь с вопросами и ответами.
Он проводит викторину.
Данны об ответах бот запонимает в Redis.

VK:

![vk_bot_video](https://user-images.githubusercontent.com/58893102/230610119-0713c56e-8331-4653-8bed-b08a5f5b9e52.gif)


TG:

![tg_bot_video](https://user-images.githubusercontent.com/58893102/230610121-21c53690-7648-4cd6-9cf4-8f01fd886568.gif)


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
    - создайте .txt файлы и положите туда вопросы и ответы (как на картинке):
        ![image](https://user-images.githubusercontent.com/58893102/232674166-a1125293-b2a3-4cc5-985f-825739f36ca1.png)
    - положите эти файлы в папку "questions"
    - запустите скрипт для создания json-словаря для викторины командой:
    
        ```python get_quiz_json.py```

## Запуск

- запустить VK-бота командой:
        ```python vk_bot.py```

- запустить TG-бота командой:
       ```python tg_bot.py```

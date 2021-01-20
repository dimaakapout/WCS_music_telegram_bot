# WCS_music_telegram_bot
Music bot in telegram for West coast swing training 

Начинающие танцоры west coast swing часто сталкиваются с проблемой - отсутсвие удобной коллекции музыки для тренировок, отранжированной по скорости (темпу) и по жанру. Бот решает эту проблему.

Найти бота: **@WCS_music_sampo_bot**
------------

### Пример работы
![](https://github.com/dimaakapout/WCS_music_telegram_bot/blob/master/example.JPG)

------------

### Установка и запуск
`cd /home/`
`git clone https://github.com/dimaakapout/WCS_music_telegram_bot`
`mkdir src_bot # Каталог с базой данных`
`docker build -t bot_app .`
`docker run --name bot --restart=always -d -v /home/src_bot:/bot/src bot_app`


### Структура проекта

**-- bot.py**  (исполняемый файл)

**-- database**  (база данных)

**-- requirements.txt**  (библиотеки)

**-- sms.txt**    (сообщения от бота)

**-- token.txt**    (токен)



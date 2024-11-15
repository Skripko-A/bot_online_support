# Online Support Bot

Online Support Bot – это AI-ассистент для обработки запросов и поддержки пользователей в онлайн-режиме. Этот проект предназначен для интеграции AI в процессы поддержки клиентов, чтобы повысить эффективность и качество обслуживания.

## Оглавление

- [Описание](#описание)
- [Требования](#требования)
- [Установка](#установка)
  - [Репозиторий](#репозиторий)
  - [Dialog Flow](#dialog-flow)
  - [google-cloud-cli](#google-cloud-cli)
  - [Программное создание агентов](#программное-создание-агентов)
  - [Бот в телеграм](#бот-в-телеграм)
  - [Сообщество в VK.com](#сообщество-в-vkcom)
  - [.env](#env)
- [Использование](#использование)
- [Цель проекта](#цель-проекта)
## Описание

Online Support Bot предоставляет следующие возможности:
- Автоматизация ответов на часто задаваемые вопросы.
- Интеграция с различными платформами мессенджеров Telegram и VK.

## Демо

Вконтакте - https://vk.com/club227193853  
![](https://github.com/Skripko-A/online_support_bot/blob/main/vk_support_bot_demo.gif)  
Телеграм - https://t.me/game_of_verbs_tele_bot  
![](https://github.com/Skripko-A/online_support_bot/blob/main/tg_support_bot_demo.gif)  

## Требования

- Python 3.8+
- Установленные библиотеки из файла `requirements.txt`
- gcloud-cli

## Установка

### Репозиторий:

```bash
git clone https://github.com/Skripko-A/online_support_bot.git
```
```bash
cd online_support_bot
```
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 isntall -r requirements.txt
```
Проект использует google dialog flow для распознавания популярных вопросов и подбора ответов,  
в связи с чем нужно также настроить google cloud cli. Вам понадобится ваш аккаунт google.

### Dialog flow
Научит ваших ботов распознавать частые вопросы и давать на них ответы
 - [создать проект ](https://console.cloud.google.com/projectselector2/home/)
 - [создать агента](https://dialogflow.cloud.google.com/#/agent/)  

Будьте внимательны, агент должен принадлежать вашему проекту.
Принадлежность определяется атрибутом Project_ID. У агента должен быть указан ID вашего проекта.

### google-cloud-cli
Нужно установить чтообы ваша машина имела доступ к вашему проекту `dialog_flow`.
[Инструкция по установке](https://cloud.google.com/sdk/docs/install) 

Теперь нужно показать google-cloud-cli ваш аккаунт google.

```bash
gcloud auth application-default login
```
Терминал предложит вам ссылку для входа в аккаунт и получения проверочного кода.  
Зайдите не страницу по предложенной вам в терминале ссылке.  
Пройдя по ссылке в браузере, выполните (подтвердите вход в аккаунт google).  
Бразуер автоматически перейдет на страницу с проверочным кодом.  
Скопируйте код в буфер обмена и вставьте код в окно терминала:  

`Once finished, enter the verification code provided in your browser: здесь должен быть ваш код`

Инициализируйте gcloud
```bash
gcloud init
```

### Программное создание агентов.
`learning_script.py` может создавать агентов автоматически при запуске:  
```bash
python3 learning_script.py
```
Вам понадобится файл `questions.json` соответствующей структуры:
```json
{
    "тема популярного вопроса": {
        "questions": [
            "первый вариант постановки популярного вопроса",
            "второй вариант",
            ...
        ],
        "answer": "Ответ, покрывающий тему данного популярного вопроса в любых его вариациях"
    },
  ...
    
}
```

Заполните приведенную "форму", после чего запустите скрипт. Скрипт создаст агентов. Агенты обучат ваших ботов.

###  Бот в телеграм
Создайте бота в телеграм:
 - Напишите отцу ботов в телеграм `@BotFather (https://t.me/BotFather)`
 - Надо будет придумать имена боту. После чего BotFather сообщит вам токен вашего бота.

### Сообщество в VK.com
Для работы с api вам понадобится включить двухфакторную аутентификацию в настройках безопасности аккаунта VK.
 - Перейдите в настройки созданного сообщества, найдите там пункт про api.  
 - Не забудьте в настройках сообщества включить сообщения, по умолчанию они могут быть выключены.
 - Нажмите создать ключ. 


### .env
 Запишите идентификационные данные в файлик .env:
```text
TG_BOT_TOKEN = id вашего бота в телеграм
DIALOG_FLOW_PROJECT_ID = id проекта в dialog flow
VK_API_KEY = ключ сообщества в vk
TG_ADMIN_CHAT_ID = id чата телеграм, в который бот будет присылать 
                    инфу мониторинга (бот запущен, бот упал)
QUESTIONS_PATH = относительны путь к файлу ('questions.json' если файл  
                  в корне проекта) questions.py в котором у вас вопросы и ответы для обучения dialog flow
```

## Использование

Для запуска бота выполните следующую команду:

```bash
python tg_bot.py
```
```bash
python3 vk_bot.py
```

## Цель проекта
Проект написан в учебных целях в рамках прохождения курса веб-разработчика Devman

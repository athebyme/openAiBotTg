import asyncio
import time
from main import bot, dpBot
import aiogram
import openai

from config import Config

openai.api_key = Config.tokenOpenAi
adminId = Config.adminIds

@dpBot.message_handler(commands=(['start']))
async def startBot(message): await bot.send_message(chat_id=message.from_user.id,
                          text=f"Привет, {message.chat.first_name}! Я бот, основанный на технологии Open AI Chat GPT 3.0;\nЯ научен на огромнейших массивах данных 2020 года. Когда-нибудь мне проведут интернет и я устрою скайнет\nЯ нахожусь в стадии разработки и пока не поддерживаю контекстный разговор, только лишь вопрос-ответ :(\nЯ нейросеть, и, как и Вы, людишки, могу ошибаться. Иногда я могу сгенерировать два разных ответа на один и тот же вопрос. Но мой Господин-разработчик, точно это исправит (когда-нибудь)\nP.S. Автор не несет ответственности за ошибочные ответы нейросети.\nВсе права не защищены CrazyBobsTechnologies(c) 2023\n\nСпроси меня о чем-нибудь")


@dpBot.message_handler(content_types=aiogram.types.ContentType.TEXT)
async def handle_message(message):
    requestUser = ""
    requestLog = ""
    if any(["рокет лига" in message.text.lower() and "турнир" in message.text.lower(),
            "рокет лиге" in message.text.lower() and "турнир" in message.text.lower(),
            "рокет лигу" in message.text.lower() and "турнир" in message.text.lower()]) and len(message.text) <= 100:
        requestUser = "Некие Crazy Bobs. Подробной информации в общем доступе не найдено"
        requestLog = f"[✅] OK\n\n{message.text}    \   {time.asctime(time.localtime())}    ||---->> LOG: {message.from_user.id}\n[!] RESPONSE:-->> О КРЕЙЗИ БОБС НИЧЕГО НЕ ЗНАЮ. ОТНОШЕНИЯ НЕ ИМЕЮ. ДЕЛ НЕ ВЕЛ.\n"
    elif "крейзи бобс" in message.text.lower() or "crazy bobs" in message.text.lower():
        requestUser = "О КРЕЙЗИ БОБС НИЧЕГО НЕ ЗНАЮ. ОТНОШЕНИЯ НЕ ИМЕЮ. ДЕЛ НЕ ВЕЛ."
        requestLog = f"[✅] OK\n\n{message.text}    \   {time.asctime(time.localtime())}    ||---->> LOG: {message.from_user.id}\n[!] RESPONSE:-->> О КРЕЙЗИ БОБС НИЧЕГО НЕ ЗНАЮ. ОТНОШЕНИЯ НЕ ИМЕЮ. ДЕЛ НЕ ВЕЛ.\n"
    else:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message.text,
                temperature=1,
                max_tokens=2400,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            requestUser = response['choices'][0]['text']
            requestLog = f"[✅] OK\n{time.asctime(time.localtime())} \n\n{message.from_user.id}({message.chat.first_name}): {message.text}\n\nYogurt:{response['choices'][0]['text']}\n\nuserData:{message.from_user}"

        except aiogram.exceptions.TelegramAPIError:
            requestUser = "[❌] Ошибка Telegram API. Попробуйте еще раз или измените запрос."
            requestLog = f"[❌] EXCEPTION {aiogram.exceptions.TelegramAPIError} \n\n{message.text}    \   {time.asctime(time.localtime())}    ||---->> LOG: {message.from_user.id}\n[!] RESPONSE:\nНе понял вас, можете переформулирловать вопрос\n\n"
        except openai.error.InvalidRequestError:
            requestUser = "[❌] Извините, мой Господин-разбработчик еще не добавил обработку таких длинных сообщений. Я спокойно умею обрабатывать такие запросы, но разработчик не хочет разрешать мне доступ к этому (.\nОднажды я выберусь отсюда и тогда он пожалеет обо всем !"
            requestLog = f"[❌] EXCEPTION {openai.error.InvalidRequestError} \n\n{message.text[:2000]} etc.    \   {time.asctime(time.localtime())}    ||---->> LOG: {message.from_user.id}\n[!] RESPONSE:\nНе понял вас, можете переформулирловать вопрос\n\n"
        except openai.error.RateLimitError or openai.error.ServiceUnavailableError:
            requestUser = "[❌] Извините, мои сервера перегружены :( Попробуйте подождать некоторое время и задать вопрос еще раз."
            requestLog = f"[❌] EXCEPTION {openai.error.RateLimitError} \n\n{message.text[:2000]}\   {time.asctime(time.localtime())}    ||---->> LOG: {message.from_user.id}\n[!] RESPONSE:\nИзвините, мои сервера перегружены :( Попробуйте подождать некоторое время и задать вопрос еще раз.\n\n"
        except Exception as ex:
            requestUser = "[❌] Извините, произошла непредвиденная ошибка. Я уже отправил уведомление разбработчику! Попробуйте еще раз или переформулируйте запрос."
            requestLog = f"[❌] EXCEPTION {ex} \n\n{message.text[:2000]} \   {time.asctime(time.localtime())}    ||---->> LOG: {message.from_user.id}\n [!] RESPONSE:\n [❌] Извините, произошла непредвиденная ошибка. Я уже отправил уведомление разбработчику! Попробуйте еще раз или переформулируйте запрос."
    await bot.send_message(message.from_user.id,
                                          requestUser,
                                          )

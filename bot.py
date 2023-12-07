import telebot
from requests import get
import asyncio
from configuration.config import admin, bot_token
bot = telebot.TeleBot(bot_token)
count = 0
def send_message(data):
    count += 1
    bot.send_message(admin, f"Пользователь добавил новый фильм под названием {data[0]}\nгод: {data[1]}\nстрана: {data[2]}\nвозраст: {data[3]}\nжанр: {data[4]}\nрейтинг: {data[5]}\nдлительность: {data[6]}")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет, помогу тебе отследить изменения в базу данных")

@bot.message_handler(content_types=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id,"Всего было добавлено " + str(count) + " фильмов")

def bot_start():
    bot.infinity_polling(none_stop=True)
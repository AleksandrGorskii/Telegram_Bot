from threading import Thread
from telebot import TeleBot
from typing import Any
from time import sleep
import datetime
import telebot
import wikipedia
from telebot.types import InlineKeyboardMarkup
from wikipedia import WikipediaPage
from db import create_tables, search_info, record_info, add_info
from kb import reply_keyboard_marcup, inline_keyboard_markup
from config import BOT_TOKEN




bot: TeleBot = telebot.TeleBot(BOT_TOKEN)
bot.delete_webhook()

@bot.message_handler(commands=['start'])
def send_welcome(message) -> None:
    create_tables()

    markup = reply_keyboard_marcup()
    bot.send_message(message.chat.id, 'Привет, я бот, который поможет вам запомнить больше нужной информации.',
                     reply_markup=markup)
    bot.register_next_step_handler(message, onclick)


def onclick(message) -> None:
    if message.text == 'Узнать информацию в интернете':
        bot.reply_to(message, 'Введите запрос: ')
        bot.register_next_step_handler(message, search)

    elif message.text == 'Записать личную информацию':
        bot.reply_to(message, 'Запишите информацию: ')
        bot.register_next_step_handler(message, record)

    elif message.text == 'Посмотреть историю поиска':
        query_history(message)


def query_history(message) -> None:
    name: str = message.from_user.first_name
    surname: str = message.from_user.last_name
    result: list[str] = add_info(name, surname)
    for i_elem in result:
        bot.send_message(message.chat.id, i_elem)
    bot.register_next_step_handler(message, onclick)


def search(message) -> None:
    date_now: datetime.datetime = datetime.datetime.now()
    time_now: datetime.time = datetime.time(date_now.hour, date_now.minute, date_now.second)
    date_now_str: str = date_now.strftime('%Y-%m-%d')
    time_now_str: str = time_now.strftime('%H:%M:%S')
    try:
        wikipedia.set_lang('ru')
        query: Any = message.text
        result: Any = wikipedia.summary(query, sentences=2)
        complete_url: WikipediaPage = wikipedia.page(query)
        name: str = message.from_user.first_name
        surname: str = message.from_user.last_name
        history: Any = result

        search_info(date_now_str, time_now_str, query, name, surname, history)
        markup: InlineKeyboardMarkup = inline_keyboard_markup(complete_url)
        bot.send_message(message.chat.id, result, reply_markup=markup)
        pr1: Thread = Thread(target=the_repetition_interval_of_the_search,
                               args=(message, history, markup, (1200, 3600, 64800)))
        pr1.start()
        bot.register_next_step_handler(message, onclick)

    except wikipedia.exceptions.DisambiguationError as err:
        options: Any = err.options
        ans: str = f"Результат неоднозначный. Попробуйте уточнить запрос. Варианты: {', '.join(options)}"
        bot.send_message(message.chat.id, ans)

    except wikipedia.exceptions.PageError:
        bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено! Уточните запрос')


def record(message) -> None:
    date_now: datetime.datetime = datetime.datetime.now()
    time_now: datetime.time = datetime.time(date_now.hour, date_now.minute, date_now.second)
    date_now_str: str = date_now.strftime('%Y-%m-%d')
    time_now_str:str = time_now.strftime('%H:%M:%S')
    name: str = message.from_user.first_name
    surname: str = message.from_user.last_name
    history: Any = message.text

    record_info(date_now_str, time_now_str, history, name, surname)

    pr2: Thread = Thread(target=the_repetition_interval_of_the_record, args=(message, history, (1200, 3600, 64800)))
    pr2.start()
    bot.register_next_step_handler(message, onclick)


def the_repetition_interval_of_the_search(message, history: Any, markup: InlineKeyboardMarkup, tpl: tuple[int]) -> None:
    for t in tpl:
        sleep(t)
        bot.send_message(message.chat.id, history, reply_markup=markup)


def the_repetition_interval_of_the_record(message, history: Any, tpl: tuple[int]) -> None:
    for t in tpl:
        sleep(t)
        bot.send_message(message.chat.id, history)


if __name__ == '__main__':
    bot.polling(none_stop=True)


from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def reply_keyboard_marcup() -> ReplyKeyboardMarkup:
    markup: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1: KeyboardButton = types.KeyboardButton('Узнать информацию в интернете')
    btn2: KeyboardButton = types.KeyboardButton('Записать личную информацию')
    btn3: KeyboardButton = types.KeyboardButton('Посмотреть историю поиска')
    markup.row(btn1, btn2)
    markup.row(btn3)
    return markup

def inline_keyboard_markup(complete_url) -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    btn1: InlineKeyboardButton = types.InlineKeyboardButton('Узнать больше и запомнить',
                                      url=complete_url.url)

    markup.row(btn1)
    return markup
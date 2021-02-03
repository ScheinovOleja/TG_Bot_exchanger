from config import *
from parser_el_change import GetCurrency
import telebot
from telebot import types

parser = GetCurrency()
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bot = telebot.TeleBot(token)
new_exchange = types.KeyboardButton("🔁 Новый обмен")
exchange_history = types.KeyboardButton("⌛ История обменов")
about_bot = types.KeyboardButton("ℹ️О боте")
support_key = types.KeyboardButton("🔔 Поддержка")
news = types.KeyboardButton("📫 Новости")
community = types.KeyboardButton("👥 Сообщество")
support_button = types.InlineKeyboardButton("🔔 Поддержка", url='https://el-change.com/faq')
terms_of_use = types.InlineKeyboardButton("Правила использования", url='https://el-change.com/rules')
returns_policy = types.InlineKeyboardButton("Политика возвратов", url='https://el-change.com/rules')


@bot.message_handler(commands=['start'])
def welcome(message):
    markup.add(new_exchange, exchange_history, about_bot, support_key, news, community)
    bot.send_message(message.chat.id, '👋 Привет! Давай начнем.', reply_markup=markup)
    bot.send_message(message.chat.id,
                     'Для произведения обмена нажми на кнопку 🔁 Новый обмен, она в нижнем меню 👇')


@bot.message_handler(content_types=['text'])
def message_one(message):
    markup_key = types.InlineKeyboardMarkup(row_width=2)
    if message.chat.type == 'private' and message.text == "ℹ️О боте":
        bot.send_message(message.chat.id,
                         'Привет, я телеграм бот!',
                         parse_mode='HTML')
        markup_key.add(support_button, terms_of_use, returns_policy)
        bot.send_message(message.chat.id, 'Более подробная информация доступна тут 👇', reply_markup=markup_key)
    if message.chat.type == 'private' and message.text == "🔔 Поддержка":
        markup_key.add(support_button, terms_of_use, returns_policy)
        bot.send_message(message.chat.id, 'Более подробная информация доступна тут 👇', reply_markup=markup_key)
    if message.chat.type == 'private' and message.text == "⌛ История обменов":
        bot.send_message(message.chat.id, '❗️ Твой список обменов пуст.')
    if message.chat.type == 'private' and message.text == "🔁 Новый обмен":
        for element in parser.parsing_give():
            markup_key.add(types.InlineKeyboardButton(element, callback_data=f'{element}_1'))
        bot.send_message(message.chat.id, 'Выбери валюту, которую нужно обменять 👇', reply_markup=markup_key)


def treatment_give(call, text, markup_key):
    dict_values = []
    for element in parser.parsing_get():
        if element in dict_values or element == text[:-2]:
            continue
        else:
            dict_values.append(element)
            markup_key.add(types.InlineKeyboardButton(element, callback_data=f'{element}_2'))
    bot.send_message(call.message.chat.id, 'Выбери валюту, которую нужно получить 👇',
                     reply_markup=markup_key)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup_key = types.InlineKeyboardMarkup(row_width=2)
    try:
        if call.message:
            if '_1' in call.data:
                treatment_give(call, call.data, markup_key)
            elif '_2' in call.data:
                bot.send_message(call.message.chat.id, f'Введите данные кошелька {call.data[:-2]}')
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)

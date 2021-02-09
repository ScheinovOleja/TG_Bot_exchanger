from config import *
from parser_el_change import GetCurrency
import telebot
from telebot import types

min_amount = 0
max_amount = 0
total_amount_text = ''
num_receive = ''

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
        bot.send_message(message.chat.id, 'Привет, я телеграм бот!', parse_mode='HTML')
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
        return True


def treatment_give(call, text, markup_key):
    global min_amount, max_amount, total_amount_text, num_receive
    dict_values = []
    give_currency = parser.parsing_give()
    num_receive = [num[1] for num in give_currency.items() if num[0] == text[:-2]]
    min_amount = float(num_receive[0][1][0])
    max_amount = float(num_receive[0][1][1])
    elements = parser.parsing_get(num_receive[0][0])
    for element in elements:
        dict_values.append(element[0])
        markup_key.add(types.InlineKeyboardButton(element[0] + f' {element[1]} ' + f'({element[2]})',
                                                  callback_data=f'{element[0]}_2'))
    bot.send_message(call.message.chat.id, 'Выбери валюту, которую нужно получить 👇',
                     reply_markup=markup_key)


def determining_currency(text):
    global total_amount_text, num_receive
    for element in parser.parsing_get(num_receive[0][0]):
        if element[0] == text[:-2]:
            total_amount_text = element[1]


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup_key = types.InlineKeyboardMarkup(row_width=2)
    try:
        if call.message:
            if '_1' in call.data:
                treatment_give(call, call.data, markup_key)
            elif '_2' in call.data:
                determining_currency(call.data)
                bot.send_message(
                    call.message.chat.id,
                    f'Введите сумму, которую хотите обменять: (Минимум:{min_amount}, максимум:{max_amount})'
                )
                bot.register_next_step_handler(call.message, get_amount)
    except Exception as e:
        print(repr(e))


def calc_total_amount(custom_number):
    global total_amount_text
    var_1, var_2 = float(total_amount_text.split(':')[0]), float(total_amount_text.split(':')[1])
    total_amount = (var_2 / var_1) * custom_number
    return total_amount


def get_amount(message):
    if message_one(message):
        return
    try:
        if float(message.text) < min_amount or float(message.text) > max_amount:
            bot.send_message(message.chat.id, f'Дурак чтоль? Сказал же, Минимум:{min_amount}, максимум:{max_amount}')
            bot.register_next_step_handler(message, get_amount)
        else:
            total_amount = calc_total_amount(float(message.text))
            bot.send_message(message.chat.id, f'За такую сумму ты получишь - {total_amount}')
    except Exception:
        bot.send_message(message.chat.id, f'А теперь то же самое, ток цифрами!')
        bot.register_next_step_handler(message, get_amount)


if __name__ == '__main__':
    bot.polling(none_stop=True)

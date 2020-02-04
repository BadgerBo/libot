import telebot

from config import token
import parser


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def provide_command_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    g = telebot.types.KeyboardButton(text='Жанры')
    t = telebot.types.KeyboardButton(text='Топ-100')
    r = telebot.types.KeyboardButton(text='Случайный выбор')
    keyboard.row(g)
    keyboard.row(t, r)
    bot.send_message(
        message.chat.id,
        f'Привет, {message.chat.username} \nЯ помогу тебе с выбором книги\n' +
        'Чтобы начать, выбери одну из доступных опций \n\n1)   Жанры\n2)   Топ-100\n3)   Случайный выбор',
        parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def provide_command_help(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Связаться с хозяином бота', url='https://t.me/BadgerBo'))
    bot.send_message(
        message.chat.id,
        'Выбери одну из доступных опций \n\n1)   Жанры\n2)   Топ-100\n3)   Случайный выбор' +
        '\n\nЕсли твой выбор пал на жанры, то определись с тем, какой из них интересует больше всего',
        parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_general_choice(message):
    if message.text == 'Жанры':
        provide_genres_choice(message)
    elif message.text == 'Топ-100':
        top_book = parser.compile_advice_top()
        give_book_advice(message, top_book, None)
    elif message.text == 'Случайный выбор':
        random_book = parser.compile_advice_random()
        give_book_advice(message, random_book, None)
    else:
        pass


def provide_genres_choice(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Классика', callback_data='Классическая-литература'),
        telebot.types.InlineKeyboardButton(text='Детективы', callback_data='Детективы'),
        telebot.types.InlineKeyboardButton(text='Для детей', callback_data='Детские-книги')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Фантастика', callback_data='Фантастика'),
        telebot.types.InlineKeyboardButton(text='Приключения', callback_data='Приключения'),
        telebot.types.InlineKeyboardButton(text='Ужасы', callback_data='Ужасы-мистика')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Любовные романы', callback_data='Любовные-романы'),
        telebot.types.InlineKeyboardButton(text='Фэнтези', callback_data='Фэнтези'),
        telebot.types.InlineKeyboardButton(text='Поэзия', callback_data='Поэзия-и-драматургия')
    )
    bot.send_message(message.chat.id, 'Выберите интересующий жанр', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_choice_of_genre(call):
    genre = call.data
    genre_book = parser.compile_advice_genre(genre)
    give_book_advice(call.message, genre_book, genre)


def give_book_advice(message, choice, genre):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Подробнее о книге', url=choice[0]))
    if genre != None:
        keyboard.add(telebot.types.InlineKeyboardButton('Еще книги этого жанра', callback_data=genre))
    bot.send_photo(message.chat.id, choice[1], choice[2], parse_mode="Markdown", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)

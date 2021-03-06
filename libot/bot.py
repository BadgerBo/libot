import telebot
from flask import Flask, request

from config import TOKEN, URL, SECRET
import parser


bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
url = URL + SECRET
bot.set_webhook(url = url)


app = Flask(__name__)


@app.route('/{}'.format(SECRET) , methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@bot.message_handler(commands=['start'])
def provide_command_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    genres_button = telebot.types.KeyboardButton(text='Genres')
    most_read_button = telebot.types.KeyboardButton(text='Most Read')
    choice_awards_button = telebot.types.KeyboardButton(text='Choice Awards')
    keyboard.row(genres_button)
    keyboard.row(most_read_button, choice_awards_button)
    bot.send_message(message.chat.id,
                     'Greetings, {}\n'.format(message.chat.username) +
                     'I can help you choose your next book\nWhat do you want to read?',
                     parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def provide_command_help(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Contact bot\'s creator', url='https://t.me/BadgerBo'))
    bot.send_message(message.chat.id,
                     'Choose one of the available options:\n1)  Genres\n2)  Most Read\n' +
                     '3)  Choice Awards\n\nThen choose particular genre, duration or year of publication',
                     parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_general_choice(message):
    if message.text == 'Genres':
        provide_genre_choice(message)
    elif message.text == 'Most Read':
        provide_duration_choice(message)
    elif message.text == 'Choice Awards':
        provide_year_choice(message)
    else:
        pass


def provide_genre_choice(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Biography', callback_data='biography'),
        telebot.types.InlineKeyboardButton(text='Children\'s', callback_data='children-s'),
        telebot.types.InlineKeyboardButton(text='Classics', callback_data='classics'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Fantasy', callback_data='fantasy'),
        telebot.types.InlineKeyboardButton(text='Fiction', callback_data='fiction'),
        telebot.types.InlineKeyboardButton(text='Graphic Novels', callback_data='graphic-novels'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Horror', callback_data='horror'),
        telebot.types.InlineKeyboardButton(text='Mystery', callback_data='mystery'),
        telebot.types.InlineKeyboardButton(text='Nonfiction', callback_data='non-fiction'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Poetry', callback_data='poetry'),
        telebot.types.InlineKeyboardButton(text='Romance', callback_data='romance'),
        telebot.types.InlineKeyboardButton(text='Science Fiction', callback_data='science-fiction'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='Thriller', callback_data='thriller'),
        telebot.types.InlineKeyboardButton(text='Travel', callback_data='travel'),
        telebot.types.InlineKeyboardButton(text='Young Adult', callback_data='young-adult'),
    )
    bot.send_message(message.chat.id, 'In which genre do you take an interest?', reply_markup=keyboard)


def provide_duration_choice(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='This Week', callback_data='w'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='This Month', callback_data='m'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='In The Last 12 Months', callback_data='y'),
    )
    bot.send_message(message.chat.id, 'Most Read Books on Goodreads.com', reply_markup=keyboard)


def provide_year_choice(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='2019', callback_data='2019'),
        telebot.types.InlineKeyboardButton(text='2018', callback_data='2018'),
        telebot.types.InlineKeyboardButton(text='2017', callback_data='2017'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='2016', callback_data='2016'),
        telebot.types.InlineKeyboardButton(text='2015', callback_data='2015'),
        telebot.types.InlineKeyboardButton(text='2014', callback_data='2014'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(text='2013', callback_data='2013'),
        telebot.types.InlineKeyboardButton(text='2012', callback_data='2012'),
        telebot.types.InlineKeyboardButton(text='2011', callback_data='2011'),
    )
    bot.send_message(message.chat.id, 'Winners of Annual Goodreads.com Choice Awards', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_choice_of_genre_or_year(call):
    if len(call.data) == 1:
        most_read_book = parser.compile_advice(
            'https://www.goodreads.com/book/most_read?category=all&country=all&duration=' + call.data)
        give_book_advice(call.message, most_read_book, call.data)
    elif call.data.isdigit():
        choice_awards_book = parser.compile_advice('https://www.goodreads.com/choiceawards/best-books-' + call.data)
        give_book_advice(call.message, choice_awards_book, call.data)
    else:
        genre_book = parser.compile_advice('https://www.goodreads.com/shelf/show/' + call.data)
        give_book_advice(call.message, genre_book, call.data)


def give_book_advice(message, book, data):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('View on goodreads.com', url=book[0]))
    if len(data) == 1:
        keyboard.add(telebot.types.InlineKeyboardButton('Another most read book',
                                                        callback_data=data))
    elif data[0].isdigit():
        keyboard.add(telebot.types.InlineKeyboardButton('Another best book of {}'.format(data),
                                                        callback_data=data))
    else:
        keyboard.add(telebot.types.InlineKeyboardButton('Another book of this genre',
                                                        callback_data=data))
    bot.send_photo(message.chat.id, book[1], book[2], parse_mode="Markdown", reply_markup=keyboard)

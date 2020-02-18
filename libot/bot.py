import telebot

from config import token
import parser


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def provide_command_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    genres_button = telebot.types.KeyboardButton(text='Genres')
    random_button = telebot.types.KeyboardButton(text='Most Read')
    choice_awards_button = telebot.types.KeyboardButton(text='Choice Awards')
    new_releases_button = telebot.types.KeyboardButton(text='New Releases')
    keyboard.row(genres_button, random_button)
    keyboard.row(choice_awards_button, new_releases_button)
    bot.send_message(message.chat.id,
                     'Greetings, {}\n'.format(message.chat.username) +
                     'I can help you choose your next book\nWhat do you want to read?',
                     parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def provide_command_help(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Contact bot\'s creator', url='https://t.me/BadgerBo'))
    bot.send_message(message.chat.id,
                     'Choose one of the available options:\n1)  Genres\n2)  Random\n3)  Choice Awards\n' +
                     '4)  New Releases\nThen choose particular genre or year of publication, if necessary',
                     parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_general_choice(message):
    if message.text == 'Genres':
        provide_genre_choice(message)
    elif message.text == 'Most Read':
        provide_duration_choice(message)
    elif message.text == 'Choice Awards':
        provide_year_choice(message)
    elif message.text == 'New Releases':
        try:
            new_releases_book = parser.compile_advice_new_releases()
            give_book_advice(message, new_releases_book, None)
        except:
            new_releases_book = parser.compile_advice_new_releases()
            give_book_advice(message, new_releases_book, None)
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
    bot.send_message(message.chat.id, 'Winners of Annual Goodreads Choice Awards', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_choice_of_genre_or_year(call):
    if call.data[0:1] == '20':
        year = call.data
        try:
            choice_awards_book = parser.compile_advice_choice_awards(year)
            give_book_advice(call.message, choice_awards_book, year)
        except:
            choice_awards_book = parser.compile_advice_choice_awards(year)
            give_book_advice(call.message, choice_awards_book, year)
    elif len(call.data) == 1:
        duration = call.data
        try:
            most_read_book = parser.compile_advice_most_read(duration)
            give_book_advice(call.message, most_read_book, None)
        except:
            most_read_book = parser.compile_advice_most_read(year)
            give_book_advice(call.message, most_read_book, None)
    else:
        genre = call.data
        try:
            genre_book = parser.compile_advice_genre(genre)
            give_book_advice(call.message, genre_book, genre)
        except:
            genre_book = parser.compile_advice_genre(genre)
            give_book_advice(call.message, genre_book, genre)


def give_book_advice(message, book, flag_for_additional_option):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('View on goodreads.com', url=book[0]))
    if flag_for_additional_option is None:
        pass
    elif flag_for_additional_option[0].isalpha():
        keyboard.add(telebot.types.InlineKeyboardButton('Another book of this genre',
                                                        callback_data=flag_for_additional_option))
    elif flag_for_additional_option[0].isdigit():
        keyboard.add(telebot.types.InlineKeyboardButton('Another best book of {}'.format(flag_for_additional_option),
                                                        callback_data=flag_for_additional_option))
    bot.send_photo(message.chat.id, book[1], book[2], parse_mode="Markdown", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)

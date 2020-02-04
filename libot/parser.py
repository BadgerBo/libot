from bs4 import BeautifulSoup
import requests
import random


def get_soup(url):
	raw_html = requests.get(url).content
	return BeautifulSoup(raw_html, "html.parser")


def compile_advice_genre(data):
	'''Жанры'''
	try:
		url_genre = get_page_soup(data)
		soup_of_genre_page = get_soup(url_genre)
		raw_book_html = make_choice_from_page(soup_of_genre_page)
		soup_of_book = get_soup('https://www.livelib.ru/' + raw_book_html)
		description = f'{get_book_title(soup_of_book)}\n\n{get_book_author(soup_of_book)}\n\n{get_book_info(soup_of_book)}\n\n{get_book_rating(soup_of_book)}'
		link = get_book_link(soup_of_book)
		cover = get_book_cover(soup_of_book)
		return link, cover, description
	except:
		compile_advice_genre(data)


def compile_advice_top():
	'''Топ-100'''
	try:
		soup_of_top = get_soup('https://www.livelib.ru/books/top')
		raw_book_html = make_choice_from_page(soup_of_top)
		soup_of_book = get_soup('https://www.livelib.ru/' + raw_book_html)
		description = f'{get_book_title(soup_of_book)}\n\n{get_book_author(soup_of_book)}\n\n{get_book_info(soup_of_book)}\n\n{get_book_top(soup_of_book)}\n{get_book_rating(soup_of_book)}'
		link = get_book_link(soup_of_book)
		cover = get_book_cover(soup_of_book)
		return link, cover, description
	except:
		compile_advice_top()


def compile_advice_random():
	'''Случайный выбор'''
	try:
		soup_of_book = get_soup('https://www.livelib.ru/book/random')
		description = f'{get_book_title(soup_of_book)}\n\n{get_book_author(soup_of_book)}\n\n{get_book_info(soup_of_book)}\n\n{get_book_rating(soup_of_book)}'
		link = get_book_link(soup_of_book)
		cover = get_book_cover(soup_of_book)
		return link, cover, description
	except:
		compile_advice_random()


def get_page_soup(genre):
	'''Жанры - Выбор номера страницы в жанре'''
	page = random.randint(1, 15)
	return f'https://www.livelib.ru/genre/{genre}/best/listview/biglist/~{page}'


def make_choice_from_page(bsoup):
	'''Жанры и Топ-100 - Ссылки на все книги со страницы'''
	list_of_books = []
	for book in bsoup.find_all('a', {'class':"brow-book-name with-cycle"}):
		book = book.get('href')
		list_of_books.append(book)
	return random.choice(list_of_books)


def get_book_link(bsoup):
	return bsoup.find('link', {'rel':"canonical"}).get('href')


def get_book_cover(bsoup):
	raw_cover = bsoup.find('img', {'id':"main-image-book"}).get('src')
	return raw_cover.replace("/200/", "/o/").replace("jpg", "jpeg")


def get_book_title(bsoup):
	raw_title = bsoup.find('span', {'itemprop':"name"}).string
	return f'*{raw_title}*'


def get_book_author(bsoup):
	raw_author = bsoup.find('a', {'id':"book-author"}).get('title')
	return f'Автор:  {raw_author}'


def get_book_info(bsoup):
	raw_info = bsoup.find('table', {'class':"compact"}).get_text().split()
	return f'ISBN:  {raw_info[1]}\nГод издания:  {raw_info[4]}'


def get_book_rating(bsoup):
	raw_rating = bsoup.find('span', {'style':"margin-right: 5px"}).string
	return f'*Средняя оценка:  {raw_rating}*'


def get_book_top(bsoup):
	raw_top = bsoup.find('a', {'class':"label-orange"}).string
	return f'Место в топ-100:  {raw_top[1:3]}'

from bs4 import BeautifulSoup
import requests
import random


class Book:

    def __init__(self, soup):
        self.soup = soup

    def get_url(self):
        return self.soup.find('link', {'rel': "canonical"}).get('href')

    def get_cover(self):
        return self.soup.find('img', {'id': "coverImage"}).get('src')

    def get_description(self):
        title = self.soup.find('h1', {'itemprop': "name"}).get_text().strip('\n ')
        author = self.soup.find('span', {'itemprop': "name"}).get_text()
        rating = self.soup.find('span', {'itemprop': "ratingValue"}).get_text().strip('\n ')
        synopsis = self.soup.find('span', {'style': "display:none"}).get_text()[:150] + '...'
        return '*{}*\nby {}\n\nRating: {}\n\n{}'.format(title, author, rating, synopsis)


def get_full_book_info(book_soup):
    book = Book(book_soup)
    url = book.get_url()
    cover = book.get_cover()
    description = book.get_description()
    return url, cover, description


def get_soup(url):
    raw_html = requests.get(url).content
    return BeautifulSoup(raw_html, "html.parser")


def make_book_choice_from_page(page_soup):
    list_of_books = []
    for book in page_soup.find_all('div', {'class': "stars"}):
        book = book.get('data-resource-id')
        list_of_books.append(book)
    return random.choice(list_of_books)


def compile_advice_genre(genre):
    soup_of_genre_page = get_soup('https://www.goodreads.com/shelf/show/' + genre)
    book_link = make_book_choice_from_page(soup_of_genre_page)
    soup_of_book = get_soup('https://www.goodreads.com/book/show/' + book_link)
    full_book_info = get_full_book_info(soup_of_book)
    return full_book_info


def compile_advice_most_read(duration):
    soup_of_most_read_page = get_soup('https://www.goodreads.com/book/most_read?category=all&country=all&duration=' + duration)
    book_link = make_book_choice_from_page(soup_of_most_read_page)
    soup_of_book = get_soup('https://www.goodreads.com/book/show/' + book_link)
    full_book_info = get_full_book_info(soup_of_book)
    return full_book_info


def compile_advice_choice_awards(year):
    soup_of_year_page = get_soup('https://www.goodreads.com/choiceawards/best-books-' + year)
    book_link = make_book_choice_from_page(soup_of_year_page)
    soup_of_book = get_soup('https://www.goodreads.com/book/show/' + book_link)
    full_book_info = get_full_book_info(soup_of_book)
    return full_book_info


def compile_advice_new_releases():
    soup_of_genre_page = get_soup('https://www.goodreads.com/book/popular_by_date/')
    book_link = make_book_choice_from_page(soup_of_genre_page)
    soup_of_book = get_soup('https://www.goodreads.com/book/show/' + book_link)
    full_book_info = get_full_book_info(soup_of_book)
    return full_book_info

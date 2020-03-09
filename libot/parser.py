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


def get_soup(url):
    raw_html = requests.get(url).content
    return BeautifulSoup(raw_html, "html.parser")


def make_book_choice_from_page(page_soup):
    list_of_books = []
    for book in page_soup.find_all('div', {'class': "stars"}):
        book = book.get('data-resource-id')
        list_of_books.append(book)
    return random.choice(list_of_books)


def compile_advice(general_url):
    soup_of_page = get_soup(general_url)
    book_id = make_book_choice_from_page(soup_of_page)
    soup_of_book = get_soup('https://www.goodreads.com/book/show/' + book_id)
    book = Book(soup_of_book)
    url = book.get_url()
    cover = book.get_cover()
    description = book.get_description()
    return url, cover, description

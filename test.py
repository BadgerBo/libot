import unittest

from libot.parser import get_soup, make_book_choice_from_page, compile_advice


class TestParser(unittest.TestCase):
    

    def test_get_soup(self):
        soup_of_page = get_soup('https://www.goodreads.com/')
        self.assertIsNotNone(soup_of_page)


    def test_make_book_choice_from_page(self):
        soup_of_page_with_multiple_books = get_soup('https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century')
        soup_of_page_with_single_book = get_soup('https://www.goodreads.com/book/show/18405.Gone_with_the_Wind')
        book_choice_from_page_with_multiple_books = make_book_choice_from_page(soup_of_page_with_multiple_books)
        book_choice_from_page_with_single_book = make_book_choice_from_page(soup_of_page_with_single_book)
        self.assertIsNotNone(book_choice_from_page_with_multiple_books)
        self.assertTrue(book_choice_from_page_with_multiple_books.isdigit())
        self.assertEqual(book_choice_from_page_with_single_book, '18405')


    def test_compile_advice(self):
        url_of_page_with_multiple_books = 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century'
        url_of_page_with_single_book = 'https://www.goodreads.com/book/show/18405.Gone_with_the_Wind'
        compile_advice_from_page_with_multiple_books = compile_advice(url_of_page_with_multiple_books)
        compile_advice_from_page_with_single_book = compile_advice(url_of_page_with_single_book)
        self.assertIsNotNone(compile_advice_from_page_with_multiple_books)
        self.assertEqual(compile_advice_from_page_with_single_book, (
            'https://www.goodreads.com/book/show/18405.Gone_with_the_Wind', 
            'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1551144577l/18405._SY475_.jpg', '*Gone with the Wind*\nby Margaret Mitchell\n\nRating: 4.29\n\nIt takes guts to make your main character spoiled, selfish, and stupid, someone without any redeeming qualities, and write an epic novel about her. Bu...'))



if __name__ == '__main__':
    unittest.main()

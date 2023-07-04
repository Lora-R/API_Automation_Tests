import unittest
from api.user import UserAPI
from api.books import BookStoreAPI
from data_structure.test_data import TestData


class TestBookFavourite(unittest.TestCase):
    api_user = None
    api_book_store = None
    data_body = None
    token = None

    @classmethod
    def setUpClass(cls):
        cls.api_user = UserAPI()
        cls.api_book_store = BookStoreAPI()

        cls.user_id = "3e9dfe16-a1fc-447e-aabc-644da3b9393e"
        cls.data_body = {
            "userName": "Admin111",
            "password": "Password123@"
        }

        cls.token = cls._generate_authorization_token(cls.data_body)

        cls.api_user.headers["Authorization"] = f"Bearer {cls.token}"
        cls.api_book_store.headers["Authorization"] = f"Bearer {cls.token}"

        cls.data_body = None

    @staticmethod
    def _generate_authorization_token(data_body):
        token_response = TestBookFavourite.api_user.generate_token(data_body)
        return token_response["token"]

    def setUp(self):
        self.test_data = TestData(self.user_id, self.api_user, self.api_book_store)
        self.test_data.clear_user_book_list()

    # 3. От списъка с всички книги, да се избере една и да се добави към предпочитаните книги (колекция).
    # Да се валидира, че книгата е добавена.
    def test_choose_book_from_the_list_with_all_books_add_it_to_favourites_validate_its_added(self):
        book = self.api_book_store.get_all_books()["books"][0]
        response = self.test_data.add_book_to_favourite(book["isbn"])
        self.assertEqual(response["books"][0]["isbn"], book["isbn"])
        self.assertTrue(self.test_data.is_book_in_user_favourite(book["isbn"]))

    # 4. Към списъка с предпочитаните книги (колекция) да се добави книга с несъществуващ номер (isbn).
    # Да се валидира грешката.
    def test_add_not_existing_book_to_favourites_validate_error(self):
        isbn_id = "123123123"
        response = self.test_data.add_book_to_favourite(isbn_id)

        self.assertEqual(response["code"], "1205")
        self.assertEqual(response["message"], "ISBN supplied is not available in Books Collection!")
        self.assertEqual(self.test_data.get_user_favourites_book_list(), [])

    # 5. От списъка с всички книги, да се избере друга книга, която да замени първата в списъка с предпочитаните
    # книги (колекция). Да се валидира, че книгата е сменена.
    def test_replace_book_in_favourites_with_another_book_from_list_with_all_books(self):
        book_1 = self.api_book_store.get_all_books()["books"][0]
        book_2 = self.api_book_store.get_all_books()["books"][3]

        self.test_data.add_book_to_favourite(book_1["isbn"])
        self.test_data.replace_book_in_favourite(book_1["isbn"], book_2["isbn"])
        self.assertTrue(self.test_data.is_book_in_user_favourite(book_2["isbn"]))

    # 6. Да се валидира, че книга с номер (isbn) 9781491904244 има 278 страници.
    def test_validate_the_amount_of_pages_of_book_with_id_9781491904244(self):
        # Get the book by ID to check its pages amount
        isbn_id = "9781491904244"
        book = self.api_book_store.get_single_book_from_books_list(isbn_id)
        pages = book["pages"]

        self.assertEqual(pages, 278)

    # 7. # Да се премахне книгата от списъка с предпочитаните книги (колекция). Да се валидира, че книгата е премахната.
    def test_remove_book_from_favourites_validate_its_removed(self):
        # Add a book to the user's favourites
        book = self.api_book_store.get_all_books()["books"][0]
        response = self.test_data.add_book_to_favourite(book["isbn"])
        self.assertEqual(response["books"][0]["isbn"], book["isbn"])

        # Assert that the added book is in the user's book list
        self.assertTrue(self.test_data.is_book_in_user_favourite(book["isbn"]))

        # Remove the book from favourites
        response = self.test_data.remove_book_from_favourite(book["isbn"])
        self.assertEqual(response.status_code, 204)

        self.assertFalse(self.test_data.is_book_in_user_favourite(book["isbn"]))

    # 8. От списъка с предпочитаните книги (колекция), да се премахне книга, която не е добавена към него.
    # Да се валидира грешката.
    def test_remove_book_that_is_not_added_from_favourites_validate_error(self):
        # Get the first book from the available books
        book = self.api_book_store.get_all_books()["books"][0]

        # Remove the book from favourites
        response = self.test_data.remove_book_from_favourite(book["isbn"])

        # Verify the response code and message
        self.assertEqual(response["code"], "1206")
        self.assertEqual(response["message"], "ISBN supplied is not available in User's Collection!")

    def tearDown(self):
        self.test_data.clear_user_book_list()

    @classmethod
    def tearDownClass(cls):
        cls.api_user.headers["Authorization"] = None
        cls.api_book_store.headers["Authorization"] = None


if __name__ == "__main__":
    unittest.main()

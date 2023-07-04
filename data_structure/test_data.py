import string
import random


class TestData:
    def __init__(self, user_id, api_user, api_book_store):
        self.user_id = user_id
        self.api_user = api_user
        self.api_book_store = api_book_store

    @staticmethod
    def randomize_entry_for_request_body():
        # Define the character sets for different password criteria
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        # part of the special characters are not accepted, therefore I decided to use just some of them
        special_characters = '!#$%&*'

        valid_password = random.choice(lowercase_letters) + random.choice(uppercase_letters) + random.choice(
            digits) + random.choice(special_characters)
        remaining_length = 8 - len(valid_password)
        valid_password += ''.join(
            random.choices(string.ascii_letters + string.digits, k=remaining_length))
        password_only_special_chars = ''.join(random.choice(special_characters) for _ in range(8))
        valid_user_name = ''.join(random.choices(string.ascii_letters + string.digits, k=11))

        # Generate individual invalid passwords for each type of validation
        dict_field_entry = {
            "valid_password": valid_password,
            "pass_invalid_no_lowercase": valid_password.upper(),
            "pass_invalid_no_uppercase": valid_password.lower(),
            "pass_invalid_only_special_char": password_only_special_chars,
            "pass_invalid_no_digit": ''.join(char if char not in digits else random.choice(uppercase_letters) for char in valid_password),
            "pass_invalid_no_special_char": ''.join(char if char not in special_characters else random.choice(lowercase_letters) for char in valid_password),
            "pass_invalid_short_length": valid_password[:7],
            "valid_username": valid_user_name
        }

        return dict_field_entry

    @staticmethod
    def structure_data_body(user_name, password):
        data_body = {
            "userName": f'{user_name}',
            "password": f'{password}'
        }

        return data_body

    def add_book_to_favourite(self, isbn):
        body_add_list_books = {
            "userId": self.user_id,
            "collectionOfIsbns": [
                {"isbn": isbn}
            ]
        }
        return self.api_book_store.add_list_of_books(body_add_list_books)

    def replace_book_in_favourite(self, old_isbn, new_isbn):
        request_replace_body = {
            "userId": self.user_id,
            "isbn": new_isbn
        }
        return self.api_book_store.put_replace_book_in_a_users_favorite_list(request_replace_body, old_isbn)

    def is_book_in_user_favourite(self, isbn):
        user = self.api_user.get_user(self.user_id)
        book_list = user["books"]
        return any(b["isbn"] == isbn for b in book_list)

    def get_user_favourites_book_list(self):
        user = self.api_user.get_user(self.user_id)
        return user["books"]

    def clear_user_book_list(self):
        self.api_book_store.delete_all_books_from_users_favourite_list(self.user_id)

    def remove_book_from_favourite(self, isbn):
        user_isbn_id_body = {
            "isbn": isbn,
            "userId": self.user_id
        }
        response = self.api_book_store.delete_single_book_from_users_favourite_list(user_isbn_id_body)

        return response

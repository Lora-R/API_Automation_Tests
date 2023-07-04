import requests


class BookStoreAPI:
    base_url = "https://url.com/Books/"
    headers = {
        'Content-Type': 'application/json'
    }

    def get_all_books(self):
        url = f"{self.base_url}/Books"
        response = requests.get(url)
        return response.json()

    def add_list_of_books(self, body_add_list_books):
        url = f"{self.base_url}/Books"
        response = None
        try:
            response = requests.post(url, json=body_add_list_books, headers=BookStoreAPI.headers)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def delete_all_books_from_users_favourite_list(self, user_id):
        url = f"{self.base_url}/Books?UserId={user_id}"
        response = requests.delete(url, headers=BookStoreAPI.headers)
        return response

    def get_single_book_from_books_list(self, isbn_id):
        url = f"{self.base_url}/Book?ISBN={isbn_id}"
        response = None
        try:
            response = requests.get(url, headers=BookStoreAPI.headers)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def delete_single_book_from_users_favourite_list(self, isbn_user_id_body):
        url = f"{self.base_url}/Book"
        response = None
        try:
            response = requests.delete(url, json=isbn_user_id_body, headers=BookStoreAPI.headers)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def put_replace_book_in_a_users_favorite_list(self, isbn_user_id_body, isbn_new_id):
        url = f'{self.base_url}/Books/{isbn_new_id}'
        response = None
        try:
            response = requests.put(url, json=isbn_user_id_body, headers=BookStoreAPI.headers)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response


book_store = BookStoreAPI()

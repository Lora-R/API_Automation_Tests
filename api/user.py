import requests


class UserAPI:
    base_url = "https://url.com/Users/"
    headers = {
        'Content-Type': 'application/json'
    }

    def create_user(self, data_body):
        url = f"{self.base_url}/User"
        response = None
        try:
            response = requests.post(url, json=data_body)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def generate_token(self, data_body):
        url = f"{self.base_url}/GenerateToken"
        response = None
        try:
            response = requests.post(url, data_body)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def authorize_user(self, data_body):
        url = f"{self.base_url}/Authorized"
        response = None
        try:
            response = requests.post(url, data_body)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def get_user(self, user_id):
        url = f"{self.base_url}/User/{user_id}"
        response = None
        try:
            response = requests.get(url, headers=UserAPI.headers)
            return response.json()
        except requests.exceptions.RequestException as ex:
            return response

    def delete_user(self, user_id):
        url = f"{self.base_url}/User/{user_id}"
        response = requests.delete(url, headers=UserAPI.headers)
        return response


user_api = UserAPI()

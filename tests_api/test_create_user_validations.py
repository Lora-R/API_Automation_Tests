import unittest
from api.user import UserAPI
from data_structure.test_data import TestData


class TestCreateUserValidations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_user = UserAPI()
        cls.api_book_store = None
        cls.user_id = None

    def setUp(self):
        self.test_data = TestData(self.user_id, self.api_user, self.api_book_store)
        self.created_user_id = None
        self.data_body = None

    def assert_code_and_message_of_response_for_invalid_password(self, response):
        self.assertEqual(response["code"], "1300")
        self.assertEqual(response["message"], "Passwords must have at least one non alphanumeric character, one digit "
                                              "('0'-'9'), one uppercase ('A'-'Z'), one lowercase ('a'-'z'), one special"
                                              " character and Password must be eight characters or longer.")

    def test_create_user_missing_parameters(self):
        self.data_body = {
            "userName": "",
            "password": ""
        }
        response = self.api_user.create_user(self.data_body)
        self.assertEqual(response["code"], "1200")
        self.assertEqual(response["message"], "UserName and Password required.")

    def test_create_already_existing_user(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        self.data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                            dict_field_entry["valid_password"])
        # First, create the user
        response = self.api_user.create_user(self.data_body)
        self.assertEqual(len(response), 3)
        self.created_user_id = response["userID"]

        # Then, try to create the same user again
        response = self.api_user.create_user(self.data_body)
        self.assertEqual(response["code"], "1204")
        self.assertEqual(response["message"], "User exists!")

    def test_create_user_with_wrong_end_point(self):
        data_body = {
            "userName": "Test1",
            "password": "@Password123"
        }
        # Use a wrong endpoint URL to simulate the error
        self.api_user.base_url = "https://url.com/Account/v1/WrongEndpoint"
        response = self.api_user.create_user(data_body)
        self.assertEqual(response.status_code, 404)

    def test_create_user_invalid_password_non_special_character(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                       dict_field_entry["pass_invalid_no_special_char"])
        response = self.api_user.create_user(data_body)
        self.assert_code_and_message_of_response_for_invalid_password(response)

    def test_create_user_invalid_password_non_alphanumeric_character(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                       dict_field_entry["pass_invalid_only_special_char"])
        response = self.api_user.create_user(data_body)
        self.assert_code_and_message_of_response_for_invalid_password(response)

    def test_create_user_invalid_password_non_digit(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                       dict_field_entry["pass_invalid_no_digit"])
        response = self.api_user.create_user(data_body)
        self.assert_code_and_message_of_response_for_invalid_password(response)

    def test_create_user_invalid_password_non_uppercase(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                       dict_field_entry["pass_invalid_no_uppercase"])
        response = self.api_user.create_user(data_body)
        self.assertEqual(response["code"], "1300")
        self.assert_code_and_message_of_response_for_invalid_password(response)

    def test_create_user_invalid_password_non_lowercase(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                       dict_field_entry["pass_invalid_no_lowercase"])
        response = self.api_user.create_user(data_body)
        self.assert_code_and_message_of_response_for_invalid_password(response)

    def test_create_user_invalid_password_less_than_eight_character_longer(self):
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                       dict_field_entry["pass_invalid_short_length"])
        response = self.api_user.create_user(data_body)
        self.assert_code_and_message_of_response_for_invalid_password(response)

    def tearDown(self):
        if self.created_user_id is not None:
            token_response = self.api_user.generate_token(self.data_body)
            token = token_response["token"]
            self.api_user.headers["Authorization"] = f"Bearer {token}"
            self.api_user.authorize_user(self.data_body)
            self.api_user.delete_user(self.created_user_id)
            self.data_body = None

    @classmethod
    def tearDownClass(cls):
        print("Test Completed")


if __name__ == "__main__":
    unittest.main()


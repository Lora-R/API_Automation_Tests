import unittest
from api.user import UserAPI
from data_structure.test_data import TestData


class TestCreatedUserSuccessfully(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_user = UserAPI()
        cls.api_book_store = None
        cls.user_id = None

    def setUp(self):
        self.test_data = TestData(self.user_id, self.api_user, self.api_book_store)
        self.created_user_id = None
        self.data_body = None

    def test_create_user_successfully_and_validate_its_created(self):
        # Randomize userName and password and create a user
        dict_field_entry = self.test_data.randomize_entry_for_request_body()
        self.data_body = self.test_data.structure_data_body(dict_field_entry["valid_username"],
                                                            dict_field_entry["valid_password"])
        response = self.api_user.create_user(self.data_body)

        self.assertIn("userID", response)
        self.assertIn("username", response)
        self.assertIn("books", response)
        self.created_user_id = response["userID"]

        # Authorize the created user
        token_response = self.api_user.generate_token(self.data_body)
        token = token_response["token"]
        self.api_user.headers["Authorization"] = f"Bearer {token}"
        self.api_user.authorize_user(self.data_body)

        response_get_user = self.api_user.get_user(self.created_user_id)

        self.assertEqual(len(response), 3)
        self.assertEqual(response_get_user["userId"], self.created_user_id)
        self.api_user.delete_user(self.created_user_id)

    def tearDown(self):
        if self.created_user_id is not None:
            self.data_body = None

    @classmethod
    def tearDownClass(cls):
        UserAPI.headers["Authorization"] = ""


if __name__ == "__main__":
    unittest.main()

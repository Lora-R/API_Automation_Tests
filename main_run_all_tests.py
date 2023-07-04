import os
import unittest
import HtmlTestRunner

from tests_api.test_create_user_validations import TestCreateUserValidations
from tests_api.test_create_user_and_validate_its_created import TestCreatedUserSuccessfully
from tests_api.tests_favorite_books_validations import TestBookFavourite


class TestRunner:
    @staticmethod
    def clear_reports_folder():
        reports_folder = os.path.join(os.getcwd(), "reports")
        for filename in os.listdir(reports_folder):
            file_path = os.path.join(reports_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def run_tests():
        # Create a test suite
        test_suite = unittest.TestSuite()

        # Add the test cases from each test file to the test suite
        test_suite.addTest(unittest.makeSuite(TestBookFavourite))
        test_suite.addTest(unittest.makeSuite(TestCreateUserValidations))
        test_suite.addTest(unittest.makeSuite(TestCreatedUserSuccessfully))

        # Define the output file path for the HTML report
        report_file = "reports"

        # Clear the files in the reports folder
        TestRunner.clear_reports_folder()

        # Create an HTMLTestRunner instance with the output file
        html_runner = HtmlTestRunner.HTMLTestRunner(output=report_file)

        # Run the test suite using the HTMLTestRunner
        html_runner.run(test_suite)


if __name__ == '__main__':
    TestRunner.run_tests()

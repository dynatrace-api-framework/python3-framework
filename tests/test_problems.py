"""Test Suite for the Extensions API"""
import unittest
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.framework.request_handler import TenantAPIs, HTTP
from dynatrace.tenant import problems

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.PROBLEMS)
PROBLEM_ID = "-123456789_987654321V2"
COMMENT_ID = "123456789"
REQUEST_DIR = "tests/mockserver_payloads/requests/problems"
RESPONSE_DIR = "tests/mockserver_payloads/responses/problems"


class TestGetProblems(unittest.TestCase):
    """Test cases for fetching problems, comments, and their details"""

    def test_get_all_problems(self):
        """Tests fetching all problems in a tenant"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            response_file=response_file,
            request_type=str(HTTP.GET)
        )

        result = problems.get_all_problems(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('problems')

        self.assertEqual(result, expected_result)

    def test_get_problem_details(self):
        """Tests fetching the details of a single problem"""
        response_file = f"{RESPONSE_DIR}/get_one.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}",
            response_file=response_file,
            request_type=str(HTTP.GET)
        )

        result = problems.get_problem_details(CLUSTER, TENANT, PROBLEM_ID)
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)

    def test_get_problem_count(self):
        """Tests fetching the total number of problems"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            response_file=response_file,
            request_type=str(HTTP.GET)
        )

        result = problems.get_problem_count(CLUSTER, TENANT)
        expected_result = 2

        self.assertEqual(result, expected_result)

    def test_get_all_comments(self):
        """Tests fetching all comments of a problem"""
        response_file = f"{RESPONSE_DIR}/get_comments.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}/comments",
            response_file=response_file,
            request_type=str(HTTP.GET)
        )

        result = problems.get_all_comments(CLUSTER, TENANT, PROBLEM_ID)
        expected_result = testtools.expected_payload(response_file).get('comments')

        self.assertEqual(result, expected_result)

    def test_get_comment_details(self):
        """Tests fetching a single comment of a problem"""
        response_file = f"{RESPONSE_DIR}/get_comment.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}/comments/{COMMENT_ID}",
            response_file=response_file,
            request_type=str(HTTP.GET)
        )

        result = problems.get_comment(CLUSTER, TENANT, PROBLEM_ID, COMMENT_ID)
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)


class TestModifyProblems(unittest.TestCase):
    """Test cases for making changes to problems and comments"""

    def test_close_problem(self):
        """Tests the manual closing of a problem"""
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}/close",
            response_code=204,
            request_type=str(HTTP.POST)
        )

        result = problems.close_problem(
            CLUSTER, TENANT, PROBLEM_ID
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_add_comment(self):
        """Tests adding a comment to a problem"""
        request_file = f"{REQUEST_DIR}/comment.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}/comments",
            request_file=request_file,
            response_code=201,
            request_type=str(HTTP.POST)
        )

        result = problems.add_comment(
            cluster=CLUSTER,
            tenant=TENANT,
            problem_id=PROBLEM_ID,
            message="Test comment",
            context="Test"
        ). status_code
        expected_result = 201

        self.assertEqual(result, expected_result)

    def test_update_comment_with_data(self):
        """Tests updating an existing comment of problem.
        Comment and context provided.
        """
        request_file = f"{REQUEST_DIR}/updated_comment.json"
        message = "updated comment"
        context = "test_context"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}/comments/{COMMENT_ID}",
            request_file=request_file,
            response_code=204,
            request_type=str(HTTP.PUT)
        )

        result = problems.update_comment(
            CLUSTER, TENANT, PROBLEM_ID, COMMENT_ID,
            message=message, context=context
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_delete_comment(self):
        """Tests deleting a comment from a problem"""
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{PROBLEM_ID}/comments/{COMMENT_ID}",
            request_type=str(HTTP.DELETE),
            response_code=204
        )

        result = problems.delete_comment(
            CLUSTER, TENANT, PROBLEM_ID, COMMENT_ID
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()

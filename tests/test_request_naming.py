"""Test suite for request_naming"""

import unittest
import tests.tooling_for_test as testtools
from user_variables import FULL_SET
from dynatrace.framework.request_handler import TenantAPIs, HTTP
from dynatrace.tenant import request_naming

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.REQUEST_NAMING)
RULE_ID = "abc1234def-1233-3321-ab123-abc123defghi"
REQUEST_DIR = "tests/mockserver_payloads/requests/request_naming"
RESPONSE_DIR = "tests/mockserver_payloads/responses/request_naming"


class TestRequest_Naming(unittest.TestCase):
    """Test cases for main functionality of the request_naming module"""

    def test_create_naming_rule(self):
        """Tests the create_naming_rule function"""
        request_file = f"{REQUEST_DIR}/definition.json"
        rule_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.POST),
            response_code=201,
            request_file=request_file
        )

        result = request_naming.create_naming_rule(CLUSTER, TENANT, rule_json).status_code
        expected_result = 201

        self.assertEqual(result, expected_result)

    def test_delete_naming_rule(self):
        """Tests the delete_naming_rule function"""

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RULE_ID}",
            request_type=str(HTTP.DELETE),
            response_code=204
        )

        result = request_naming.delete_naming_rule(CLUSTER, TENANT, RULE_ID).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_export_to_files(self):
        """Tests the export_to_files function"""
        response_file1 = f"{RESPONSE_DIR}/get_all.json"
        response_file2 = f"{RESPONSE_DIR}/get_one.json"
        rules_list = testtools.expected_payload(response_file1).get("values")
        rule_json = testtools.expected_payload(response_file2)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file1,
            mock_id="Req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RULE_ID}",
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file2,
            mock_id="Req2"
        )

        request_naming.export_to_files(CLUSTER, TENANT, RESPONSE_DIR)
        file = f"{rules_list[0].get('name')}.json"
        expected_file = 

        self.assertEqual(result, expected_result)

    def test_get_all_rules(self):
        """Tests the get_all_rules function"""
        request_file = f"{REQUEST_DIR}/[req_file].json"
        response_file = f"{RESPONSE_DIR}/[res_file].json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            request_file=request_file,
            response_file=response_file
        )

        result = request_naming.get_all_rules(CLUSTER, TENANT)
        expected_result = None

        self.assertEqual(result, expected_result)

    def test_get_rule_details(self):
        """Tests the get_rule_details function"""
        request_file = f"{REQUEST_DIR}/[req_file].json"
        response_file = f"{RESPONSE_DIR}/[res_file].json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{rule_id}",
            request_type=str(HTTP.GET),
            response_code=200,
            request_file=request_file,
            response_file=response_file
        )

        result = request_naming.get_rule_details(CLUSTER, TENANT, RULE_ID)
        expected_result = None

        self.assertEqual(result, expected_result)

    def test_update_naming_rule(self):
        """Tests the update_naming_rule function"""
        request_file = f"{REQUEST_DIR}/[req_file].json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{rule_id}",
            request_type=str(HTTP.PUT),
            response_code=204,
            request_file=request_file
        )

        result = request_naming.update_naming_rule(CLUSTER, TENANT, RULE_ID, RULE_JSON)
        expected_result = None

        self.assertEqual(result, expected_result)


class TestErrorHandling(unittest.TestCase):
    def test_export_to_files_RuntimeError(self):
        """Tests error handling for function export_to_files.
        RuntimeError should be raised when when the folder path does not exist.
        """
        with self.assertRaises(RuntimeError):
            request_naming.export_to_files(CLUSTER, TENANT, FOLDER)


if __name__ == "__main__":
    unittest.main()

"""Test suite for request_attributes"""

import unittest
import os
import tests.tooling_for_test as testtools
from user_variables import FULL_SET
from dynatrace.framework.request_handler import TenantAPIs, HTTP
from dynatrace.tenant import request_attributes

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.REQUEST_ATTRIBUTES)
RA_ID = "123abc456-a123-1234-4321-def123ghi45"
RA_NAME = "Mock_ReqAttr_1"
REQUEST_DIR = "tests/mockserver_payloads/requests/request_attributes"
RESPONSE_DIR = "tests/mockserver_payloads/responses/request_attributes"


class TestRequestAttributes(unittest.TestCase):
    """Test cases for main functionality of the request_attributes module"""

    def test_create_or_update_request_attribute_u(self):
        """Tests the create_or_update_request_attribute function.
        Test the update portion of this function.
        """
        request_file = f"{REQUEST_DIR}/updated.json"
        response_file = f"{RESPONSE_DIR}/get_all.json"
        ra_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file,
            mock_id="Req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RA_ID}",
            request_type=str(HTTP.PUT),
            response_code=204,
            request_file=request_file,
            mock_id="Req2"
        )

        result = request_attributes.create_or_update_request_attribute(
            CLUSTER, TENANT, ra_json
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_create_or_update_request_attribute_c(self):
        """Tests the create_or_update_request_attribute function.
        Test the create portion of this function.
        """
        request_file = f"{REQUEST_DIR}/definition.json"
        response_file = f"{RESPONSE_DIR}/get_all.json"
        ra_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file,
            mock_id="Req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.POST),
            response_code=201,
            request_file=request_file,
            mock_id="Req2"
        )

        result = request_attributes.create_or_update_request_attribute(
            CLUSTER, TENANT, ra_json
        ).status_code
        expected_result = 201

        self.assertEqual(result, expected_result)

    def test_create_request_attribute(self):
        """Tests the create_request_attribute function"""
        request_file = f"{REQUEST_DIR}/definition.json"
        ra_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.POST),
            response_code=201,
            request_file=request_file
        )

        result = request_attributes.create_request_attribute(
            CLUSTER, TENANT, ra_json
        ).status_code
        expected_result = 201

        self.assertEqual(result, expected_result)

    def test_delete_request_attribute_by_id(self):
        """Tests the delete_request_attribute_by_id function"""
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RA_ID}",
            request_type=str(HTTP.DELETE),
            response_code=204
        )

        result = request_attributes.delete_request_attribute_by_id(
            CLUSTER, TENANT, RA_ID
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_delete_request_attribute_by_name(self):
        """Tests the delete_request_attribute_by_name function"""
        response_file = f"{RESPONSE_DIR}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file,
            mock_id="Req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RA_ID}",
            request_type=str(HTTP.DELETE),
            response_code=204,
            mock_id="Req2"
        )

        result = request_attributes.delete_request_attribute_by_name(
            CLUSTER, TENANT, RA_NAME
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_export_to_files(self):
        """Tests the export_to_files function"""
        response_file1 = f"{RESPONSE_DIR}/get_all_one.json"
        response_file2 = f"{RESPONSE_DIR}/get_one.json"
        folder = RESPONSE_DIR

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
            url_path=f"{URL_PATH}/{RA_ID}",
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file2,
            mock_id="Req2"
        )

        request_attributes.export_to_files(CLUSTER, TENANT, folder)
        file = os.path.exists(f"{RESPONSE_DIR}/{RA_NAME}.json")
        expected_file = True
        file_data = testtools.expected_payload(f"{RESPONSE_DIR}/{RA_NAME}.json")
        expected_file_data = testtools.expected_payload(response_file2)

        self.assertEqual(file, expected_file)
        self.assertEqual(file_data, expected_file_data)

    def test_get_all_request_attributes(self):
        """Tests the get_all_request_attributes function"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file
        )

        result = request_attributes.get_all_request_attributes(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get("values")

        self.assertEqual(result, expected_result)

    def test_get_request_attribute_details(self):
        """Tests the get_request_attribute_details function"""
        response_file = f"{RESPONSE_DIR}/get_one.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RA_ID}",
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file
        )

        result = request_attributes.get_request_attribute_details(
            CLUSTER, TENANT, RA_ID
        )
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)

    def test_get_request_attribute_id(self):
        """Tests the get_request_attribute_id function"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file
        )

        result = request_attributes.get_request_attribute_id(CLUSTER, TENANT, RA_NAME)
        expected_result = RA_ID

        self.assertEqual(result, expected_result)

    def test_update_request_attribute(self):
        """Tests the update_request_attribute function"""
        request_file = f"{REQUEST_DIR}/updated.json"
        ra_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{RA_ID}",
            request_type=str(HTTP.PUT),
            response_code=204,
            request_file=request_file
        )

        result = request_attributes.update_request_attribute(
            CLUSTER, TENANT, RA_ID, ra_json
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)


class TestErrorHandling(unittest.TestCase):
    """Tests Request Attribute Error Handling"""
    def test_delete_request_attribute_by_name_runtime_error(self):
        """Tests error handling for function delete_request_attribute_by_name.
        RuntimeError should be raised when request attribute ID is not found.
        """
        response_file = f"{RESPONSE_DIR}/get_all.json"
        ra_name = "invalid_name"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_code=200,
            response_file=response_file
        )

        with self.assertRaises(RuntimeError):
            request_attributes.delete_request_attribute_by_name(CLUSTER, TENANT, ra_name)

    def test_export_to_files_runtime_error(self):
        """Tests error handling for function export_to_files.
        RuntimeError should be raised when export folder does not exist.
        """
        folder = "invalid_folder/path"

        with self.assertRaises(RuntimeError):
            request_attributes.export_to_files(CLUSTER, TENANT, folder)


if __name__ == "__main__":
    unittest.main()

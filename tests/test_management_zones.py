"""Test Suite for Management Zone operations"""

import unittest
import tests.tooling_for_test as testtools
from dynatrace.tenant import management_zones
from dynatrace.framework.settings import get_cluster_dict
from dynatrace.framework.request_handler import TenantAPIs, HTTP

CLUSTER = get_cluster_dict("mockserver1")
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.MANAGEMENT_ZONES)
RESPONSE_DIR = "tests/mockserver_payloads/responses/management_zones"
REQUEST_DIR = "tests/mockserver_payloads/requests/management_zones"
MZ_ID = "1234567890"
MZ_NAME = "Mock_MZ"
TAGS = [("CONTEXTLESS", "Application", "DemoApp")]


class TestUtils(unittest.TestCase):
    """Test cases for utility functions, separate from API"""

    def test_rule_types_enum(self):
        """Tests the RuleTypes enum. Must return object name"""
        result = str(management_zones.RuleTypes.HTTP_MONITOR)
        expected_result = management_zones.RuleTypes.HTTP_MONITOR.name

        self.assertEqual(result, expected_result)

    def test_generate_template(self):
        """Tests generating a standard MZ template"""
        mz_json_file = f"{RESPONSE_DIR}/get_mz.json"

        result = management_zones.generate_mz_template(MZ_NAME, TAGS)
        expected_result = testtools.expected_payload(mz_json_file)

        self.assertEqual(result, expected_result)

    def test_import_mz_from_file(self):
        """Tests importing a MZ JSON from file"""
        mz_json_file = f"{RESPONSE_DIR}/get_mz.json"

        result = management_zones.import_mz_from_file(mz_json_file)
        expected_result = testtools.expected_payload(mz_json_file)

        self.assertEqual(result, expected_result)


class TestFetchingMZs(unittest.TestCase):
    """Test cases for fetching Management Zones and their details"""

    def test_get_all_management_zones(self):
        """Tests fetching all the Managment Zones in the tenant"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = management_zones.get_all_management_zones(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get("values")

        self.assertEqual(result, expected_result)

    def test_get_management_zone_details(self):
        """Tests fetching the details of a management zone."""
        response_file = f"{RESPONSE_DIR}/get_mz.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{MZ_ID}",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = management_zones.get_management_zone_details(CLUSTER, TENANT, MZ_ID)
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)

    def test_get_management_zone_id(self):
        """Tests fetching the ID for a Management Zone referenced by name"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = management_zones.get_management_zone_id(CLUSTER, TENANT, MZ_NAME)
        expected_result = MZ_ID

        self.assertEqual(result, expected_result)


class TestModifyingManagementZones(unittest.TestCase):
    """Test cases for making changes to Management Zones within a tenant"""

    def test_add_management_zone(self):
        """Tests adding a new management zone to a tenant"""
        request_file = f"{REQUEST_DIR}/mz.json"
        response_file = f"{RESPONSE_DIR}/created.json"
        mz_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.POST),
            request_file=request_file,
            response_code=201,
            response_file=response_file
        )

        result = management_zones.add_management_zone(CLUSTER, TENANT, mz_json)
        expected_result = MZ_ID

        self.assertEqual(result, expected_result)

    def test_update_management_zone(self):
        """Tests updating an existing Management Zone in a tenant"""
        request_file = f"{REQUEST_DIR}/mz.json"
        mz_json = testtools.expected_payload(request_file)

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{MZ_ID}",
            request_type=str(HTTP.PUT),
            request_file=request_file,
            response_code=201
        )

        result = management_zones.update_management_zone(
            CLUSTER, TENANT, MZ_ID, mz_json
        ).status_code
        expected_result = 201

        self.assertEqual(result, expected_result)

    def test_delete_management_zone_by_id(self):
        """Tests deleting a Management Zone referenced by ID"""
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{MZ_ID}",
            request_type=str(HTTP.DELETE),
            response_code=204
        )

        result = management_zones.delete_management_zone_by_id(
            CLUSTER, TENANT, MZ_ID
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)

    def test_delete_management_zone_by_name(self):
        """Tests deleting a Management Zone referenced by name"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}",
            request_type=str(HTTP.GET),
            response_file=response_file,
            mock_id="Req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{MZ_ID}",
            request_type=str(HTTP.DELETE),
            response_code=204,
            mock_id="Req2"
        )

        result = management_zones.delete_management_zone_by_name(
            CLUSTER, TENANT, MZ_NAME
        ).status_code
        expected_result = 204

        self.assertEqual(result, expected_result)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling within Management Zone operations"""

    def test_generate_template_tags_not_list(self):
        """Tests error handling when generating a standard MZ template.
        Tags must be given as a list object.
        """
        with self.assertRaises(ValueError):
            management_zones.generate_mz_template(MZ_NAME, "wrong_tags")

    def test_generate_template_tags_not_tuples(self):
        """Tests error handling when generating a standard MZ template.
        Tags list must contain only tuples.
        """
        with self.assertRaises(ValueError):
            management_zones.generate_mz_template(MZ_NAME, ["wrong_tags"])

    def test_delete_mz_not_found(self):
        """Tests error handling when deleting a Management Zone by name.
        Management Zone must return an ID.
        """
        wrong_name = "non_existing_mz"
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        with self.assertRaises(RuntimeError):
            management_zones.delete_management_zone_by_name(CLUSTER, TENANT, wrong_name)


if __name__ == "__main__":
    unittest.main()

"""Test Cases For Maintenance Windows."""
import unittest
import user_variables
from tests import tooling_for_test
from dynatrace.tenant import maintenance
from dynatrace.requests.request_handler import TenantAPIs

CLUSTER = user_variables.FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = TenantAPIs.MAINTENANCE_WINDOWS


class TestMaintenanceWindowCreate(unittest.TestCase):
    """Test Cases for Creating a Maintenance Window"""
    REQUEST_DIR = "tests/mockserver_payloads/requests/maintenance/"
    RESPONSE_DIR = "tests/mockserver_payloads/responses/maintenance/"

    def test_create_daily_no_scope(self):
        """
        Testing create daily Maintenance Window with no scope
        """
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_daily_1.json"
        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload Daily",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
            maintenance_schedule,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_daily_single_tag(self):
        """Testing create daily Maintenance Window with a single tag scope"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_single_tag_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_daily_1.json"
        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[{'context': "CONTEXTLESS", 'key': "testing"}])
        maintenance_json = maintenance.generate_window_json(
            "Test Payload Daily",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
            maintenance_schedule,
            scope=maintenance_scope,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_daily_tags_and(self):
        """Testing Payloads with multiple tags in an \"AND\" configuration"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_multi_tags_and_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_daily_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[
                {'context': "CONTEXTLESS", 'key': "testing"},
                {'context': "CONTEXTLESS", 'key': "testing2"}
            ],
            match_any_tag=False
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload Daily",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
            maintenance_schedule,
            scope=maintenance_scope,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_daily_tags_or(self):
        """Testing Payloads with multiple tags in an \"AND\" configuration"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_multi_tags_or_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_daily_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[
                {'context': "CONTEXTLESS", 'key': "testing"},
                {'context': "CONTEXTLESS", 'key': "testing2"}
            ],
            match_any_tag=True
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload Daily",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
            maintenance_schedule,
            scope=maintenance_scope,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))


if __name__ == '__main__':
    unittest.main()

# CREATE TESTS LEFT:
# ONCE TEST
# WEEKLY TEST
# MONTHLY TEST

# Single Entity
# Multi Entity
# Single Tag with Filter Type
# Mutli Tags with Filter Type
# Single Tag with Management Zone
# Multi Tags with Management Zone

# EXCEPTION TEST CASES:
# INVALID RECURRENCE
# INVALID WEEK DAY
# INVALID MONTH DAY
# WEEK DAY NOT SUPPLIED
# MONTH DAY NOT SUPPLIED
# MONTHLY DAY OUT OF SCOPE (31 in 30 day month)
# INVALID FILTER_TYPE
# MANAGEMENT_ZONE WITHOUT TAG
# FILTER_TYPE WITHOUT TAG

# OTHER TEST CASES:
# GET ALL WINDOWS
# GET DETAILS OF WINDOW
# DELETE WINDOW
# UPDATE WINDOW

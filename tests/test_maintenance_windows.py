"""
Test Cases For Maintenance Windows.
"""
import unittest
import user_variables
from tests import tooling_for_test
from dynatrace.tenant import maintenance
from dynatrace.requests.request_handler import TenantAPIs

CLUSTER = user_variables.FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = TenantAPIs.MAINTENANCE_WINDOWS


class TestMaintenanceWindowCreate(unittest.TestCase):
    def test_create_daily_no_scope(self):
        """
        Testing create daily Maintenance Window with no scope
        """
        mockserver_expectation_file = "tests/mockserver_expectations/mock_maintenance_create_daily_expectation_1.json"
        mockserver_response_file = "tests/mockserver_expectations/mock_maintenance_create_daily_response_1.json"
        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_payload_file=mockserver_expectation_file,
            response_payload_file=mockserver_response_file,
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
        self.assertEqual(result, tooling_for_test.expected_payload(mockserver_response_file))


if __name__ == '__main__':
    unittest.main()
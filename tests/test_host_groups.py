"""Testing dynatrace.tenant.host_groups"""
import unittest
import user_variables
from tests import tooling_for_test
from dynatrace.tenant import host_groups

CLUSTER = user_variables.FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = "/api/v1/entity/infrastructure/hosts"


class TestHostGroupFunctions(unittest.TestCase):
    RESPONSE_DIR = "tests/mockserver_payloads/responses/host_groups/"

    def test_get_host_groups_tenantwide(self):
        parameters = {
            "relativeTime": ["day"],
            "includeDetails": ["true"],
            "Api-Token": [CLUSTER["api_token"][TENANT]],
        }
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_get_general_1.json"
        tooling_for_test.create_mockserver_expectation(
            CLUSTER, TENANT, URL_PATH, "GET", parameters=parameters, response_file=mockserver_response_file)
        command_tested = host_groups.get_host_groups_tenantwide(
            CLUSTER, TENANT)

        expected_result = {
            'HOST_GROUP-ABCDEFGH12345678': 'HOST_GROUP_1'
        }
        self.assertEqual(command_tested, expected_result)


if __name__ == '__main__':
    unittest.main()

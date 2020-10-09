"""Testing dynatrace.tenant.host_groups"""
import unittest
import user_variables  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.framework.request_handler import TenantAPIs
from dynatrace.tenant.shared import EntityTypes
from dynatrace.tenant import host_groups

CLUSTER = user_variables.FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = f"{TenantAPIs.ENTITIES}"
TYPE = f"{EntityTypes.HOST_GROUP}"


class TestHostGroupFunctions(unittest.TestCase):
    """General Tests for Host Group Functions"""
    RESPONSE_DIR = "tests/mockserver_payloads/responses/host_groups/"

    def test_get_host_groups_tenantwide(self):
        """Testing Retreival of all Host Groups within a single tenant"""
        parameters = {
            "from": "now-24h",
            "entitySelector": f'type("{TYPE}")',
        }
        response_file = f"{self.RESPONSE_DIR}mock_get_general_1.json"
        testtools.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "GET",
            parameters=parameters,
            response_file=response_file
        )
        command_tested = host_groups.get_host_groups_tenantwide(
            CLUSTER, TENANT)

        expected_result = {
            hg.get('entityId'): hg.get('displayName')
            for hg in testtools.expected_payload(response_file).get('entities')
        }
        self.assertEqual(command_tested, expected_result)


if __name__ == '__main__':
    unittest.main()

"""Test suite for Topology Processes"""

import unittest
from tests import tooling_for_test as testtools
from dynatrace import settings
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology.shared import EntityTypes
from dynatrace.tenant.topology import process

FULL_SET = settings.get_setting("FULL_SET")
CLUSTER = FULL_SET.get('mockserver1')
TENANT = 'tenant1'
URL_PATH = f"{TenantAPIs.ENTITIES}"
TYPE = f"{EntityTypes.PROCESS_GROUP_INSTANCE}"
RESPONSE_DIR = "tests/mockserver_payloads/responses/processes"


class TestGetProcesses(unittest.TestCase):
    """Test cases for fetching topology processes."""

    def test_get_all_processes(self):
        """Test getting all processes tenantwide."""
        response_file = f"{RESPONSE_DIR}/get_all_pgis.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'type("{TYPE}")'
            },
            response_file=response_file
        )

        result = process.get_processes_tenantwide(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_single_process(self):
        """Tests getting one specific process."""
        response_file = f"{RESPONSE_DIR}/get_one_pgi.json"
        process_id = "PROCESS_GROUP_INSTANCE-ABC123DEF456GHI7"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'entityId({process_id})'
            },
            response_file=response_file
        )

        result = process.get_process(CLUSTER, TENANT, process_id)
        expected_result = testtools.expected_payload(response_file).get('entities')[0]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

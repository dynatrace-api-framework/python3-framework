"""Test suite for Topology Processes"""

import unittest
from user_variables import FULL_SET
from tests import tooling_for_test as testtools
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology import process

cluster = FULL_SET.get('mock_cluster')
tenant = 'mock_tenant'
url = f"{TenantAPIs.V1_TOPOLOGY}/infrastructure/processes"
request_dir = "tests/mockserver_payloads/requests/processes"
response_dir = "tests/mockserver_payloads/responses/processes"


class TestGetProcesses(unittest.TestCase):
    """Test cases for fetching topology processes."""

    def test_get_all_processes(self):
        """Test getting all processes tenantwide."""
        response_file = f"{response_dir}/get_all_pgis.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = process.get_processes_tenantwide(cluster, tenant)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_single_process(self):
        """Tests getting one specific process."""
        response_file = f"{response_dir}/get_one_pgi.json"
        process_id = "PROCESS_GROUP_INSTANCE-718687D9E9D0D7CE"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = process.get_process(cluster, tenant, process_id)
        self.assertEqual(result, testtools.expected_payload(response_file))


if __name__ == '__main__':
    unittest.main()

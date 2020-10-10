"""
Test Suite for OneAgents API/Operations
"""
import unittest

from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.framework.request_handler import TenantAPIs
from dynatrace.tenant import oneagents

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
V1HOST_URL = f'{TenantAPIs.V1_TOPOLOGY}/infrastructure/hosts'
ONEAGENTS_URL = f'{TenantAPIs.ONEAGENTS}'
RESPONSE_DIR = "tests/mockserver_payloads/responses/oneagents"


class TestHostUnits(unittest.TestCase):
    """Test cases for retrieving host units"""

    def test_get_host_units_tenantwide(self):
        """Test getting host units tenant-wide"""

        response_file = f'{RESPONSE_DIR}/v1_get_all_hosts.json'

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=V1HOST_URL,
            request_type="GET",
            response_file=response_file
        )

        result = oneagents.get_host_units_tenantwide(CLUSTER, TENANT)
        self.assertEqual(result, 4)

    def test_get_host_units_clusterwide(self):
        """Test getting host units cluster-wide"""

        response_file = f'{RESPONSE_DIR}/v1_get_all_hosts.json'

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=V1HOST_URL,
            request_type="GET",
            response_file=response_file
        )

        result = oneagents.get_host_units_clusterwide(CLUSTER)
        self.assertEqual(result, 4)

    def test_get_host_units_setwide(self):
        """Test getting host units set-wide"""

        response_file = f'{RESPONSE_DIR}/v1_get_all_hosts.json'

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=V1HOST_URL,
            request_type="GET",
            response_file=response_file
        )

        result = oneagents.get_host_units_setwide(FULL_SET)
        self.assertEqual(result, 4)


class TestOneAgents(unittest.TestCase):
    """Test cases for OneAgent operations"""

    def test_get_oneagents_tenantwide(self):
        """Test getting OneAgents tenant-wide"""

        response_file = f'{RESPONSE_DIR}/get_oneagents.json'

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=ONEAGENTS_URL,
            request_type="GET",
            response_file=response_file
        )

        result = oneagents.get_oneagents_tenantwide(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('hosts')

        self.assertEqual(result, expected_result)

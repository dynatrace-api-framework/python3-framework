"""
Test Suite for Topology Hosts
"""
import unittest
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology import hosts

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.ENTITIES)
V1_URL_PATH = f'{TenantAPIs.V1_TOPOLOGY}/infrastructure/hosts'
TAG_URL_PATH = str(TenantAPIs.TAGS)
REQUEST_DIR = "tests/mockserver_payloads/requests/hosts"
RESPONSE_DIR = "tests/mockserver_payloads/responses/hosts"


class TestGetHosts(unittest.TestCase):
    """Tests cases for fetching topology hosts."""

    def test_get_all_hosts(self):
        """Test fetching all hosts"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'type("HOST")'
            },
            response_file=response_file
        )

        result = hosts.get_hosts_tenantwide(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_single_host(self):
        """Test fetching a specific host"""

        host_id = "HOST-ABC123DEF456GHIJ"
        response_file = f"{RESPONSE_DIR}/get_single.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'entityId({host_id})'
            },
            response_file=response_file
        )

        result = hosts.get_host(CLUSTER, TENANT, host_id)
        expected_result = testtools.expected_payload(response_file).get('entities')[0]
        self.assertEqual(result, expected_result)

    def test_get_host_count(self):
        """Test getting the count of hosts in a tenant."""

        response_file = f"{RESPONSE_DIR}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            response_file=response_file,
            parameters={
                'from': 'now-24h',
                'entitySelector': 'type("HOST")'
            }
        )

        result = hosts.get_host_count_tenantwide(CLUSTER, TENANT)
        self.assertEqual(result, 3)

    def test_get_host_units(self):
        """Tests getting the consumed host units in a tenant."""

        response_file = f"{RESPONSE_DIR}/v1_get_all.json"
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=V1_URL_PATH,
            request_type="GET",
            response_file=response_file
        )

        result = hosts.get_host_units_tenantwide(CLUSTER, TENANT)
        self.assertEqual(result, 4)


class TestHostTagging(unittest.TestCase):
    """Test cases for testing host-level tagging."""

    def test_add_tags(self):
        """Test adding two tags to a specific host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        request_file = f"{REQUEST_DIR}/tags.json"
        tags = ["demo", "example"]

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            request_type="POST",
            url_path=TAG_URL_PATH,
            request_file=request_file,
            parameters={
                'entitySelector': f'entityId({host_id})'
            },
            response_code=201
        )

        result = hosts.add_host_tags(CLUSTER, TENANT, host_id, tags)
        self.assertEqual(result.status_code, 201)

    def test_delete_tags(self):
        """Test deleting a tag from a specific host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        tag = "demo"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=TAG_URL_PATH,
            request_type="DELETE",
            response_code=204
        )

        result = hosts.delete_host_tag(CLUSTER, TENANT, host_id, tag)
        self.assertEqual(204, result.status_code)


if __name__ == '__main__':
    unittest.main()

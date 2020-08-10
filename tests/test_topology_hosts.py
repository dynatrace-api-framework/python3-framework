"""
Test Suite for Topology Hosts
"""
import unittest
from user_variables import FULL_SET
from tests import tooling_for_test as testtools
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology import hosts

cluster = FULL_SET.get('mock_cluster')
tenant = 'mock_tenant'
url = f"{TenantAPIs.V1_TOPOLOGY}/infrastructure/hosts"
request_dir = "tests/mockserver_payloads/requests/hosts"
response_dir = "tests/mockserver_payloads/responses/hosts"


class TestGetHosts(unittest.TestCase):
    """Tests cases for fetching topology hosts."""

    def test_get_all_hosts(self):
        """Test fetching all hosts"""

        response_file = f"{response_dir}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = hosts.get_hosts_tenantwide(cluster, tenant)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_single_host(self):
        """Test fetching a specific host"""

        host_id = "HOST-9F74450267BAAE20"
        response_file = f"{response_dir}/get_single.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=f"{url}/{host_id}",
            request_type="GET",
            response_file=response_file
        )

        result = hosts.get_host(cluster, tenant, host_id)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_host_count(self):
        """Test getting the count of hosts in a tenant."""

        response_file = f"{response_dir}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file,
            parameters=dict(relativeTime=['day'],
                            includeDetails=['False'])
        )

        result = hosts.get_host_count_tenantwide(cluster, tenant)
        self.assertEqual(result, 3)

    def test_get_host_units(self):
        """Tests getting the consumed host units in a tenant."""

        response_file = f"{response_dir}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = hosts.get_host_units_tenantwide(cluster, tenant)
        self.assertEqual(result, 4)

        hosts.set_host_properties


class TestHostTagging(unittest.TestCase):
    """Test cases for testing host-level tagging."""

    def test_add_tags(self):
        """Test adding two tags to a specific host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        request_file = f"{request_dir}/tags.json"
        tags = ["demo", "example"]

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            request_type="POST",
            url_path=f"{url}/{host_id}",
            request_file=request_file,
            response_code=201
        )

        result = hosts.add_host_tags(cluster, tenant, host_id, tags)
        self.assertEqual(result, 201)

    def test_delete_tags(self):
        """Test deleting a tag from a specific host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        tag = "demo"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=f"{url}/{host_id}/tags/{tag}",
            request_type="DELETE",
            response_code=204
        )

        result = hosts.delete_host_tag(cluster, tenant, host_id, tag)
        self.assertEqual(204, result.status_code)


if __name__ == '__main__':
    unittest.main()

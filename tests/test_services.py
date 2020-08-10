"""Test Suite for Topology Services"""

import unittest
from user_variables import FULL_SET
from tests import tooling_for_test as testtools
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology import services

cluster = FULL_SET.get('mockserver1')
tenant = 'tenant1'
url = f"{TenantAPIs.V1_TOPOLOGY}/infrastructure/services"
request_dir = "tests/mockserver_payloads/requests/services"
response_dir = "tests/mockserver_payloads/responses/services"


class TestGetServices(unittest.TestCase):
    """Test cases for fetching topology services."""

    def test_get_all_svc(self):
        """Test fetching all services"""
        response_file = f"{response_dir}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = services.get_services_tenantwide(cluster, tenant)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_single_svc(self):
        """Test fetching single service"""
        response_file = f"{response_dir}/get_one.json"
        svc_id = "SERVICE-ABC123DEF456GHI7"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=f"{url}/{svc_id}",
            request_type="GET",
            response_file=response_file
        )

        result = services.get_service(cluster, tenant, svc_id)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_svc_count(self):
        """Test getting the service count tenantwide."""
        response_file = f"{response_dir}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = services.get_service_count_tenantwide(cluster, tenant)
        self.assertEqual(result, 3)


class TestServiceTags(unittest.TestCase):
    """Test cases for service tags"""

    def test_add_svc_tags(self):
        """Test adding two tags to the service."""
        svc_id = "SERVICE-ABC123DEF456GHI7"
        request_file = f"{request_dir}/tags.json"
        tags = ["demo", "example"]

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            request_type="POST",
            url_path=f"{url}/{svc_id}",
            request_file=request_file,
            response_code=201
        )

        result = services.add_service_tags(cluster, tenant, svc_id, tags)
        self.assertEqual(result, 201)


if __name__ == '__main__':
    unittest.main()

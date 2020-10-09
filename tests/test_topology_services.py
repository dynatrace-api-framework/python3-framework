"""Test Suite for Topology Services"""

import unittest
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.tenant.topology.shared import EntityTypes
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology import services

CLUSTER = FULL_SET.get('mockserver1')
TENANT = 'tenant1'
URL_PATH = f"{TenantAPIs.ENTITIES}"
TAG_URL_PATH = f"{TenantAPIs.TAGS}"
TYPE = f"{EntityTypes.SERVICE}"
REQUEST_DIR = "tests/mockserver_payloads/requests/services"
RESPONSE_DIR = "tests/mockserver_payloads/responses/services"


class TestGetServices(unittest.TestCase):
    """Test cases for fetching topology services."""

    def test_get_all_svc(self):
        """Test fetching all services"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

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

        result = services.get_services_tenantwide(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_single_svc(self):
        """Test fetching single service"""
        response_file = f"{RESPONSE_DIR}/get_one.json"
        svc_id = "SERVICE-ABC123DEF456GHI7"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'entityId({svc_id})'
            },
            response_file=response_file
        )

        result = services.get_service(CLUSTER, TENANT, svc_id)
        expected_result = testtools.expected_payload(response_file).get('entities')[0]
        self.assertEqual(result, expected_result)

    def test_get_svc_count(self):
        """Test getting the service count tenantwide."""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'from': 'now-24h',
                'entitySelector': f'type("{TYPE}")'
            },
            response_file=response_file
        )

        result = services.get_service_count_tenantwide(CLUSTER, TENANT)
        self.assertEqual(result, 3)


class TestServiceTags(unittest.TestCase):
    """Test cases for service tags"""

    def test_add_svc_tags(self):
        """Test adding two tags to the service."""
        svc_id = "SERVICE-ABC123DEF456GHI7"
        request_file = f"{REQUEST_DIR}/tags.json"
        tags = ["demo", "example"]

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            request_type="POST",
            url_path=TAG_URL_PATH,
            request_file=request_file,
            parameters={
                'entitySelector': f'entityId({svc_id})'
            },
            response_code=201
        )

        result = services.add_service_tags(CLUSTER, TENANT, svc_id, tags)
        self.assertEqual(result.status_code, 201)


if __name__ == '__main__':
    unittest.main()

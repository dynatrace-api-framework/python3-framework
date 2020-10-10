"""Test Suite for Topology Process Groups"""

import unittest
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.tenant.shared import EntityTypes
from dynatrace.framework.request_handler import TenantAPIs
from dynatrace.tenant import process_groups

CLUSTER = FULL_SET.get('mockserver1')
TENANT = 'tenant1'
URL_PATH = f"{TenantAPIs.ENTITIES}"
TAG_URL_PATH = f"{TenantAPIs.TAGS}"
ENTITY = f"{EntityTypes.PROCESS_GROUP}"
REQUEST_DIR = "tests/mockserver_payloads/requests/processes"
RESPONSE_DIR = "tests/mockserver_payloads/responses/processes"


class TestGetPGs(unittest.TestCase):
    """Test cases for fetching topology process groups."""

    def test_get_all_pgs(self):
        """Test fetching all PGs"""
        response_file = f"{RESPONSE_DIR}/get_all_pgs.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'type("{ENTITY}")'
            },
            response_file=response_file
        )

        result = process_groups.get_process_groups_tenantwide(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_single_pg(self):
        """Test fetching single PG"""
        response_file = f"{RESPONSE_DIR}/get_one_pg.json"
        pg_id = "PROCESS_GROUP-ABC123DEF456GHI7"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'entityId({pg_id})'
            },
            response_file=response_file
        )

        result = process_groups.get_process_group(CLUSTER, TENANT, pg_id)
        expected_result = testtools.expected_payload(response_file).get('entities')[0]
        self.assertEqual(result, expected_result)

    def test_get_pg_count(self):
        """Test getting the PG count tenantwide."""
        response_file = f"{RESPONSE_DIR}/get_all_pgs.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'type("{ENTITY}")'
            },
            response_file=response_file
        )

        result = process_groups.get_process_group_count_tenantwide(CLUSTER, TENANT)
        self.assertEqual(result, 3)


class TestPGTags(unittest.TestCase):
    """Test cases for PG tags"""

    def test_add_pg_tags(self):
        """Test adding two tags to the PG."""
        pg_id = "PROCESS_GROUP-859E1549052CD876"
        request_file = f"{REQUEST_DIR}/tags.json"
        tags = ["demo", "example"]

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            request_type="POST",
            url_path=TAG_URL_PATH,
            request_file=request_file,
            parameters={
                'entitySelector': f'entityId({pg_id})'
            },
            response_code=201
        )

        result = process_groups.add_process_group_tags(CLUSTER, TENANT,
                                                       pg_id, tags)
        self.assertEqual(result.status_code, 201)


if __name__ == '__main__':
    unittest.main()

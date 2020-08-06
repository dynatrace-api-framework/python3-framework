"""Test Suite for Topology Process Groups"""

import unittest
from user_variables import FULL_SET
from tests import tooling_for_test as testtools
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.tenant.topology import process_groups

cluster = FULL_SET.get('mockserver1')
tenant = 'tenant1'
url = f"{TenantAPIs.V1_TOPOLOGY}/infrastructure/process-groups"
request_dir = "tests/mockserver_payloads/requests/processes"
response_dir = "tests/mockserver_payloads/responses/processes"


class TestGetPGs(unittest.TestCase):
    """Test cases for fetching topology process groups."""

    def test_get_all_pgs(self):
        """Test fetching all PGs"""
        response_file = f"{response_dir}/get_all_pgs.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = process_groups.get_process_groups_tenantwide(cluster, tenant)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_single_pg(self):
        """Test fetching single PG"""
        response_file = f"{response_dir}/get_one_pg.json"
        pg_id = "PROCESS_GROUP-859E1549052CD876"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=f"{url}/{pg_id}",
            request_type="GET",
            response_file=response_file
        )

        result = process_groups.get_process_group(cluster, tenant, pg_id)
        self.assertEqual(result, testtools.expected_payload(response_file))

    def test_get_pg_count(self):
        """Test getting the PG count tenantwide."""
        response_file = f"{response_dir}/get_all_pgs.json"

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            url_path=url,
            request_type="GET",
            response_file=response_file
        )

        result = process_groups.get_process_group_count_tenantwide(cluster,
                                                                   tenant)
        self.assertEqual(result, 4)


class TestPGTags(unittest.TestCase):
    """Test cases for PG tags"""

    def test_add_pg_tags(self):
        """Test adding two tags to the PG."""
        pg_id = "PROCESS_GROUP-859E1549052CD876"
        request_file = f"{request_dir}/tags.json"
        tags = ["demo", "example"]

        testtools.create_mockserver_expectation(
            cluster=cluster,
            tenant=tenant,
            request_type="POST",
            url_path=f"{url}/{pg_id}",
            request_file=request_file,
            response_code=201
        )

        result = process_groups.add_process_group_tags(cluster, tenant,
                                                       pg_id, tags)
        self.assertEqual(result, 201)


if __name__ == '__main__':
    unittest.main()

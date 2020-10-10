"""
Test Suite for Entities API
"""
import unittest
from dynatrace.tenant.entities import EntityTypes
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.framework.request_handler import TenantAPIs
from dynatrace.tenant import entities

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.ENTITIES)
TAG_URL_PATH = str(TenantAPIs.TAGS)
REQUEST_DIR = "tests/mockserver_payloads/requests/entities"
RESPONSE_DIR = "tests/mockserver_payloads/responses/entities"


class TestGetEntities(unittest.TestCase):
    """Tests cases for fetching entities."""

    def test_get_entities(self):
        """Test fetching all entities of given type tenant-wide"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'type(HOST)'
            },
            response_file=response_file
        )

        result = entities.get_entities_tenantwide(CLUSTER, TENANT, EntityTypes.HOST)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_entities_clusterwide(self):
        """Test fetching all entities of given type cluster-wide"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'type(HOST)'
            },
            response_file=response_file
        )

        result = entities.get_entities_clusterwide(CLUSTER, EntityTypes.HOST)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_entities_setwide(self):
        """Test fetching all entities of given type set-wide"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'type(HOST)'
            },
            response_file=response_file
        )

        result = entities.get_entities_setwide(FULL_SET, EntityTypes.HOST)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(result, expected_result)

    def test_get_entity(self):
        """Test fetching a single entity."""

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

        result = entities.get_entity(CLUSTER, TENANT, host_id)
        expected_result = testtools.expected_payload(response_file).get('entities')[0]
        self.assertEqual(result, expected_result)

    def test_get_entities_by_page(self):
        """Test fetching tenantwide entities by page"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'type(HOST)'
            },
            response_file=response_file
        )

        result = entities.get_entities_by_page(CLUSTER, TENANT, EntityTypes.HOST)
        expected_result = testtools.expected_payload(response_file).get('entities')
        self.assertEqual(next(result), expected_result)

    def test_get_entity_count_tenantwide(self):
        """Test getting the count of entities within a tenant."""

        response_file = f"{RESPONSE_DIR}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            response_file=response_file,
            parameters={
                'from': 'now-24h',
                'pageSize': '1',
                'entitySelector': 'type(HOST)'
            }
        )

        result = entities.get_entity_count_tenantwide(CLUSTER, TENANT, EntityTypes.HOST)
        self.assertEqual(result, 3)

    def test_get_entity_count_clusterwide(self):
        """Test getting the count of entities within a cluster."""

        response_file = f"{RESPONSE_DIR}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            response_file=response_file,
            parameters={
                'from': 'now-24h',
                'pageSize': '1',
                'entitySelector': 'type(HOST)'
            }
        )

        result = entities.get_entity_count_clusterwide(CLUSTER, EntityTypes.HOST)
        self.assertEqual(result, 3)

    def test_get_entity_count_setwide(self):
        """Test getting the count of entities within a full set."""

        response_file = f"{RESPONSE_DIR}/get_all.json"
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            response_file=response_file,
            parameters={
                'from': 'now-24h',
                'pageSize': '1',
                'entitySelector': 'type(HOST)'
            }
        )

        result = entities.get_entity_count_setwide(FULL_SET, EntityTypes.HOST)
        self.assertEqual(result, 3)


class TestHostTagging(unittest.TestCase):
    """Test cases for testing entity tagging."""

    def test_add_tags(self):
        """Test adding two tags to a specific entity."""

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

        result = entities.add_tags(
            cluster=CLUSTER,
            tenant=TENANT,
            tag_list=tags,
            entitySelector=f'entityId({host_id})'
        )
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

        result = entities.delete_tag(
            cluster=CLUSTER,
            tenant=TENANT,
            tag_key=tag,
            entitySelector=f'entityId({host_id})'
        )
        self.assertEqual(204, result.status_code)


if __name__ == '__main__':
    unittest.main()

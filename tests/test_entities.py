"""
Test Suite for Entities API
"""
import unittest
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.tenant.entities import EntityTypes
from dynatrace.framework.request_handler import TenantAPIs
from dynatrace.tenant import entities

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.ENTITIES)
TAG_URL_PATH = str(TenantAPIs.TAGS)
REQUEST_DIR = "tests/mockserver_payloads/requests/entities"
RESPONSE_DIR = "tests/mockserver_payloads/responses/entities"


class TestFramework(unittest.TestCase):
    """Tests for framework functions related to entities."""

    def test_enum_repr(self):
        result = EntityTypes.HOST.__repr__()
        expected_result = EntityTypes.HOST.name

        self.assertEqual(result, expected_result)


class TestGetEntities(unittest.TestCase):
    """Tests cases for fetching entities."""

    def test_get_entities_with_selector(self):
        """Tests fetching all entities matching a selector"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'tag("test"),type(HOST)'
            },
            response_file=response_file
        )

        result = entities.get_entities_tenantwide(
            CLUSTER, TENANT, EntityTypes.HOST, **{'entitySelector': 'tag("test")'}
        )
        expected_result = testtools.expected_payload(response_file).get('entities')

        self.assertEqual(result, expected_result)

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

    def test_get_entities_by_id(self):
        """Test fetching multiple entities by IDs"""
        entity_ids = "HOST-ABC123DEF456GHIJ,HOST-5B9CE4E4E14185FA,HOST-421D60DB4A2EA929"
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': f'entityId({entity_ids})'
            },
            response_file=response_file
        )

        result = entities.get_entity(CLUSTER, TENANT, entity_ids)
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

    def test_get_entities_by_page_with_selector(self):
        """Test fetching tenantwide entities by page using entity selector"""

        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                'entitySelector': 'tag("test"),type(HOST)'
            },
            response_file=response_file
        )

        result = entities.get_entities_by_page(
            CLUSTER, TENANT, EntityTypes.HOST, **{'entitySelector': 'tag("test")'}
        )
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

    def test_get_entity_count_tenantwide_with_selector(self):
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
                'entitySelector': 'tag("test"),type(HOST)'
            }
        )

        result = entities.get_entity_count_tenantwide(
            CLUSTER, TENANT, EntityTypes.HOST, **{'entitySelector': 'tag("test")'}
        )
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

    def test_delete_tag(self):
        """Test deleting a tag from a specific host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        tag = "demo"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=TAG_URL_PATH,
            request_type="DELETE",
            parameters={
                'key': tag,
                'entitySelector': f'entityId({host_id})'
            },
            response_code=204
        )

        result = entities.delete_tag(
            cluster=CLUSTER,
            tenant=TENANT,
            tag_key=tag,
            entitySelector=f'entityId({host_id})'
        )
        self.assertEqual(204, result.status_code)

    def test_delete_tag_with_value(self):
        """Test deleting a tag with specific value from a host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        tag = "demo_key"
        tag_val = "demo_value"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=TAG_URL_PATH,
            request_type="DELETE",
            parameters={
                'key': tag,
                'value': tag_val,
                'entitySelector': f'entityId({host_id})'
            },
            response_code=204
        )

        result = entities.delete_tag(
            cluster=CLUSTER,
            tenant=TENANT,
            tag_key=tag,
            tag_value=tag_val,
            entitySelector=f'entityId({host_id})'
        )
        self.assertEqual(204, result.status_code)

    def test_delete_tag_all(self):
        """Test deleting a tag by key from a specific host."""

        host_id = "HOST-ABC123DEF456GHIJ"
        tag = "demo"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=TAG_URL_PATH,
            request_type="DELETE",
            parameters={
                "key": tag,
                "deleteAllWithKey": "True",
                "entitySelector": f"entityId({host_id})"
            },
            response_code=204
        )

        result = entities.delete_tag(
            cluster=CLUSTER,
            tenant=TENANT,
            tag_key=tag,
            tag_value="all",
            entitySelector=f'entityId({host_id})'
        )
        self.assertEqual(204, result.status_code)


class TestCustomDevices(unittest.TestCase):
    """Test cases for custom devices."""

    def test_create_device(self):
        """Test creating a new custom device"""
        request_file = f"{REQUEST_DIR}/device.json"
        json_data = testtools.expected_payload(request_file)
        device_id = json_data.get("customDeviceId")

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                "entitySelector": f"entityId({device_id})"
            },
            response_data={},
            mock_id="req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/custom",
            request_type="POST",
            request_file=request_file,
            response_code=201,
            mock_id="req2"
        )

        result = entities.custom_device(CLUSTER, TENANT, json_data)

        self.assertEqual(result.status_code, 201)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling in the entities module."""

    def test_add_tags_err_no_tag(self):
        """Tests error handling when adding tags to entities.
        Tags cannot be empty.
        """
        with self.assertRaises(TypeError):
            entities.add_tags(CLUSTER, TENANT, "")

    def test_add_tags_err_no_list(self):
        """Tests error handling when adding tags to entities.
        Tags list must be a list.
        """
        with self.assertRaises(TypeError):
            entities.add_tags(CLUSTER, TENANT, "tag")

    def test_add_tags_err_no_selector(self):
        """Tests error handling when adding tags to entities.
        Must provide an entity selector.
        """
        with self.assertRaises(ValueError):
            entities.add_tags(CLUSTER, TENANT, ["test"])

    def test_add_tags_err_no_type(self):
        """Tests error handling when adding tags to entities.
        Must provide either entity type or ID in entity selector.
        """
        with self.assertRaises(ValueError):
            entities.add_tags(
                CLUSTER, TENANT, ["test"], **{'entitySelector': 'tag("test")'}
            )

    def test_delete_tag_err_no_tag(self):
        """Tests error handling when deleting tags from entities.
        Tag key must not be empty.
        """
        with self.assertRaises(TypeError):
            entities.delete_tag(CLUSTER, TENANT, "")

    def test_delete_tag_err_no_selector(self):
        """Tests error handling when deleting tags from entities.
        Must provide entity selector.
        """
        with self.assertRaises(ValueError):
            entities.delete_tag(CLUSTER, TENANT, "test")

    def test_delete_tag_err_no_type(self):
        """Tests error handling when deleting tags from entities.
        Must provide either entity ID or type in entity selector.
        """
        with self.assertRaises(ValueError):
            entities.delete_tag(
                CLUSTER, TENANT, "test", **{'entitySelector': 'tag("test")'}
            )

    def test_create_device_err_missing(self):
        """Tests error handling when creating custom devices.
        Device ID or name must be present in payload.
        """
        request_file = f"{REQUEST_DIR}/device.json"
        json_data = testtools.expected_payload(request_file)
        json_data.pop("customDeviceId")

        with self.assertRaises(ValueError):
            entities.custom_device(CLUSTER, TENANT, json_data)

    def test_create_device_err_no_type(self):
        """Tests error handling when creating a custom device.
        Type must be present in the payload.
        """
        request_file = f"{REQUEST_DIR}/device.json"
        json_data = testtools.expected_payload(request_file)
        device_id = json_data.get("customDeviceId")
        json_data.pop("type")

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                "entitySelector": f"entityId({device_id})"
            },
            response_data={}
        )

        with self.assertRaises(ValueError):
            entities.custom_device(CLUSTER, TENANT, json_data)


if __name__ == '__main__':
    unittest.main()

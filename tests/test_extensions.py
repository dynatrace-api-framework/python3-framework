"""Test Suite for the Extensions API"""
import unittest
import json
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testtools
from dynatrace.framework.request_handler import TenantAPIs, HTTP
from dynatrace.tenant import extensions

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.EXTENSIONS)
EXTENSION_ID = "custom.jmx.radujmx123456789"
INSTANCE_ID = "HOST-ABC123DEF456GHI7"
REQUEST_DIR = "tests/mockserver_payloads/requests/extensions"
RESPONSE_DIR = "tests/mockserver_payloads/responses/extensions"


class TestGetExtensions(unittest.TestCase):
    """Test cases for fetching extensions and their details"""

    def test_get_all_extensions(self):
        """Test fetching a list of extensions from a tenant"""
        response_file = f"{RESPONSE_DIR}/get_all.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_all_extensions(CLUSTER, TENANT)
        expected_result = testtools.expected_payload(response_file).get('extensions')

        self.assertEqual(result, expected_result)

    def test_get_extension_details(self):
        """Test fetching the details of an extension"""
        response_file = f"{RESPONSE_DIR}/details.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_extension_details(CLUSTER, TENANT, EXTENSION_ID)
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)

    def test_get_extension_instances(self):
        """Test fetching the list of instances for an extension"""
        response_file = f"{RESPONSE_DIR}/instances.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}/instances",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_extension_instances(CLUSTER, TENANT, EXTENSION_ID)
        expected_result = testtools.expected_payload(
            response_file
        ).get('configurationsList')

        self.assertEqual(result, expected_result)

    def test_get_extension_states(self):
        """Test fetching the list of states for an extension"""
        response_file = f"{RESPONSE_DIR}/states.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}/states",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_extension_states(CLUSTER, TENANT, EXTENSION_ID)
        expected_result = testtools.expected_payload(response_file).get('states')

        self.assertEqual(result, expected_result)

    def test_get_extension_global_config(self):
        """Test fetching the global configuration of an extension"""
        response_file = f"{RESPONSE_DIR}/config.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}/global",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_extension_global_config(CLUSTER, TENANT, EXTENSION_ID)
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)

    def test_get_extension_instance_config(self):
        """Test fetching a configuration instance for an extension"""
        response_file = f"{RESPONSE_DIR}/config.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}/instances/{INSTANCE_ID}",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_extension_instance_config(
            CLUSTER, TENANT, EXTENSION_ID, INSTANCE_ID
        )
        expected_result = testtools.expected_payload(response_file)

        self.assertEqual(result, expected_result)

    def test_get_extension_metrics(self):
        """Tests fetching the metrics collected by an extension"""
        details_file = f"{RESPONSE_DIR}/details.json"
        response_file = f"{RESPONSE_DIR}/metrics.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}",
            request_type=str(HTTP.GET),
            response_file=details_file,
            mock_id="first"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=str(TenantAPIs.METRICS),
            parameters={
                "metricSelector": "ext:custom.jmx.radujmx.*"
            },
            mock_id="second",
            request_type=str(HTTP.GET),
            response_file=response_file
        )

        result = extensions.get_extension_metrics(CLUSTER, TENANT, EXTENSION_ID)
        expected_result = list(
            m.get('metricId')
            for m in testtools.expected_payload(response_file).get('metrics')
        )

        self.assertEqual(result, expected_result)


class TestModifyExtensions(unittest.TestCase):
    """Test cases for modifying extension states and details"""

    def test_update_global_config(self):
        """Test updating the global config for an extension"""
        request_file = f"{REQUEST_DIR}/config.json"
        with open(request_file, "r") as config_file:
            config = json.loads(config_file.read())

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}/global",
            request_type=str(HTTP.PUT),
            request_file=request_file,
            response_code=202
        )

        result = extensions.update_global_config(
            CLUSTER, TENANT, EXTENSION_ID, config
        ).status_code
        expected_result = 202

        self.assertEqual(result, expected_result)

    def test_update_instance_config(self):
        """Test updating an instance of configuration for an extension"""
        request_file = f"{REQUEST_DIR}/config.json"
        with open(request_file, "r") as config_file:
            config = json.loads(config_file.read())

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/{EXTENSION_ID}/instances/{INSTANCE_ID}",
            request_type=str(HTTP.PUT),
            request_file=request_file,
            response_code=202
        )

        result = extensions.update_instance_config(
            CLUSTER, TENANT, EXTENSION_ID, INSTANCE_ID, config
        ).status_code
        expected_result = 202

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()

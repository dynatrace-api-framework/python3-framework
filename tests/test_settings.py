"""Test Cases for dynatrace.settings"""
import unittest
import yaml
from dynatrace.framework import settings

SETTINGS_JSON = "user_variables.json"
SETTINGS_YAML = "user_variables.yaml"
with open(SETTINGS_YAML) as file:
    IMPORTED_SETTINGS = yaml.load(file, Loader=yaml.FullLoader)

URL = "test.site"
TENANT_TOKEN = "new_tenant_token"

class TestSettings(unittest.TestCase):
    """Standard Testing Class"""
    def test_get_setting_from_user_variable(self):
        """Will pull from user_variables when available"""
        timezone = settings.get_setting("DEFAULT_TIMEZONE")
        self.assertEqual(timezone, "America/Chicago")

    def test_get_setting_from_default(self):
        """When not in user_variables, info should be pulled from default values"""
        log_dir = settings.get_setting("LOG_DIR")
        self.assertEqual(log_dir, "logs/")

    def test_get_invalid_setting(self):
        """"When not a valid setting, an error should be thrown"""
        with self.assertRaises(AttributeError) as context:
            settings.get_setting("INVALID_SETTING")

        self.assertIn("not a valid user variable attribute",
                      str(context.exception))

class TestSettingsFile(unittest.TestCase):
    """Test settings file is being used when provided"""
    def test_import_yaml(self):
        """Testing YAML Import"""
        settings.load_settings_from_file(SETTINGS_YAML)
        self.assertEqual(settings.get_setting("LOG_LEVEL"), "DEBUG")
    def test_import_json(self):
        """Testing JSON Import"""
        settings.load_settings_from_file(SETTINGS_JSON)
        self.assertEqual(settings.get_setting("LOG_LEVEL"), "WARNING")
    def test_import_multi(self):
        """Ensure Latest user_variables file takes precedent"""
        settings.load_settings_from_file(SETTINGS_YAML)
        settings.load_settings_from_file(SETTINGS_JSON)
        self.assertEqual(settings.get_setting("LOG_LEVEL"), "WARNING")
        self.assertEqual(settings.get_setting("DEFAULT_TIMEZONE"),"America/Chicago")

class TestClusterSettings(unittest.TestCase):
    """Test Cluster Settings"""
    def test_get_cluster_dict_with_dict(self):
        """Test retreiving cluster dictionary by passing in a dict"""

        request_cluster = IMPORTED_SETTINGS['FULL_SET']['mockserver1']
        response_cluster = settings.get_cluster_dict(request_cluster)
        self.assertEqual(request_cluster, response_cluster)
    def test_get_cluster_dict_with_str(self):
        """Test retreiving cluster dictionary by passing in a dict"""
        response_cluster = settings.get_cluster_dict("mockserver1")
        self.assertEqual(IMPORTED_SETTINGS['FULL_SET']['mockserver1'], response_cluster)
    def test_cluster_creation_minimal(self):
        """Test cluster creation programatically"""
        new_cluster = settings.create_cluster("cluster", URL)
        expected_cluster = {
            "url": URL,
            'tenant': {},
            'api_token': {},
            'verify_ssl': True,
            'is_managed': True,
        }
        self.assertEqual(new_cluster, expected_cluster)
    def test_cluster_creation_complete(self):
        """Test cluster creation programatically"""
        new_cluster = settings.create_cluster(
                "cluster",
                URL,
                tenant_ids={"tenant1":"tenant1-id"},
                tenant_tokens={"tenant1":"tenant1-token"},
                cluster_token="cluster_api_token"
        )
        expected_cluster = {
                "url": URL,
                "tenant": {
                        "tenant1": "tenant1-id"
                },
                "api_token": {
                        "tenant1": "tenant1-token"
                },
                "verify_ssl": True,
                "is_managed": True,
                "cluster_token": "cluster_api_token"
        }
        self.assertEqual(new_cluster, expected_cluster)
    def test_add_tenant_to_cluster(self):
        """Test adding tenant to cluster programatically"""
        settings.create_cluster(
                "cluster",
                URL
        )
        new_cluster = settings.add_tenant_to_cluster(
                "cluster",
                "new-id-here",
                TENANT_TOKEN,
                "tenant2"
        )
        expected_cluster = {
                "url": URL,
                "tenant": {
                        "tenant2": "new-id-here"
                },
                "api_token": {
                        "tenant2": TENANT_TOKEN
                },
                "verify_ssl": True,
                "is_managed": True
        }
        self.assertEqual(new_cluster, expected_cluster)

class TestClusterExceptions(unittest.TestCase):
    """Exceptions with Cluster Operations"""
    def test_cluster_creation_improper_tenant(self):
        """Create cluster with an invalid tenant_id combination"""
        with self.assertRaises(ValueError) as context:
            settings.create_cluster(
                    "cluster",
                    URL,
                    tenant_ids={"tenant1":"tenant1-id"},
                    cluster_token="cluster_api_token"
            )
        self.assertTrue("Tenant and tenant token must both be dict" in str(context.exception))
    def test_add_tenant_to_cluster_dict(self):
        """Addiing Tenant to Cluster Dictionary"""
        with self.assertRaises(NotImplementedError) as context:
            new_cluster = settings.create_cluster(
                    "cluster",
                    URL
            )
            new_cluster = settings.add_tenant_to_cluster(
                    new_cluster,
                    "new-id-here",
                    TENANT_TOKEN,
                    "tenant2"
            )
        self.assertTrue(
                "Cluster dicts are not supported yet. Please use str for the cluster's key" \
                        in str(context.exception))
    def test_add_tenant_to_cluster_nonexistant(self):
        """Get Cluster Dict with an invalid/nonexistant key"""
        with self.assertRaises(KeyError) as context:
            settings.create_cluster(
                    "cluster",
                    URL
            )
            settings.add_tenant_to_cluster(
                    "cluster2",
                    "new-id-here",
                    TENANT_TOKEN,
                    "tenant2"
            )
        self.assertTrue("Cluster not found" in str(context.exception))
    def test_get_cluster_dict_nonexistant(self):
        """Get Cluster Dict with an invalid/nonexistant key"""
        with self.assertRaises(ValueError) as context:
            settings.get_cluster_dict("cluster2")
        self.assertTrue("Cluster not found" in str(context.exception))

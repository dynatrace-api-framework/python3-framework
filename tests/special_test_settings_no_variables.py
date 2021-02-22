"""Special Cases for settings which requires user_variables.py to NOT exist"""
import unittest
from os import rename

USER_VARIABLES_CURRENT="user_variables.py"
USER_VARIABLES_MOVED="user_variables.py.tmp"
class TestSettingsWithoutVarFile(unittest.TestCase):
    """Special test cases when user_variables is absent"""
    def test_settings_without_var_file(self):
        """Test should return default value when user_variables missing"""
        rename(USER_VARIABLES_CURRENT, USER_VARIABLES_MOVED)
        from dynatrace.framework import settings  # pylint: disable=import-outside-toplevel
        timezone = settings.get_setting("DEFAULT_TIMEZONE")
        self.assertEqual(timezone, "UTC")
        rename(USER_VARIABLES_MOVED, USER_VARIABLES_CURRENT)
    def test_cluster_creation_from_nothing(self):
        """Create Cluster without a preexisting user_variables"""
        rename(USER_VARIABLES_CURRENT, USER_VARIABLES_MOVED)
        from dynatrace.framework import settings # pylint: disable=import-outside-toplevel
        new_cluster = settings.create_cluster("cluster", "test.site")
        expected_cluster = {
            "url": "test.site",
            'tenant': {},
            'api_token': {},
            'verify_ssl': True,
            'is_managed': True,
        }
        self.assertEqual(new_cluster, expected_cluster)
        rename(USER_VARIABLES_MOVED, USER_VARIABLES_CURRENT)

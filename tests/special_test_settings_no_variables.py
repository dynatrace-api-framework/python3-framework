"""Special Cases for settings which requires user_variables.py to NOT exist"""
import unittest
from os import rename


class TestSettingsWithoutVarFile(unittest.TestCase):
    """Special test cases when user_variables is absent"""
    def test_settings_without_var_file(self):
        """Test should return default value when user_variables missing"""
        rename("user_variables.py", "user_variables.py.tmp")
        from dynatrace import settings  # pylint: disable=import-outside-toplevel
        timezone = settings.get_setting("DEFAULT_TIMEZONE")
        self.assertEqual(timezone, "UTC")
        rename("user_variables.py.tmp", "user_variables.py")

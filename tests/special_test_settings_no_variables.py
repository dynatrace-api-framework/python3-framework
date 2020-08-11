import unittest
from os import rename

class TestSettingsWithoutVarFile(unittest.TestCase):
    def test_settings_without_var_file(self):
        rename("user_variables.py", "user_variables.py.tmp")
        from dynatrace import settings
        tz = settings.get_setting("DEFAULT_TIMEZONE")
        self.assertEqual(tz, "UTC")
        rename("user_variables.py.tmp", "user_variables.py")


"""Test Cases for dynatrace.settings"""
import unittest
from dynatrace import settings


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

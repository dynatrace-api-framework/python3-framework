import unittest
from dynatrace import settings


class TestSettings(unittest.TestCase):
    def test_get_setting_from_user_variable(self):
        tz = settings.get_setting("DEFAULT_TIMEZONE")
        self.assertEqual(tz, "America/Chicago")

    def test_get_setting_from_default(self):
        log_dir = settings.get_setting("LOG_DIR")
        self.assertEqual(log_dir, "logs/")

    def test_get_invalid_setting(self):
        with self.assertRaises(AttributeError) as context:
            settings.get_setting("INVALID_SETTING")

        self.assertIn("not a valid user variable attribute",
                      str(context.exception))

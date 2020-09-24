"""Test Cases For Maintenance Windows."""
import unittest
import user_variables
from tests import tooling_for_test
from dynatrace.tenant import maintenance
from dynatrace.requests.request_handler import TenantAPIs
from dynatrace.exceptions import InvalidDateFormatException

CLUSTER = user_variables.FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.MAINTENANCE_WINDOWS)
TEST_RANGE_START = "2020-01-01 00:00"
TEST_RANGE_END = "2020-01-02 00:00"
TEST_PAYLOAD_TITLE = "Test Payload"
TEST_PAYLOAD_DESC = "Generating Payload for Test"


class TestMaintenanceWindowCreate(unittest.TestCase):
    """Test Cases for Creating a Maintenance Window"""
    REQUEST_DIR = "tests/mockserver_payloads/requests/maintenance/"
    RESPONSE_DIR = "tests/mockserver_payloads/responses/maintenance/"

    def test_create_daily_no_scope(self):
        """
        Testing create daily Maintenance Window with no scope
        """
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"
        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.DAILY,
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END
        )
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_daily_single_tag(self):
        """Testing create daily Maintenance Window with a single tag scope"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_single_tag_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"
        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.DAILY,
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[{'context': "CONTEXTLESS", 'key': "testing"}])
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            scope=maintenance_scope,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_daily_tags_and(self):
        """Testing Payloads with multiple tags in an \"AND\" configuration"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_multi_tags_and_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.DAILY,
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[
                {'context': "CONTEXTLESS", 'key': "testing"},
                {'context': "CONTEXTLESS", 'key': "testing2"}
            ],
            match_any_tag=False
        )
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            scope=maintenance_scope,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_daily_tags_or(self):
        """Testing Payloads with multiple tags in an \"AND\" configuration"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_daily_multi_tags_or_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.DAILY,
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[
                {'context': "CONTEXTLESS", 'key': "testing"},
                {'context': "CONTEXTLESS", 'key': "testing2"}
            ],
            match_any_tag=True
        )
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            scope=maintenance_scope,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_once_no_scope(self):
        """Testing Payloads with ONCE recurrance type"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_once_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.ONCE,
            # TODO Remove need for these variables. ONCE does not use them
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END
        )
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_weekly_no_scope(self):
        """Testing Payloads with WEEKLY recurrance type"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_weekly_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.WEEKLY,
            # TODO Remove need for these variables. ONCE does not use them
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END,
            day=maintenance.DayOfWeek.SUNDAY
        )
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

    def test_create_monthly_no_scope(self):
        """Testing Payloads with MONTHLY recurrance type"""
        mockserver_request_file = f"{self.REQUEST_DIR}mock_create_monthly_1.json"
        mockserver_response_file = f"{self.RESPONSE_DIR}mock_create_1.json"

        tooling_for_test.create_mockserver_expectation(
            CLUSTER,
            TENANT,
            URL_PATH,
            "POST",
            request_file=mockserver_request_file,
            response_file=mockserver_response_file,
        )
        maintenance_schedule = maintenance.generate_schedule(
            maintenance.RecurrenceType.MONTHLY,
            # TODO Remove need for these variables. ONCE does not use them
            "23:00",
            60,
            TEST_RANGE_START,
            TEST_RANGE_END,
            day=1
        )
        maintenance_json = maintenance.generate_window_json(
            TEST_PAYLOAD_TITLE,
            TEST_PAYLOAD_DESC,
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT,
            maintenance_schedule,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))


class TestMaintenanceExceptions(unittest.TestCase):
    """Series of Tests aimed at triggering exception"""
    def test_invalid_recurrence_type(self):
        """Testing exception thrown for invalid recurrence type"""
        with self.assertRaises(ValueError) as context:
            maintenance.generate_schedule(
                "HOURLY",
                "23:00",
                60,
                TEST_RANGE_START,
                TEST_RANGE_END,
            )

        self.assertTrue("Invalid Recurrence Type!" in str(context.exception))

    def test_invalid_day_of_week(self):
        """Testing exception thrown for invalid dayOfWeek"""
        with self.assertRaises(ValueError) as context:
            maintenance.generate_schedule(
                maintenance.RecurrenceType.WEEKLY,
                "23:00",
                60,
                TEST_RANGE_START,
                TEST_RANGE_END,
                day=1
            )
        self.assertTrue("Invalid Weekly Day!" in str(context.exception))

    def test_invalid_day_of_month_value(self):
        """Testing exception thrown for invalid dayOfMonth for incorrect int"""
        with self.assertRaises(ValueError) as context:
            maintenance.generate_schedule(
                maintenance.RecurrenceType.MONTHLY,
                "23:00",
                60,
                TEST_RANGE_START,
                TEST_RANGE_END,
                day=32
            )
        self.assertTrue("Invalid Monthly Day!" in str(context.exception))

    def test_invalid_day_of_month_type(self):
        """Testing exception thrown for invalid dayOfMonth for a non-int"""
        with self.assertRaises(TypeError) as context:
            maintenance.generate_schedule(
                maintenance.RecurrenceType.MONTHLY,
                "23:00",
                60,
                TEST_RANGE_START,
                TEST_RANGE_END,
                day="Eleven"
            )
        self.assertTrue(
            "Invalid type for Day of Month! Int between 1-31 required" in str(context.exception))

    def test_no_day_of_week_supplied(self):
        """Weekly Maintenance Window with no dayOfWeek supplied"""
        with self.assertRaises(Exception) as context:
            maintenance.generate_schedule(
                maintenance.RecurrenceType.WEEKLY,
                "23:00",
                60,
                TEST_RANGE_START,
                TEST_RANGE_END,
            )
        self.assertTrue("Invalid Weekly Day!" in str(context.exception))

    def test_no_day_of_month_supplied(self):
        """Monthly Maintenance Window with no dayOfMonth supplied"""
        with self.assertRaises(Exception) as context:
            maintenance.generate_schedule(
                maintenance.RecurrenceType.MONTHLY,
                "23:00",
                60,
                TEST_RANGE_START,
                TEST_RANGE_END,
            )
        self.assertTrue(
            "Invalid type for Day of Month!" in str(context.exception))

    def test_invalid_datetime_format(self):
        """Test invalid datetime supplied to trigger ValueError"""
        # TODO Fix Exceoption to have a message as first arg
        with self.assertRaises(InvalidDateFormatException) as context:
            maintenance.generate_schedule(
                maintenance.RecurrenceType.DAILY,
                "23:00",
                60,
                TEST_RANGE_START,
                "2020-01-02"
            )
        self.assertTrue(
            "Incorrect Date " in context.exception.message, context.exception.message)

    def test_invalid_filter_type(self):
        """Invalid Filter_Type"""
        with self.assertRaises(ValueError) as context:
            maintenance.generate_scope(
                tags=[{'context': "CONTEXTLESS", 'key': "testing"}],
                filter_type="INVALID_TYPE"
            )
        self.assertTrue("Invalid Filter Type" in (
            msg := str(context.exception)), msg)  # pylint: disable=used-before-assignment


class TestMaintenanceEnumTypes(unittest.TestCase):
    """Test to validate Maintenance Enum Types are correct"""
    def test_suppression_enum_str(self):
        """Suppression enum str should be string"""
        suppression = maintenance.Suppression(
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT)
        self.assertIsInstance(
            maintenance.Suppression.__str__(suppression), str)

    def test_suppression_enum_repr(self):
        """Suppression enum repr should be string"""
        suppression = maintenance.Suppression(
            maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT)
        self.assertIsInstance(
            maintenance.Suppression.__repr__(suppression), str)

    def test_day_of_week_enum_str(self):
        """Day of Week enum str should be string"""
        day_of_week = maintenance.DayOfWeek(maintenance.DayOfWeek.MONDAY)
        self.assertIsInstance(maintenance.DayOfWeek.__str__(day_of_week), str)

    def test_day_of_week_enum_repr(self):
        """Day of Week enum repr should be string"""
        day_of_week = maintenance.DayOfWeek(maintenance.DayOfWeek.MONDAY)
        self.assertIsInstance(maintenance.DayOfWeek.__repr__(day_of_week), str)

    def test_context_enum_str(self):
        """Context enum str should be string"""
        context = maintenance.Context(maintenance.Context.CONTEXTLESS)
        self.assertIsInstance(maintenance.Context.__str__(context), str)

    def test_context_enum_repr(self):
        """Context enum repr should be string"""
        context = maintenance.Context(maintenance.Context.CONTEXTLESS)
        self.assertIsInstance(maintenance.Context.__repr__(context), str)

    def test_recurrence_type_enum_str(self):
        """Recurrence Type enum str should be string"""
        recurrence_type = maintenance.RecurrenceType(
            maintenance.RecurrenceType.DAILY)
        self.assertIsInstance(
            maintenance.RecurrenceType.__str__(recurrence_type), str)

    def test_recurrence_type_enum_repr(self):
        """Recurrence Type enum repr should be string"""
        recurrence_type = maintenance.RecurrenceType(
            maintenance.RecurrenceType.DAILY)
        self.assertIsInstance(
            maintenance.RecurrenceType.__repr__(recurrence_type), str)

    def test_filter_type_enum_str(self):
        """Filter Type enum str should be string"""
        suppression = maintenance.FilterType(
            maintenance.FilterType.APM_SECURITY_GATEWAY)
        self.assertIsInstance(maintenance.FilterType.__str__(suppression), str)

    def test_filter_type_enum_repr(self):
        """Filter Type enum repr should be string"""
        suppression = maintenance.FilterType(
            maintenance.FilterType.APM_SECURITY_GATEWAY)
        self.assertIsInstance(
            maintenance.FilterType.__repr__(suppression), str)


class TestTagParsing(unittest.TestCase):
    """Testing Maintenance Window Tag Handling"""
    def test_tag_variations(self):
        """Testing various ways tags need to be parsed"""
        # Test 1 - Key
        # Test 2 - Key, Value
        # Test 3 - Context, Key and Value
        # Test 4 - Key with Colon, Value
        # Test 5 - Key with Colon, Value Blank
        # Test 6 - Context, Key with Colon and Value
        # Test 7 - Context, Key
        # Test 8 - Context, Key with square brackets
        # Test 9 - Context, Key with colon and squares
        # Test 10 - Empty Context with squares

        test_tag_list = [
            "Key",
            "Key:Value",
            "[Context]Key:Value",
            "Key:withColon:Value",
            "Key:withColon:",
            "[Context]Key:withColon:Value",
            "[Context]Key",
            "[Context][KeywithSquares]",
            "[Context][KeyWithSquares]:AndColons:Value",
            "[][KeywithSquares]",
        ]

        test_tag_expected_results = [
            {'context': 'CONTEXTLESS', 'key': 'Key'},
            {'context': 'CONTEXTLESS', 'key': 'Key:Value'},
            {'context': 'Context', 'key': 'Key:Value'},
            {'context': 'CONTEXTLESS', 'key': 'Key:withColon:Value'},
            {'context': 'CONTEXTLESS', 'key': 'Key:withColon:'},
            {'context': 'Context', 'key': 'Key:withColon:Value'},
            {'context': 'Context', 'key': 'Key'},
            {'context': 'Context', 'key': '[KeywithSquares]'},
            {'context': 'Context',
             'key': '[KeyWithSquares]:AndColons:Value'},
            {'context': 'CONTEXTLESS', 'key': '[][KeywithSquares]'},
        ]

        for i, test_tag_input in enumerate(test_tag_list):
            processed_tag = test_tag_input
            self.assertTrue(
                (result := maintenance.parse_tag(processed_tag)
                 ) == test_tag_expected_results[i],
                f"Test {i}: {result} did not match {test_tag_expected_results[i]}")


if __name__ == '__main__':
    unittest.main()

# CREATE TESTS LEFT:
# Single Entity
# Multi Entity
# Single Tag with Filter Type
# Mutli Tags with Filter Type
# Single Tag with Management Zone
# Multi Tags with Management Zone

# EXCEPTION TEST CASES:
# MANAGEMENT_ZONE WITHOUT TAG
# FILTER_TYPE WITHOUT TAG

# OTHER TEST CASES:
# GET ALL WINDOWS
# GET DETAILS OF WINDOW
# DELETE WINDOW
# UPDATE WINDOW

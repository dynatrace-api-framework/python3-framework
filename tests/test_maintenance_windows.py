"""Test Cases For Maintenance Windows."""
import unittest
import user_variables
from tests import tooling_for_test
from dynatrace.tenant import maintenance
from dynatrace.requests.request_handler import TenantAPIs

CLUSTER = user_variables.FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = TenantAPIs.MAINTENANCE_WINDOWS


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
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
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
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[{'context': "CONTEXTLESS", 'key': "testing"}])
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
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
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[
                {'context': "CONTEXTLESS", 'key': "testing"},
                {'context': "CONTEXTLESS", 'key': "testing2"}
            ],
            match_any_tag=False
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
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
            "DAILY",
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_scope = maintenance.generate_scope(
            tags=[
                {'context': "CONTEXTLESS", 'key': "testing"},
                {'context': "CONTEXTLESS", 'key': "testing2"}
            ],
            match_any_tag=True
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
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
            #TODO Remove need for these variables. ONCE does not use them
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00"
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
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
            #TODO Remove need for these variables. ONCE does not use them
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00",
            day=maintenance.DayOfWeek.SUNDAY
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
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
            #TODO Remove need for these variables. ONCE does not use them
            "23:00",
            60,
            "2020-01-01 00:00",
            "2020-01-02 00:00",
            day=1
        )
        maintenance_json = maintenance.generate_window_json(
            "Test Payload",
            "Generating Payload for Test",
            "DETECT_PROBLEMS_AND_ALERT",
            maintenance_schedule,
            is_planned=True
        )
        result = maintenance.create_window(CLUSTER, TENANT, maintenance_json)
        self.assertEqual(result, tooling_for_test.expected_payload(
            mockserver_response_file))

class TestEnumTypes(unittest.TestCase):
    def test_suppression_enum_str(self):
        suppression = maintenance.Suppression(maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT)
        self.assertIsInstance(maintenance.Suppression.__str__(suppression), str)

    def test_suppression_enum_repr(self):
        suppression = maintenance.Suppression(maintenance.Suppression.DETECT_PROBLEMS_AND_ALERT)
        self.assertIsInstance(maintenance.Suppression.__repr__(suppression), str)

    def test_day_of_week_enum_str(self):
        day_of_week = maintenance.DayOfWeek(maintenance.DayOfWeek.MONDAY)
        self.assertIsInstance(maintenance.DayOfWeek.__str__(day_of_week), str)

    def test_day_of_week_enum_repr(self):
        day_of_week = maintenance.DayOfWeek(maintenance.DayOfWeek.MONDAY)
        self.assertIsInstance(maintenance.DayOfWeek.__repr__(day_of_week), str)

    def test_context_enum_str(self):
        context = maintenance.Context(maintenance.Context.CONTEXTLESS)
        self.assertIsInstance(maintenance.Context.__str__(context), str)

    def test_context_enum_repr(self):
        context = maintenance.Context(maintenance.Context.CONTEXTLESS)
        self.assertIsInstance(maintenance.Context.__repr__(context), str)

    def test_recurrence_type_enum_str(self):
        recurrence_type = maintenance.RecurrenceType(maintenance.RecurrenceType.DAILY)
        self.assertIsInstance(maintenance.RecurrenceType.__str__(recurrence_type), str)

    def test_recurrence_type_enum_repr(self):
        recurrence_type = maintenance.RecurrenceType(maintenance.RecurrenceType.DAILY)
        self.assertIsInstance(maintenance.RecurrenceType.__repr__(recurrence_type), str)

    def test_filter_type_enum_str(self):
        suppression = maintenance.FilterType(maintenance.FilterType.APM_SECURITY_GATEWAY)
        self.assertIsInstance(maintenance.FilterType.__str__(suppression), str)

    def test_filter_type_enum_repr(self):
        suppression = maintenance.FilterType(maintenance.FilterType.APM_SECURITY_GATEWAY)
        self.assertIsInstance(maintenance.FilterType.__repr__(suppression), str)


class TestTagParsing(unittest.TestCase):
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
                {'context': 'Context', 'key': '[KeyWithSquares]:AndColons:Value'},
                {'context': 'CONTEXTLESS', 'key': '[][KeywithSquares]'},
        ]

        all_tests_passed = True
        for i in range(0, len(test_tag_list)):
            processed_tag = test_tag_list[i]
            self.assertTrue(
                    (result := maintenance.parse_tag(processed_tag)) == test_tag_expected_results[i], 
                    f"Test {i}: {result} did not match {test_tag_expected_results[i]}")

if __name__ == '__main__':
    unittest.main()

# CREATE TESTS LEFT:
# INCORRECT DAY OF WEEK
# INCORRECT DAY OF MONTH

# Single Entity
# Multi Entity
# Single Tag with Filter Type
# Mutli Tags with Filter Type
# Single Tag with Management Zone
# Multi Tags with Management Zone

# EXCEPTION TEST CASES:
# INVALID RECURRENCE
# INVALID WEEK DAY
# INVALID MONTH DAY
# WEEK DAY NOT SUPPLIED
# MONTH DAY NOT SUPPLIED
# MONTHLY DAY OUT OF SCOPE (31 in 30 day month)
# INVALID FILTER_TYPE
# MANAGEMENT_ZONE WITHOUT TAG
# FILTER_TYPE WITHOUT TAG

# OTHER TEST CASES:
# GET ALL WINDOWS
# GET DETAILS OF WINDOW
# DELETE WINDOW
# UPDATE WINDOW
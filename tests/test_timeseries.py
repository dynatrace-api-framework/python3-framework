"""Test cases for Timeseries (V1) API operations"""

import unittest
from tests import tooling_for_test as testtools
from user_variables import FULL_SET
from dynatrace.tenant import timeseries
from dynatrace.framework.request_handler import TenantAPIs, HTTP

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.TIMESERIES)
TIMESERIES_ID = "custom.test.timeseries"
RESPONSE_DIR = "tests/mockserver_payloads/responses/timeseries"


class TestGetTimeseries(unittest.TestCase):
    """Test cases for fetch operations"""

    def test_get_metric_with_prediction(self):
        """Test getting metric data with prediction"""
        response_file = f"{RESPONSE_DIR}/get_predict.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type=str(HTTP.GET),
            parameters={
                "timeseriesIdentifier": TIMESERIES_ID,
                "relativeTime": "30mins",
                "includeData": "True",
                "predict": "True"
            },
            response_file=response_file
        )

        result = timeseries.get_metric_data_with_prediction(
            CLUSTER, TENANT, TIMESERIES_ID
        )
        expected_result = testtools.expected_payload(
            response_file
        ).get("dataResult").get("dataPoints")

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()

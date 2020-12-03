"""
Test Suite for Metrics API
"""
import unittest
# from user_variables import FULL_SET  # pylint: disable=import-error
from user_variables import FULL_SET
from tests import tooling_for_test as testtools
from dynatrace.framework.exceptions import InvalidAPIResponseException
from dynatrace.framework.request_handler import TenantAPIs
from dynatrace.tenant import metrics

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
URL_PATH = str(TenantAPIs.METRICS)
METRIC_SELECTOR = 'builtin:host.mem.avail.*'
REQUEST_DIR = "tests/mockserver_payloads/requests/metrics"
RESPONSE_DIR = "tests/mockserver_payloads/responses/metrics"


class TestGetMetrics(unittest.TestCase):
    """Tests cases for fetching metrics and their details."""

    def test_get_metric_descriptor(self):
        """Test fetching descriptors for metrics matching selector."""
        response_file = f"{RESPONSE_DIR}/descriptors.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                "metricSelector": METRIC_SELECTOR
            },
            response_file=response_file
        )

        result = metrics.get_metric_descriptor(
            CLUSTER, TENANT, **{'metricSelector': METRIC_SELECTOR}
        )
        expected_result = testtools.expected_payload(response_file).get('metrics')
        self.assertEqual(result, expected_result)

    def test_get_metric_count(self):
        """Test fetching the count of metrics matching selector."""
        response_file = f"{RESPONSE_DIR}/descriptors.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                "metricSelector": METRIC_SELECTOR
            },
            response_file=response_file
        )

        result = metrics.get_metric_count(
            CLUSTER, TENANT, **{'metricSelector': METRIC_SELECTOR}
        )
        expected_result = testtools.expected_payload(response_file).get('totalCount')
        self.assertEqual(result, expected_result)

    def test_get_metric_data(self):
        """Test fetching datapoints for metrics matching selector."""
        response_file = f"{RESPONSE_DIR}/datapoints.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/query",
            request_type="GET",
            parameters={
                "metricSelector": "builtin:host.mem.avail.pct",
                "resolution": "Inf"
            },
            response_file=response_file
        )

        result = metrics.get_metric_data(
            CLUSTER, TENANT, **{'metricSelector': 'builtin:host.mem.avail.pct',
                                'resolution': 'Inf'}
        )
        data = testtools.expected_payload(response_file).get('result')[0].get('data')
        expected_result = {'builtin:host.mem.avail.pct': data}
        self.assertEqual(result, expected_result)

    def test_get_metric_dimension_count(self):
        """Test fetching dimension count for metrics matching selector."""
        response_file = f"{RESPONSE_DIR}/descriptors.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                "metricSelector": METRIC_SELECTOR
            },
            response_file=response_file
        )

        result = metrics.get_metric_dimension_count(CLUSTER, TENANT, METRIC_SELECTOR)
        expected_result = 3
        self.assertEqual(result, expected_result)

    def test_get_metric_ddus(self):
        """Test fetching the estimated DDUs consumed by a metric."""
        response_file = f"{RESPONSE_DIR}/descriptors.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=URL_PATH,
            request_type="GET",
            parameters={
                "metricSelector": METRIC_SELECTOR
            },
            response_file=response_file
        )

        result = metrics.get_metric_estimated_ddus(CLUSTER, TENANT, METRIC_SELECTOR)
        expected_result = 3 * 525.6
        self.assertEqual(result, expected_result)

    def test_get_metric_data_multipage(self):
        """Test fetching datapoints for metrics matching selector in a
        multipage result set.
        """
        response_file1 = f"{RESPONSE_DIR}/datapoints_page1.json"
        response_file2 = f"{RESPONSE_DIR}/datapoints_page2.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/query",
            request_type="GET",
            parameters={
                "metricSelector": "builtin:host.mem.avail.pct",
                "resolution": "Inf"
            },
            response_file=response_file1,
            mock_id="req1"
        )
        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/query",
            request_type="GET",
            parameters={
                "nextPageKey": "ABC123"
            },
            response_file=response_file2,
            mock_id="req2"
        )

        result = metrics.get_metric_data(
            CLUSTER, TENANT, **{'metricSelector': 'builtin:host.mem.avail.pct',
                                'resolution': 'Inf'}
        )
        data = testtools.expected_payload(response_file1).get('result')[0].get('data')
        data.extend(
            testtools.expected_payload(response_file2).get('result')[0].get('data')
        )
        expected_result = {'builtin:host.mem.avail.pct': data}

        self.assertEqual(result, expected_result)


class TestPushMetrics(unittest.TestCase):
    """Tests for metrics ingestion capability"""

    def test_metrics_ingest(self):
        """Tests simple metric ingestion"""
        request_file = f"{REQUEST_DIR}/payload.txt"
        with open(file=request_file, mode='r') as text:
            payload = text.read()

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/ingest",
            request_type="POST",
            request_data=request_file,
            response_code=202
        )

        result = metrics.ingest_metrics(CLUSTER, TENANT, payload)
        self.assertEqual(result.status_code, 202)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling during metrics operations"""

    def test_fetch_metric_not_resolved(self):
        """Tests error handling for missing metric selector.
        """
        response_file = f"{RESPONSE_DIR}/error.json"

        testtools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path=f"{URL_PATH}/query",
            request_type="GET",
            response_file=response_file,
            response_code=400
        )

        with self.assertRaises(InvalidAPIResponseException):
            metrics.get_metric_data(CLUSTER, TENANT)


if __name__ == '__main__':
    unittest.main()

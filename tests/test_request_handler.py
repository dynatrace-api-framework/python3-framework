"""Test suite for testing framework core functionality"""
import unittest
import time
from user_variables import FULL_SET  # pylint: disable=import-error
from tests import tooling_for_test as testools
from dynatrace.framework import request_handler as rh

CLUSTER = FULL_SET["mockserver1"]
TENANT = "tenant1"
RESPONSE_DIR = "tests/mockserver_payloads/responses/request_handler"


class TestEnums(unittest.TestCase):
    """Test cases for enum classes"""

    def test_cluster_apis(self):
        """Tests the string representation of cluster API enum"""
        result = rh.ClusterAPIs.BASE.__str__()
        expected_result = rh.ClusterAPIs.BASE.value

        self.assertEqual(result, expected_result)

    def test_tenant_apis(self):
        """Tests the string representation of tenant API enum"""
        result = rh.TenantAPIs.PROBLEMS.__str__()
        expected_result = rh.TenantAPIs.PROBLEMS.value

        self.assertEqual(result, expected_result)

    def test_http_enum(self):
        """Tests the string and dunder representation of HTTP API enum"""
        result1 = rh.HTTP.POST.__str__()
        result2 = rh.HTTP.POST.__repr__()
        expected_result = rh.HTTP.POST.name

        self.assertEqual(result1, expected_result)
        self.assertEqual(result2, expected_result)


class TestRequests(unittest.TestCase):
    """Test cases for making API requests"""

    def test_request_slowdown(self):
        """Tests the adding of delays in case of rate limit approaching"""
        testools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path="/testpath",
            request_type=str(rh.HTTP.GET),
            response_code=200,
            rate_remaining="25",
            rate_limit="100"
        )

        before = time.time()
        rh.make_api_call(CLUSTER, "/testpath", TENANT)
        after = time.time()

        result = after - before
        expected_result = 1

        self.assertGreaterEqual(result, expected_result)

    def test_request_saas(self):
        """Tests making a normal API request for SaaS"""
        testools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path="/testpath",
            request_type=str(rh.HTTP.GET),
            response_code=200
        )

        result = rh.make_api_call(
            cluster=CLUSTER,
            tenant=TENANT,
            endpoint="/testpath"
        ).status_code
        expected_result = 200

        self.assertEqual(result, expected_result)

    def test_request_managed(self):
        """Tests making a normal API request for Managed"""
        MGD_CLUSTER = CLUSTER.copy()
        MGD_CLUSTER["is_managed"] = True

        testools.create_mockserver_expectation(
            cluster=MGD_CLUSTER,
            tenant=TENANT,
            url_path="/e/mockserver/testpath",
            request_type=str(rh.HTTP.GET),
            response_code=200,
            mock_id="managed"
        )

        result = rh.make_api_call(
            cluster=MGD_CLUSTER,
            tenant=TENANT,
            endpoint="/testpath"
        ).status_code
        expected_result = 200

        self.assertEqual(result, expected_result)

    def test_v1_multipage_request(self):
        """Tests making a multipage result request for v1 style pagination"""
        response_file1 = f"{RESPONSE_DIR}/v1_page1.json"
        response_file2 = f"{RESPONSE_DIR}/v1_page2.json"

        testools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path="/testpath",
            request_type=str(rh.HTTP.GET),
            response_file=response_file1,
            response_headers={
                "next-page-key": "ABC123"
            },
            mock_id="req1"
        )
        testools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path="/testpath",
            request_type=str(rh.HTTP.GET),
            response_file=response_file2,
            mock_id="req2"
        )
        result = rh.get_results_whole(CLUSTER, TENANT, "/testpath", api_version=1)
        expected_result = testools.expected_payload(response_file1)
        expected_result.extend(testools.expected_payload(response_file2))

        self.assertEqual(result, expected_result)

    def test_v2_multipage_request(self):
        """Tests making a multipage result request for v2 style pagination"""
        response_file1 = f"{RESPONSE_DIR}/v2_page1.json"
        response_file2 = f"{RESPONSE_DIR}/v2_page2.json"

        testools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path="/testpath",
            request_type=str(rh.HTTP.GET),
            response_file=response_file1,
            mock_id="req1"
        )
        testools.create_mockserver_expectation(
            cluster=CLUSTER,
            tenant=TENANT,
            url_path="/testpath",
            request_type=str(rh.HTTP.GET),
            response_file=response_file2,
            mock_id="req2"
        )
        result = rh.get_results_whole(
            CLUSTER, TENANT, "/testpath", api_version=2, item="items"
        ).get("items")
        expected_result = testools.expected_payload(response_file1).get("items")
        expected_result.extend(testools.expected_payload(response_file2).get("items"))

        self.assertEqual(result, expected_result)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling"""

    def test_v2_multipage_no_item(self):
        """Tests error handling for V2 multipage API with missing item.
        Item to be collected must be specified.
        """
        with self.assertRaises(ValueError):
            rh.get_results_whole(CLUSTER, TENANT, "/testpath", api_version=2)

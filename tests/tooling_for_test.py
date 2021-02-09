"""Mockserver Expectation Setup"""
import json
import logging
import requests
from dynatrace.framework.request_handler import generate_tenant_url

logging.basicConfig(filename="testing_tools.log", level=logging.DEBUG)


def create_mockserver_expectation(cluster, tenant, url_path, request_type, **kwargs):
    """Creates an expectation for a mockserver request.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - name of Tenant (as taken from variable set)\n
    @param url_path (str) - path for the request that matches this expectation\n
    @param request_type (HTTP str) - type of HTTP request that matches expectation
    \n
    @kwargs parameters (dict) - query string parameters for the request\n
    @kwargs request_file (str) - path to JSON file representing request payload\n
    @kwargs request_data (str) - path to plain-text file representing request payload
    @kwargs response_body (str) - path to JSON file representing response to request\n
    @kwargs response_code (int) - HTTP response code
    \n
    @throws ValueError - when the response code is not positive
    """
    requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

    if cluster.get("is_managed"):
        expected_path = f"/e/{cluster.get('tenant').get(tenant)}{url_path}"
        expectation_url = f"http://{cluster['url']}/mockserver/expectation"
    else:
        expected_path = url_path
        expectation_url = f"{generate_tenant_url(cluster, tenant)}/mockserver/expectation"

    expectation = {
        "httpRequest": {
            "headers": {
                "Authorization": [f"Api-Token {cluster.get('api_token').get(tenant)}"]
            },
            "path": expected_path,
            "method": request_type
        },
        "httpResponse": {
            "statusCode": 200
        },
        "times": {
            "remainingTimes": 1,
            "unlimited": False
        },
        "id": "OneOff",
    }

    logging.debug("URL PATH: %s", url_path)
    logging.debug("KWARGS %s", kwargs)

    # Mockserver expectation syntax expects each parameter's matching values
    # to be given as a list (even if just 1 value)
    if 'parameters' in kwargs:
        expectation["httpRequest"]["queryStringParameters"] = {
            param: [
                kwargs['parameters'][param]
            ]
            for param in kwargs['parameters']
        }

    if "request_file" in kwargs:
        with open(kwargs['request_file']) as open_file:
            request_payload = json.load(open_file)
        expectation["httpRequest"]["body"] = {
            "type": "JSON",
            "json": request_payload,
        }

    if "request_data" in kwargs:
        with open(kwargs['request_data']) as file:
            request_data = file.read()
        expectation["httpRequest"]["body"] = {
            "type": "STRING",
            "string": request_data,
            "contentType": "text/plain"
        }

    if "response_file" in kwargs:
        with open(kwargs['response_file']) as open_file:
            response_payload = json.load(open_file)
        expectation["httpResponse"]["body"] = {
            "type": "JSON",
            "json": response_payload,
        }
        expectation["httpResponse"]["headers"] = {
            "content-type": ["application/json"],
            "x-ratelimit-remaining": ['100000000'],
            "x-ratelimit-limit": ['100000000']
        }

    if "response_code" in kwargs:
        expectation["httpResponse"]["statusCode"] = kwargs["response_code"]

    if "mock_id" in kwargs:
        expectation["id"] = kwargs["mock_id"]

    logging.debug(expectation)

    test_req = requests.request(
        "PUT",
        expectation_url,
        json=expectation,
        verify=False
    )
    logging.debug(test_req.text)
    if test_req.status_code > 300:
        print(expectation, test_req.status_code, test_req.text, end="\n")
        raise ValueError(test_req.status_code)


def expected_payload(json_file):
    """The payload that should be tested against

    Args:
        json_file (str): file name for result json

    Returns:
        dict: payload of the expected result JSON
    """
    with open(json_file) as open_file:
        return json.load(open_file)

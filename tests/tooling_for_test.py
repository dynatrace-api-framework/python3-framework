"""Mockserver Expectation Setup"""
import json
import logging
import requests
from dynatrace.requests.request_handler import generate_tenant_url

logging.basicConfig(filename="testing_tools.log", level=logging.DEBUG)


def create_mockserver_expectation(cluster, tenant, url_path, request_type, **kwargs):
    """Create Payload For MockServer to expect and respond

    Args:
        cluster (Dictionary): [description]
        tenant (str): [description]
        url_path (str): [description]
        request_type (HTTP str): [description]

    Raises:
        ValueError: [description]
    """
    requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member
    expectation = {
        "httpRequest": {
            "headers": {
                "Authorization": [f"Api-Token {cluster.get('api_token').get(tenant)}"],
                "x-ratelimit-remaining": 100000000,
                "x-ratelimit-limit": 100000000
            },
            "path": url_path,
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
    # Paramaters should always at least have Api-Token
    if 'parameters' in kwargs:
        expectation["httpRequest"]["queryStringParameters"] = kwargs['parameters']

    if "request_file" in kwargs:
        with open(kwargs['request_file']) as open_file:
            request_payload = json.load(open_file)
        expectation["httpRequest"]["body"] = {
            "type": "JSON",
            "json": request_payload,
        }

    if "response_file" in kwargs:
        with open(kwargs['response_file']) as open_file:
            response_payload = json.load(open_file)
        expectation["httpResponse"]["body"] = {
            "type": "JSON",
            "json": response_payload,
        }
        expectation["httpResponse"]["headers"] = {
            "content-type": ["application/json"]
        }

    if "response_code" in kwargs:
        expectation["httpResponse"]["statusCode"] = kwargs["response_code"]

    if "mock_id" in kwargs:
        expectation["id"] = kwargs["mock_id"]

    logging.debug(expectation)

    expectation_url = f"{generate_tenant_url(cluster, tenant)}/mockserver/expectation"
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

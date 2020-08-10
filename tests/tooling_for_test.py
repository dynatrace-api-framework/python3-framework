"""Mockserver Expectation Setup"""
import requests
import json
import logging
from dynatrace.requests.request_handler import generate_tenant_url

logging.basicConfig(filename="testing_tools.log", level=logging.DEBUG)


def create_mockserver_expectation(cluster, tenant, url_path, request_type, **kwargs):
    requests.packages.urllib3.disable_warnings()
    expectation = {
        "httpRequest": {
            "headers": {
                "Authorization": [f"Api-Token {cluster.get('api_token').get(tenant)}"],
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

    logging.debug(f"URL PATH: {url_path}")
    logging.debug(f"KWARGS {kwargs}")
    # Paramaters should always at least have Api-Token
    if 'parameters' in kwargs:
        expectation["httpRequest"]["queryStringParameters"] = kwargs['parameters']

    if "request_file" in kwargs:
        with open(kwargs['request_file']) as f:
            request_payload = json.load(f)
        expectation["httpRequest"]["body"] = {
            "type": "JSON",
            "json": request_payload,
        }

    if "response_file" in kwargs:
        with open(kwargs['response_file']) as f:
            response_payload = json.load(f)
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
    with open(json_file) as f:
        return json.load(f)

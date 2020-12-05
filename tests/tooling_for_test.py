"""Mockserver Expectation Setup"""
import json
import logging
import requests

logging.basicConfig(filename="testing_tools.log", level=logging.DEBUG)
EXPECTATION_URL = "https://mockserver.mockserver:5555/mockserver/expectation"


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
    @kwargs response_file (str) - path to JSON file representing response to request\n
    @kwargs response_body (dict) - dictionary representing the JSON response to request\n
    @kwargs response_code (int) - HTTP response code
    \n
    @throws ValueError - when the response code is not positive
    """
    requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

    logging.debug("URL PATH: %s", url_path)
    logging.debug("KWARGS %s", kwargs)

    # Get the appropriate token for the API
    if "onpremise" in url_path:
        api_token = cluster["cluster_token"]
    else:
        api_token = cluster["api_token"][tenant]

    # Defaults that can be overridden in kwargs
    response_code = kwargs.get("response_code", 200)
    request_id = kwargs.get("mock_id", "OneOff")
    rate_remaining = kwargs.get("rate_remaining", "100000000")
    rate_limit = kwargs.get("rate_limit", "100000000")
    content_type = kwargs.get("content_type", "application/json")
    parameters = kwargs.get("parameters", None)
    request_file = kwargs.get("request_file", None)
    request_data = kwargs.get("request_data", None)
    response_file = kwargs.get("response_file", None)
    response_data = kwargs.get("response_data", None)
    response_headers = kwargs.get("response_headers", None)
    request_body = None
    response_body = None

    expectation = {
        "httpRequest": {
            "headers": {
                "Authorization": [f"Api-Token {api_token}"]
            },
            "path": url_path,
            "method": request_type
        },
        "httpResponse": {
            "statusCode": response_code,
            "headers": {
                "content-type": [content_type],
                "x-ratelimit-remaining": [rate_remaining],
                "x-ratelimit-limit": [rate_limit]
            }
        },
        "times": {
            "remainingTimes": 1,
            "unlimited": False
        },
        "id": request_id,
    }

    # Mockserver expectation syntax expects each parameter's matching values
    # to be given as a list (even if just 1 value)
    if parameters:
        parameters = {param: [parameters.get(param)] for param in parameters}
        expectation["httpRequest"]["queryStringParameters"] = parameters

    if response_file or response_data:
        response_body = {
            "type": "JSON",
            "json": expected_payload(response_file) if response_file else response_data,
        }
        expectation["httpResponse"]["body"] = response_body

    if request_file:
        request_body = {
            "type": "JSON",
            "json": expected_payload(request_file),
        }
        expectation["httpRequest"]["body"] = request_body

    if request_data:
        with open(kwargs['request_data']) as file:
            data = file.read()
        request_body = {
            "type": "STRING",
            "string": data,
            "contentType": "text/plain"
        }
        expectation["httpRequest"]["body"] = request_body

    if response_headers:
        for header in response_headers:
            expectation["httpResponse"]["headers"][header] = [response_headers[header]]

    logging.debug(expectation)

    test_req = requests.request(
        "PUT",
        EXPECTATION_URL,
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

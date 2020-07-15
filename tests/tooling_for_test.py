"""Mockserver Expectation Setup"""
import requests
import json
from dynatrace.requests.request_handler import generate_tenant_url, no_ssl_verification


def create_mockserver_expectation(cluster, tenant, url_path, request_type, parameters, response_payload_file=None, mock_id=None):
  expectation = {
      "httpRequest": {
          "queryStringParameters": {
              "Api-Token": ["sample_api_token"]  # TODO Change this Hard Code
          },
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

  # Paramaters should always at least have Api-Token
  expectation["httpRequest"]["queryStringParameters"] = parameters

  if response_payload_file:
    with open(response_payload_file) as f:
      response_payload = json.load(f)
    expectation["httpResponse"]["body"] = {
        "type": "JSON",
        "json": response_payload,
    }

  if mock_id:
    expectation["id"] = mock_id

  expectation_url = generate_tenant_url(
      cluster, tenant) + "/mockserver/expectation"
  with no_ssl_verification():
    test_req = requests.request(
        "PUT", expectation_url, json=expectation, verify=False)
    if test_req.status_code > 300:
      print(expectation, test_req.status_code, test_req.text, end="\n")
      raise ValueError(test_req.status_code)


def expected_payload(json_file):
  with open(json_file) as f:
    return json.load(f)
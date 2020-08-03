"""Mockserver Expectation Setup"""
import requests
import json
from dynatrace.requests.request_handler import generate_tenant_url


def create_mockserver_expectation(cluster, tenant, url_path, request_type, **kwargs):
  requests.packages.urllib3.disable_warnings()
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
  if 'parameters' in kwargs:
    expectation["httpRequest"]["queryStringParameters"] = kwargs['parameters']

  if "request_payload_file" in kwargs:
    with open(kwargs['request_payload_file']) as f:
      request_payload = json.load(f)
    expectation["httpRequest"]["body"] = {
        "type": "JSON",
        "json": request_payload,
    }

  if "response_payload_file" in kwargs:
    with open(kwargs['response_payload_file']) as f:
      response_payload = json.load(f)
    expectation["httpResponse"]["body"] = {
        "type": "JSON",
        "json": response_payload,
    }
    expectation["httpResponse"]["headers"] = {
        "content-type": ["application/json"]
    }

  if "mock_id" in kwargs:
    expectation["id"] = kwargs["mock_id"]

  expectation_url = f"{generate_tenant_url(cluster, tenant)}/mockserver/expectation"
  test_req = requests.request(
      "PUT",
      expectation_url,
      json=expectation,
      verify=False
  )
  if test_req.status_code > 300:
    print(expectation, test_req.status_code, test_req.text, end="\n")
    raise ValueError(test_req.status_code)


def expected_payload(json_file):
  with open(json_file) as f:
    return json.load(f)

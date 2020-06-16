"""Make API Request to available Dynatrace API"""
import warnings
import contextlib
import requests
from urllib3.exceptions import InsecureRequestWarning

OLD_MERGE_ENVIRONMENT_SETTINGS = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
  """Silence Request Warning for Unchecked SSL"""
  opened_adapters = set()

  def merge_environment_settings(self, url, proxies, stream, verify, cert):
    # Verification happens only once per connection so we need to close
    # all the opened adapters once we're done. Otherwise, the effects of
    # verify=False persist beyond the end of this context manager.
    opened_adapters.add(self.get_adapter(url))

    settings = OLD_MERGE_ENVIRONMENT_SETTINGS(self, url, proxies, stream, verify, cert)

    return settings

  requests.Session.merge_environment_settings = merge_environment_settings

  try:
    with warnings.catch_warnings():
      warnings.simplefilter('ignore', InsecureRequestWarning)
      yield
  finally:
    requests.Session.merge_environment_settings = OLD_MERGE_ENVIRONMENT_SETTINGS

    for adapter in opened_adapters:
      try:
        adapter.close()
      except Exception:
        pass

def check_response(response):
  """Checks if the Reponse has a Successful Status Code"""
  if not 200 <= response.status_code <= 299:
    raise Exception(
        "Response Error\n" + response.url + "\n" + str(response.status_code) + "\n" + response.text
    )

def check_managed(managed_bool):
  """Checks if the Cluster Operation is valid (Managed) for the current cluster"""
  if not managed_bool:
    raise Exception("Cluster Operations not supported for SaaS!")

def sanitize_endpoint (endpoint):
  if endpoint[0] == '/':
    endpoint = endpoint [1:]
  return endpoint

def generate_tenant_url(cluster, tenant):
  """Generate URL based on SaaS or Managed"""
  url = "https://"
  if cluster["is_managed"]:
    url = url + cluster['url'] + "/e/" + cluster['tenant'][tenant]
  else:
    url = url + cluster['tenant'][tenant] + "." + cluster['url']
  return url

def cluster_get(cluster, endpoint, params=None):
  """Get Request to Cluster API"""
  check_managed(cluster["is_managed"])

  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['cluster_token']
    verify = (True if "verify_ssl" not in cluster else cluster ["verify_ssl"])
    response = requests.get(
        "https://" + cluster['url'] + "/api/v1.0/onpremise/" + endpoint,
        params=params,
        verify=verify
    )
    check_response(response)
    return response


def cluster_post(cluster, endpoint, params=None, json=None):
  """Post Request to Cluster API"""
  check_managed(cluster["is_managed"])

  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['cluster_token']

    response =  requests.post(
        "https://" + cluster['url'] + "/api/v1.0/onpremise/" + endpoint,
        params=params,
        json=json,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"])
    )
    check_response(response)
    return response

def cluster_put(cluster, endpoint, params=None, json=None):
  """Post Request to Cluster API"""
  check_managed(cluster["is_managed"])

  if not params:
    params = {}
  
  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['cluster_token']

    response =  requests.put(
        "https://" + cluster['url'] + "/api/v1.0/onpremise/" + endpoint,
        params=params,
        json=json,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"])
    )
    check_response(response)
    return response

def cluster_delete(cluster, endpoint, params=None, json=None):
  """Delete Request to Cluster API"""
  check_managed(cluster["is_managed"])

  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['cluster_token']
    response =  requests.delete(
        "https://" + cluster['url'] + "/api/v1.0/onpremise/" + endpoint,
        params=params,
        json=json,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"])
    )
    check_response(response)
    return response

def env_get(cluster, tenant, endpoint, params=None):
  """Get Request to Tenant Environment API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]
    response = requests.get(
        generate_tenant_url(cluster, tenant) + "/api/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"])
    )
    check_response(response)
    return response

def env_post(cluster, tenant, endpoint, params=None, json=None):
  """Post Request to Tenant Environment API"""
  if not params:
    params = {}

    endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]

    response = requests.post(
        generate_tenant_url(cluster, tenant) + "/api/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"]),
        json=json
    )
    check_response(response)
    return response

def env_put(cluster, tenant, endpoint, params=None, json=None):
  """Post Request to Tenant Environment API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]

    response = requests.put(
        generate_tenant_url(cluster, tenant) + "/api/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"]),
        json=json
    )
    check_response(response)
    return response

def env_delete(cluster, tenant, endpoint, params=None):
  """Get Request to Tenant Environment API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]
    response = requests.delete(
        generate_tenant_url(cluster, tenant) + "/api/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"])
    )
    check_response(response)
    return response


def config_get(cluster, tenant, endpoint, params=None, json=None):
  """Get Request to Tenant Configuration API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]

    response = requests.get(
        generate_tenant_url(cluster, tenant) + "/api/config/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"]),
        json=json
    )
    check_response(response)
    return response

def config_post(cluster, tenant, endpoint, params=None, json=None):
  """Post Request to Tenant Configuration API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]

    response = requests.post(
        generate_tenant_url(cluster, tenant) + "/api/config/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"]),
        json=json
    )
    check_response(response)
    return response

def config_put(cluster, tenant, endpoint, params=None, json=None):
  """Put Request to Tenant Configuration API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]

    response = requests.put(
        generate_tenant_url(cluster, tenant) + "/api/config/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"]),
        json=json
    )
    check_response(response)
    return response

def config_delete(cluster, tenant, endpoint, params=None, json=None):
  """Delete Request to Tenant Configuration API"""
  if not params:
    params = {}

  endpoint = sanitize_endpoint(endpoint)

  with no_ssl_verification():
    params['Api-Token'] = cluster['api_token'][tenant]

    response = requests.delete(
        generate_tenant_url(cluster, tenant) + "/api/config/v1/" + endpoint,
        params=params,
        verify=(True if "verify_ssl" not in cluster else cluster ["verify_ssl"]),
        json=json
    )
    check_response(response)
    return response

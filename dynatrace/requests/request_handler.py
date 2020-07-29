"""Make API Request to available Dynatrace API"""
import requests
import time
from dynatrace.exceptions import InvalidAPIResponseException, ManagedClusterOnlyException
from enum import Enum, auto

requests.packages.urllib3.disable_warnings()

HTTPS_STR = "https://"


class ClusterAPIs(Enum):
    """
    Enum representing Dynatrace Cluster REST API endpoints.\n
    Use these values when adding the 'endpoint' argument.
    """
    BASE = "/api/v1.0/onpremise"
    CLUSTER = f"{BASE}/cluster"
    CONFIG = f"{CLUSTER}/configuration"
    CONFIG_STATUS = f"{CONFIG}/status"
    SSL = f"{BASE}/sslCertificate"
    SSL_STORE = f"{SSL}/store"
    SSO = ""  # Need to confirm endpoint
    GROUPS = f"{BASE}/groups"
    USERS = f"{BASE}/users"

    def __str__(self):
        return self.value


class TenantAPIs(Enum):
    """
    Enum representing Dynatrace Tenant REST API endpoints.\n
    Use these values when adding the 'endpoint' argument.
    """
    PROBLEM_DETAILS = "/api/v1/problem/details"
    PROBLEM_FEED = "/api/v1/problem/feed"
    PROBLEM_STATUS = "/api/v1/problem/status"
    DEPLOY_ONEAGENT = "/api/v1/deployment/installer/agent"
    DEPLOY_ONEAGENT_CONNECTION_INFO = "/api/v1/deployment/installer/agent/connectioninfo"
    DEPLOY_ONEAGENT_CONNECTION_ENDPOINTS = "/api/v1/deployment/installer/agent/connectioninfo/endpoints"
    DEPLOY_ACTIVEGATE = "/api/v1/deployment/installer/gateway"
    DEPLOY_BOSH = "/api/v1/deployment/boshrelease"
    EVENTS = "/api/v1/events"
    USER_SESSIONS = "/api/v1/userSessionQueryLanguage"
    TOKENS = "/api/v1/tokens"
    SYNTHETIC_MONITORS = "/api/v1/synthetic/monitors"
    SYNTHETIC_LOCATIONS = "/api/v1/synthetic/locations"
    SYNTHETIC_NODES = "/api/v1/synthetic/nodes"
    ENTITIES = "/api/v2/entities"
    METRICS = "/api/v2/metrics"
    TAGS = "/api/v2/tags"
    NETWORK_ZONES = "/api/v2/networkZones"
    MANAGEMENT_ZONES = "/api/config/v1/managementZones"
    V1_TOPOLOGY = "/api/v1/entity"
    MAINTENANCE_WINDOWS = "/api/config/v1/maintenanceWindows"
    ONEAGENTS = "/api/v1/oneagents"
    EXTENSIONS = "/api/config/v1/extensions"
    REQUEST_ATTRIBUTES = "/api/config/v1/service/requestAttributes/"
    REQUEST_NAMING = "/api/config/v1/service/requestNaming"

    def __str__(self):
        return self.value


class HTTP(Enum):
    '''
    Enum representing HTTP request methods.\n
    Use these values when adding the 'method' argument.
    '''
    GET = auto()
    PUT = auto()
    POST = auto()
    DELETE = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def make_api_call(cluster, endpoint, tenant=None, params=None, json=None, method=HTTP.GET):
    '''
    Function makes an API call in a safe way, taking into account the rate limits.
    This will ensure the API call will always go through, with the program waiting for the limit to reset if needed.\n
    
    @param cluster - Cluster dictionary from variable_set\n
    @param endpoint - API endpoint to call.\n
    @param tenant - String of tenant name used in cluster dictionary\n
    @param json - dictionary to be converted to JSON request\n
    @param method - HTTP method to use in call. Use HTTP enum.\n
    \n
    @return - response from request\n
    '''
    # Set the right URL for the operation
    url = f"{generate_tenant_url(cluster, tenant)}{endpoint}" if tenant else f"{HTTPS_STR}{cluster['url']}"

    if not params:
        params = {}

    # Get correct token for the operation
    if 'onpremise' in str(endpoint) or 'cluster' in str(endpoint):
        check_managed (cluster)
        params['Api-Token'] = cluster['cluster_token']
    else:
        params['Api-Token'] = cluster['api_token'][tenant]

    # Loop to retry in case of rate limits
    while True:
        if method == HTTP.GET:
            response = requests.get(url=url,
                                    params=params,
                                    verify=cluster.get('verify_ssl'))
        elif method == HTTP.PUT:
            response = requests.put(url=url,
                                    params=params,
                                    verify=cluster.get('verify_ssl'),
                                    json=json)
        elif method == HTTP.POST:
            response = requests.post(url=url,
                                     params=params,
                                     verify=cluster.get('verify_ssl'),
                                     json=json)
        elif method == HTTP.DELETE:
            response = requests.delete(url=url,
                                       params=params,
                                       verify=cluster.get('verify_ssl'))
        if check_response(response):
            break

    return response


def check_response(response):
    '''
    Checks if the Response has a Successful Status Code

    @param response - The response variable returned from a request\n

    '''
    headers = response.headers

    if response.status_code == 429:
        print("Endpoint request limit of "
              f"{headers['x-ratelimit-limit']} was reached!")
        # Wait until the limit resets and try again
        time_to_wait = int(headers['x-ratelimit-reset'])/1000000 - time.time()

        # Check that there's actually time to wait
        if time_to_wait > 0:
            print(f"Waiting {time_to_wait} sec until the limit resets.")
            time.sleep(float(time_to_wait))
        return False
    elif not 200 <= response.status_code <= 299:
        raise InvalidAPIResponseException(f"Response Error:\n{response.url}\n{response.status_code}\n{response.text}")

    return True


def check_managed(cluster):
    """Checks if the Cluster Operation is valid (Managed) for the current cluster"""
    if not cluster['is_managed']:
        raise ManagedClusterOnlyException()


def generate_tenant_url(cluster, tenant):
    """Generate URL based on SaaS or Managed"""
    url = HTTPS_STR
    if cluster["is_managed"]:
        url += cluster['url'] + "/e/" + cluster['tenant'][tenant]
    else:
        url += cluster['tenant'][tenant] + "." + cluster['url']
    return url

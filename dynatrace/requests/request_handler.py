"""Make API Request to available Dynatrace API"""
from enum import Enum, auto
import time
import functools
import requests
from dynatrace.exceptions import InvalidAPIResponseException, ManagedClusterOnlyException


requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

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
        return str(self.value)


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
    DEPLOY_ONEAGENT_CONNECTION_ENDPOINTS = \
        "/api/v1/deployment/installer/agent/connectioninfo/endpoints"
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
        return str(self.value)


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
        return str(self.name)

    def __repr__(self):
        return str(self.name)


def slow_down(func):
    """
    Decorator for slowing down API requests. In case of SaaS limits are as low
    as 50/min. If current call is within the last 25% remaining requests (until
    the limit is reached) then a slow down of 1 sec is applied.
    *** Should only use to decorate API-calling functions ***
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        # Get the cluster from wrapped function
        if 'cluster' in kwargs:
            cluster = kwargs.get('cluster')
        else:
            cluster = args[0]

        # Only slow-down SaaS
        if not cluster.get('is_managed') and 'x-ratelimit-remaining' in response.headers:
            # Standard Dynatrace response headers
            req_remaining = int(response.headers.get('x-ratelimit-remaining'))
            req_limit = int(response.headers.get('x-ratelimit-limit'))
            # If 75% requests already made, slow down
            if req_remaining/req_limit <= 0.25:
                time.sleep(1)

        return response
    return wrapper


@slow_down
def make_api_call(cluster, endpoint, tenant=None, params=None, json=None, method=HTTP.GET):
    '''
    Function makes an API call in a safe way, taking into account the rate limits.
    This will ensure the API call will always go through.\n
    The program will wait for the limit to reset if needed.\n

    @param cluster - Cluster dictionary from variable_set\n
    @param endpoint - API endpoint to call.\n
    @param tenant - String of tenant name used in cluster dictionary\n
    @param json - dictionary to be converted to JSON request\n
    @param method - HTTP method to use in call. Use HTTP enum.\n
    \n
    @return - response from request\n
    '''
    # Set the right URL for the operation
    url = f"{generate_tenant_url(cluster, tenant)}{endpoint}" \
        if tenant else f"{HTTPS_STR}{cluster['url']}{endpoint}"

    if not params:
        params = {}

    # Get correct token for the operation
    if 'onpremise' in str(endpoint) or 'cluster' in str(endpoint):
        check_managed(cluster)
        headers = dict(Authorization=f"Api-Token {cluster['cluster_token']}")
    else:
        headers = dict(Authorization=f"Api-Token {cluster['api_token'][tenant]}")

    # Loop to retry in case of rate limits
    while True:
        response = requests.request(
            method=str(method),
            url=url,
            params=params,
            headers=headers,
            json=json,
            verify=cluster.get('verify_ssl')
        )
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

    if not 200 <= response.status_code <= 299:
        raise InvalidAPIResponseException(
            f"Response Error:\n{response.url}\n{response.status_code}\n{response.text}")

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

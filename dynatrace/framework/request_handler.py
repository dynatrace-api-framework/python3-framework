"""Make API Request to available Dynatrace API"""
from enum import Enum, auto
import time
import functools
import requests
from dynatrace.framework.exceptions import InvalidAPIResponseException, ManagedClusterOnlyException


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
def make_api_call(cluster, endpoint, tenant=None, method=HTTP.GET, **kwargs):
    """Function makes an API call in a safe way.
    It takes into account any API rate limits. This will ensure the API call
    will always go through. The program will wait for the limit to reset if
    needed.
    \n
    @param cluster (dict) - Cluster dictionary from variable_set\n
    @param endpoint (str) - API endpoint to call.\n
    @param tenant (str) - String of tenant name used in cluster dictionary\n
    @param method (str) - HTTP method to use in call. Use HTTP enum.
    \n
    @kwargs params (dict) - query string parameters\n
    @kwargs json (dict) - request body to be sent as JSON\n
    @kwargs body (str) - request body to be sent as plain text
    \n
    @returns - response from request\n
    """
    # Set the right URL for the operation
    url = f"{generate_tenant_url(cluster, tenant)}{endpoint}" \
        if tenant else f"{HTTPS_STR}{cluster['url']}{endpoint}"

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
            headers=headers,
            verify=cluster.get('verify_ssl'),
            **kwargs
        )
        if check_response(response):
            break

    return response


def get_results_whole(cluster, tenant, endpoint, **kwargs):
    """Gets a multi-paged result set and returns it whole.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)\n
    @param endpoint (str) - API endpoint to call. Use the TenantAPIs Enum.\n
    \n
    @kwargs item (str) - the item to be retrieved from results response (e.g. entities)\n
    \n
    @throws ValueError - when V2 API is used but no item is given
    """
    # Ensure it always makes at least 1 call
    cursor = 1
    # For V2 and OneAgents APIs must specify the item collected
    if '/api/v2/' in str(endpoint) or endpoint == TenantAPIs.ONEAGENTS:
        is_v2 = True
        if 'item' not in kwargs:
            raise ValueError("For V2 APIs you must provide collected item.")
        item = kwargs['item']
        results = {}
    else:
        is_v2 = False
        results = []

    while cursor:
        if cursor != 1:
            if not is_v2 or endpoint == TenantAPIs.ONEAGENTS:
                # V1 and OneAgents require all other query params are preserved
                kwargs['nextPageKey'] = cursor
            else:
                # V2 requires all other query params are removed
                kwargs = dict(nextPageKey=cursor)

        response = make_api_call(
            cluster=cluster,
            tenant=tenant,
            endpoint=endpoint,
            params=kwargs
        )

        # V2 returns additional data in response that should be preserved
        if is_v2:
            if cursor == 1:
                results = response.json()
            else:
                results[item].extend(response.json().get(item))
            cursor = response.json().get('nextPageKey')
        else:
            results.extend(response.json())
            cursor = response.headers.get('next-page-key')

    return results


def get_results_by_page(cluster, tenant, endpoint, **kwargs):
    """Gets a multi-paged result set one page at at time.
    Useful for parsing very large result sets (e.g. entities) in optimal manner.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)\n
    @param endpoint (str) - API endpoint to call. Use the TenantAPIs Enum.\n
    \n
    @kwargs item (str) - the item to be retrieved from results response (e.g. entities)\n
    \n
    @throws ValueError - when V2 API is used but no item is given
    """
    # Ensure it always makes at least 1 call
    cursor = 1
    # Check whether pagination behaviour is for V1 or V2 APIs
    if '/api/v2/' in str(endpoint):
        is_v2 = True
        if 'item' not in kwargs:
            raise ValueError("For is_v2 APIs you must provide collected item.")
        item = kwargs['item']
    else:
        is_v2 = False

    while cursor:
        if cursor != 1:
            # V2 requires all other query params are removed
            if is_v2:
                kwargs = dict(nextPageKey=cursor)
            # V1 requires all other query params are preserved
            else:
                kwargs['nextPageKey'] = cursor

        response = make_api_call(
            cluster=cluster,
            endpoint=endpoint,
            tenant=tenant,
            params=kwargs
        )

        # OneAgents API pagination behaves like V1 but results returned are like V2
        if is_v2 or endpoint == TenantAPIs.ONEAGENTS:
            yield response.json().get(item)
            cursor = response.json().get('nextPageKey')
        else:
            yield response.json()
            cursor = response.headers.get('next-page-key')


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

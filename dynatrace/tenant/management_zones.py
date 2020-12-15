"""Functions for Management Zone Operations via Configuration API"""

import json
from enum import Enum, auto
from dynatrace.framework import request_handler as rh, logging

ENDPOINT = str(rh.TenantAPIs.MANAGEMENT_ZONES)
logger = logging.get_logger(__name__)


class RuleTypes(Enum):
    """Accepted values for Management Zone rule types."""
    APPMON_SERVER = auto()
    APPMON_SYSTEM_PROFILE = auto()
    AWS_ACCOUNT = auto()
    AWS_APPLICATION_LOAD_BALANCER = auto()
    AWS_AUTO_SCALING_GROUP = auto()
    AWS_CLASSIC_LOAD_BALANCER = auto()
    AWS_NETWORK_LOAD_BALANCER = auto()
    AWS_RELATIONAL_DATABASE_SERVICE = auto()
    AZURE = auto()
    BROWSER_MONITOR = auto()
    CLOUD_APPLICATION = auto()
    CLOUD_APPLICATION_NAMESPACE = auto()
    CLOUD_FOUNDRY_FOUNDATION = auto()
    CUSTOM_APPLICATION = auto()
    CUSTOM_DEVICE = auto()
    CUSTOM_DEVICE_GROUP = auto()
    DATA_CENTER_SERVICE = auto()
    ENTERPRISE_APPLICATION = auto()
    ESXI_HOST = auto()
    EXTERNAL_MONITOR = auto()
    HOST = auto()
    HOST_GROUP = auto()
    HTTP_MONITOR = auto()
    KUBERNETES_CLUSTER = auto()
    MOBILE_APPLICATION = auto()
    OPENSTACK_ACCOUNT = auto()
    PROCESS_GROUP = auto()
    SERVICE = auto()
    WEB_APPLICATION = auto()

    def __str__(self):
        """Overriding default __str__ to return the name."""
        return self.name


def generate_mz_template(name, tags):
    """Generates a standard Management Zone with custom name and rules matching tags.
    The rules include Hosts, Services, Process Groups, Web & Mobile Applications,
    Browser, HTTP, and External Synthetic Tests, and Custom Device Groups.
    Tags must be given as a tuple in this order: context, key, value (optional).
    \n
    @param name (str) - The name of the Management Zone to be created\n
    @param tags (list(tuple)) - [0] is tag context, [1] is tag key, [2] is the tag value
    \n
    @returns dict - Management Zone
    """
    try:
        if not isinstance(tags, list):
            raise ValueError(
                f"Tags must be given as a list of tuples. Found {type(tags)} instead."
            )
        if not all(isinstance(tag, tuple) for tag in tags):
            raise ValueError(
                "All provided tags must be tuples. Found a mix of types instead."
            )
    except ValueError:
        logger.exception("Error: invalid format for tags object.", stack_info=True)
        raise
    logger.info("Building standard Management Zone from template")
    logger.debug("Name: %s; Tags: %s", name, tags)
    me_types = [
        RuleTypes.HOST, RuleTypes.SERVICE, RuleTypes.PROCESS_GROUP,
        RuleTypes.WEB_APPLICATION, RuleTypes.BROWSER_MONITOR, RuleTypes.HTTP_MONITOR,
        RuleTypes.MOBILE_APPLICATION, RuleTypes.CUSTOM_DEVICE_GROUP,
        RuleTypes.EXTERNAL_MONITOR
    ]
    mz_rules = [
        dict(
            type=str(me_type),
            enabled=True,
            propagationTypes=[],
            conditions=[
                dict(
                    key=dict(attribute=f"{me_type}_TAGS"),
                    comparisonInfo=dict(
                        type="TAG",
                        operator="EQUALS" if len(tag) > 2 else "TAG_KEY_EQUALS",
                        value=dict(
                            context=tag[0],
                            key=tag[1],
                            value=tag[2] if len(tag) > 2 else None
                        ),
                        negate=False
                    )
                ) for tag in tags
            ]
        ) for me_type in me_types
    ]

    mz_json = dict(name=name, rules=mz_rules)

    return mz_json


def add_management_zone(cluster, tenant, mz_json):
    """Adds a new management zone to the tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param mz_json (dict) - Management Zone definition, to be sent as JSON payload
    \n
    @returns str - ID of the newly created Management Zone, if successful
    """
    logger.info("Adding a new Management Zone in tenant %s", tenant)
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.POST,
        endpoint=ENDPOINT,
        json=mz_json
    )

    if "id" in response.json():
        return response.json()['id']

    return response.text


def update_management_zone(cluster, tenant, mz_id, mz_json):
    """Updates an existing Management Zone with given definition.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param mz_json (dict) - Management Zone definition, to be sent as JSON payload\n
    @param mz_id (str) - ID of the Management Zone to update
    \n
    @returns Response - HTTP Response to the request
    """
    logger.info("Updating Management Zone with ID %s in tenant %s", mz_id, tenant)

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.PUT,
        endpoint=f"{ENDPOINT}/{mz_id}",
        json=mz_json
    )

    return response


def delete_management_zone_by_id(cluster, tenant, mz_id):
    """Deletes an existing Management Zone, referenced by ID.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param mz_id (str) - ID of the Management Zone to delete
    \n
    @returns Response - HTTP Response to the request
    """
    logger.info("Deleting Management Zone with ID %s from tenant %s", mz_id, tenant)

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.DELETE,
        endpoint=f"{ENDPOINT}/{mz_id}"
    )

    return response


def delete_management_zone_by_name(cluster, tenant, mz_name):
    """Deletes an existing Management Zone, referenced by name.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param mz_name (str) - name of the Management Zone to delete
    \n
    @returns Response - HTTP Response to the request
    \n
    @throws RuntimeError - when Management Zone was not found in tenant
    """
    mz_id = get_management_zone_id(cluster, tenant, mz_name)

    if not mz_id:
        try:
            raise RuntimeError(
                f"Error: No Management Zone found with name {mz_id} in tenant {tenant}"
            )
        except RuntimeError:
            logger.exception("Error: Management Zone not found.", stack_info=True)
            raise

    logger.info("Deleting the Management Zone from tenant")
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.DELETE,
        endpoint=f"{ENDPOINT}/{mz_id}"
    )

    return response


def get_all_management_zones(cluster, tenant):
    """Gets all Management Zones within a Tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set
    \n
    @returns list - list of Management Zones
    """
    logger.info("Getting all Management Zones from tenant %s", tenant)
    management_zones = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT
    ).json().get("values")

    return management_zones


def get_management_zone_details(cluster, tenant, mz_id):
    """Gets the full details of a Management Zone referenced by ID.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param mz_id (str) - ID of the Management Zone to fetch
    \n
    @returns dict - Management Zone details
    """
    logger.info(
        "Getting details for Management Zone with id %s in tenant %s", mz_id, tenant
    )
    mz_details = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{mz_id}"
    ).json()

    return mz_details


def get_management_zone_id(cluster, tenant, mz_name):
    """Gets the ID of a Management Zone referenced by name.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param mz_name (str) - name of the Management Zone to find
    \n
    @returns str - ID of the Management Zone if found. None otherwise.
    """
    logger.info(
        "Finding ID for Management Zone with name %s in tenant %s", mz_name, tenant
    )
    mz_list = get_all_management_zones(cluster, tenant)

    for m_zone in mz_list:
        if m_zone['name'] == mz_name:
            return m_zone['id']
    return None


def import_mz_from_file(file):
    """Reads a Management Zone definition from a (JSON) file.
    \n
    @param file (str) - the file to read (must be valid JSON)
    \n
    @returns dict - dictionary created from reading the file
    """
    logger.info("Reading Management Zone from file.")
    with open(file=file, mode="r") as json_file:
        mz_details = json.load(json_file)

    return mz_details

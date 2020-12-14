"""Module for Entities API operations"""

from enum import Enum, auto
from dynatrace.framework import logging
from dynatrace.framework import request_handler as rh

logger = logging.get_logger(__name__)


class EntityTypes(Enum):
    """Accepted values for EntityType arguments"""
    HTTP_CHECK = auto()
    RELATIONAL_DATABASE_SERVICE = auto()
    APPLICATION = auto()
    KUBERNETES_NODE = auto()
    CONTAINER_GROUP_INSTANCE = auto()
    OPENSTACK_COMPUTE_NODE = auto()
    QUEUE = auto()
    EBS_VOLUME = auto()
    OPENSTACK_PROJECT = auto()
    PROCESS_GROUP = auto()
    EC2_INSTANCE = auto()
    GEOLOC_SITE = auto()
    DEVICE_APPLICATION_METHOD_GROUP = auto()
    AWS_AVAILABILITY_ZONE = auto()
    SYNTHETIC_TEST_STEP = auto()
    AZURE_STORAGE_ACCOUNT = auto()
    AZURE_IOT_HUB = auto()
    AWS_APPLICATION_LOAD_BALANCER = auto()
    CLOUD_APPLICATION_NAMESPACE = auto()
    BROWSER = auto()
    GEOLOCATION = auto()
    HTTP_CHECK_STEP = auto()
    HYPERVISOR_DISK = auto()
    AZURE_APP_SERVICE_PLAN = auto()
    NEUTRON_SUBNET = auto()
    S3BUCKET = auto()
    NETWORK_INTERFACE = auto()
    QUEUE_INSTANCE = auto()
    APPLICATION_METHOD_GROUP = auto()
    GCP_ZONE = auto()
    OPENSTACK_VM = auto()
    MOBILE_APPLICATION = auto()
    PROCESS_GROUP_INSTANCE = auto()
    HOST_GROUP = auto()
    SYNTHETIC_LOCATION = auto()
    SERVICE_INSTANCE = auto()
    GOOGLE_COMPUTE_ENGINE = auto()
    AZURE_SERVICE_BUS_TOPIC = auto()
    AZURE_TENANT = auto()
    CLOUD_APPLICATION = auto()
    AZURE_EVENT_HUB = auto()
    DEVICE_APPLICATION_METHOD = auto()
    AZURE_SERVICE_BUS_NAMESPACE = auto()
    VIRTUALMACHINE = auto()
    ELASTIC_LOAD_BALANCER = auto()
    AZURE_SUBSCRIPTION = auto()
    AZURE_REDIS_CACHE = auto()
    AWS_NETWORK_LOAD_BALANCER = auto()
    BOSH_DEPLOYMENT = auto()
    EXTERNAL_SYNTHETIC_TEST_STEP = auto()
    DOCKER_CONTAINER_GROUP_INSTANCE = auto()
    APPLICATION_METHOD = auto()
    AZURE_CREDENTIALS = auto()
    AZURE_MGMT_GROUP = auto()
    SERVICE_METHOD_GROUP = auto()
    AZURE_FUNCTION_APP = auto()
    AZURE_SQL_SERVER = auto()
    AZURE_SQL_DATABASE = auto()
    AZURE_VM = auto()
    OPENSTACK_AVAILABILITY_ZONE = auto()
    SWIFT_CONTAINER = auto()
    CLOUD_APPLICATION_INSTANCE = auto()
    SERVICE = auto()
    VMWARE_DATACENTER = auto()
    AZURE_EVENT_HUB_NAMESPACE = auto()
    VCENTER = auto()
    AZURE_SERVICE_BUS_QUEUE = auto()
    SERVICE_METHOD = auto()
    OS = auto()
    CONTAINER_GROUP = auto()
    AWS_CREDENTIALS = auto()
    AZURE_SQL_ELASTIC_POOL = auto()
    DATASTORE = auto()
    HYPERVISOR_CLUSTER = auto()
    SYNTHETIC_TEST = auto()
    EXTERNAL_SYNTHETIC_TEST = auto()
    AUTO_SCALING_GROUP = auto()
    CUSTOM_APPLICATION = auto()
    AZURE_API_MANAGEMENT_SERVICE = auto()
    DISK = auto()
    HYPERVISOR = auto()
    CUSTOM_DEVICE = auto()
    AZURE_REGION = auto()
    CINDER_VOLUME = auto()
    DOCKER_CONTAINER_GROUP = auto()
    KUBERNETES_CLUSTER = auto()
    AZURE_WEB_APP = auto()
    HOST = auto()
    AZURE_LOAD_BALANCER = auto()
    OPENSTACK_REGION = auto()
    AWS_LAMBDA_FUNCTION = auto()
    AZURE_APPLICATION_GATEWAY = auto()
    AZURE_VM_SCALE_SET = auto()
    AZURE_COSMOS_DB = auto()
    DYNAMO_DB_TABLE = auto()
    CUSTOM_DEVICE_GROUP = auto()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


def get_entities_tenantwide(cluster, tenant, entity_type, **kwargs):
    """Get all Entities of specified type in the tenant.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param entity_type - use EntityTypes enum\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n
    @kwargs fields - entity detail fields\n\n
    @return - List of all entities matching the selection.
    """
    # If entitySelector already present, don't overwrite
    if 'entitySelector' in kwargs:
        kwargs['entitySelector'] += f',type({entity_type})'
    else:
        kwargs['entitySelector'] = f'type({entity_type})'

    logger.info(f"Getting whole result set for entities in {tenant} tenant")
    response = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        api_version=2,
        item='entities',
        endpoint=rh.TenantAPIs.ENTITIES,
        **kwargs
    )
    return response.get('entities')


def get_entities_clusterwide(cluster, entity_type, aggregated=True, **kwargs):
    """Get all Entities of specified type in the cluster.
    \n
    @param cluster - Dynatrace Cluster (from variable set)\n
    @param entity_type - use EntityTypes enum\n
    @param aggregated - whether results should be split by tenant\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n
    @kwargs fields - entity detail fields\n\n
    @return - List of all entities matching the selection if not aggregated.
              Dictionary with tenants as keys if aggregated.
    """
    split_entities = {}
    all_entities = []

    logger.info("Getting whole result set for entities in cluster")
    for tenant in cluster['tenant']:
        tenant_entities = get_entities_tenantwide(
            cluster=cluster,
            tenant=tenant,
            entity_type=entity_type,
            **kwargs
        )
        all_entities.extend(tenant_entities)
        split_entities[tenant] = tenant_entities

    return all_entities if aggregated else split_entities


def get_entities_setwide(full_set, entity_type, aggregated=True, **kwargs):
    """Get all Entities of specified type in the full cluster set.
    \n
    @param full_set - Variable set (from user variables)\n
    @param entity_type - use EntityTypes enum\n
    @param aggregated - whether results should be split by cluster\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n
    @kwargs fields - entity detail fields\n\n
    @return - List of all entities matching the selection if not aggregated.
              Dictionary with clusters as keys if aggregated.
    """
    split_entities = {}
    all_entities = []

    logger.info("Getting whole result set for entities in all clusters")
    for cluster in full_set:
        cluster_entities = get_entities_clusterwide(
            cluster=full_set[cluster],
            entity_type=entity_type,
            **kwargs
        )

        all_entities.extend(cluster_entities)
        split_entities[cluster] = cluster_entities

    return all_entities if aggregated else split_entities


def get_entities_by_page(cluster, tenant, entity_type, **kwargs):
    """Get all Entities of specified type, page by page.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param entity_type - use EntityTypes enum\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n
    @kwargs fields - entity detail fields\n
    @kwargs pageSize - max. number of entities returned per call.\n\n
    @return - Generator object (page by page) of all entities that match.
    """
    # If entitySelector already present, don't overwrite
    if 'entitySelector' in kwargs:
        kwargs['entitySelector'] += f',type({entity_type})'
    else:
        kwargs['entitySelector'] = f'type({entity_type})'

    logger.info(f"Getting paged result set for entities in {tenant} tenant")
    response = rh.get_results_by_page(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.ENTITIES,
        api_version=2,
        item='entities',
        **kwargs
    )

    for entities in response:
        yield entities


def get_entity(cluster, tenant, entity_id, **kwargs):
    """Get the details of an entity specified by ID.
    You can use more than one ID if they're comma separated (id-1,id-2).\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param entity_id - ID of monitored Entity\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n
    @kwargs fields - entity detail fields\n
    @return - One entity for one ID. List of entities otherwise.
    """
    # If entitySelector already present, don't overwrite
    if 'entitySelector' in kwargs:
        kwargs['entitySelector'] += f',entityId({entity_id})'
    else:
        kwargs['entitySelector'] = f'entityId({entity_id})'

    logger.info(f"Getting entity details for ID(s) {entity_id}")
    response = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.ENTITIES,
        api_version=2,
        item='entities',
        **kwargs
    )

    if response.get('totalCount') == 1:
        return response.get('entities')[0]

    return response.get('entities')


def get_entity_count_tenantwide(cluster, tenant, entity_type, **kwargs):
    """Get the total number of entities of a given type in the tenant.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param entity_type - use EntityTypes enum for this\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n\n
    @return - number of entities.
    """
    if 'from' not in kwargs:
        kwargs['from'] = "now-24h"
    # pageSize is irrelevant, so make the response size minimal
    kwargs['pageSize'] = 1
    # fields are irrelevant, so make the response size minimal
    kwargs['fields'] = ""

    # If entitySelector already present, don't overwrite
    if 'entitySelector' in kwargs:
        kwargs['entitySelector'] += f',type({entity_type})'
    else:
        kwargs['entitySelector'] = f'type({entity_type})'

    logger.info(f"Getting entity count from {tenant} tenant")
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.ENTITIES,
        params=kwargs
    )

    return response.json().get('totalCount')


def get_entity_count_clusterwide(cluster, entity_type, **kwargs):
    """Get total number of entitites of a given type in the cluster.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param entity_type - use EntityTypes enum for this\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n\n
    @return - number of entities
    """
    count = 0
    logger.info("Getting entity count from cluster")
    for tenant in cluster['tenant']:
        count += get_entity_count_tenantwide(
            cluster=cluster,
            tenant=tenant,
            entity_type=entity_type,
            **kwargs
        )
    return count


def get_entity_count_setwide(full_set, entity_type, **kwargs):
    """Get total number of entities of a give type in the cluster set.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param entity_type - use EntityTypes enum for this\n
    @kwargs entitySelector - used to filter entities\n
    @kwargs from - timeframe start\n
    @kwargs to - timeframe end\n\n
    @return - number of entities
    """
    count = 0
    logger.info("Getting entity count from all clusters")
    for cluster in full_set:
        count += get_entity_count_clusterwide(
            cluster=full_set[cluster],
            entity_type=entity_type,
            **kwargs
        )
    return count


def add_tags(cluster, tenant, tag_list, **kwargs):
    """Add tags to entities.
    Must specify at least an Entity Type or ID in entitySelector.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param tag_list - list of tags as dictionaries with "key" and
                      optionally "value" attributes\n
    @kwargs entitySelector - must specify at least either type or entityId.
                             use EntityTypes enum for type.\n\n
    @throws TypeError - if tag_list is empty or not a list\n
    @throws ValueError - if neither entity_type nor entity_id are specified
    """
    # Sanity checking, error handling
    if not tag_list:
        try:
            raise TypeError("No tags provided")
        except TypeError:
            logger.exception("Error: No tags provided")
            raise
    if not isinstance(tag_list, list):
        try:
            raise TypeError("tags_list is not a list")
        except TypeError:
            logger.exception("Error: tags_list must be a list")
            raise
    if 'type' not in kwargs['entitySelector'] \
            and 'entityId' not in kwargs['entitySelector']:
        try:
            raise ValueError("entitySelector must have at least type or entityId")
        except ValueError:
            logger.exception("Error: entitySelector missing required values")
            raise

    logger.info("Adding tags to entities")
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.POST,
        endpoint=rh.TenantAPIs.TAGS,
        params=kwargs,
        json=dict(tags=tag_list)
    )

    return response


def delete_tag(cluster, tenant, tag_key, tag_value=None, **kwargs):
    """Delete a tag from entities.
    Must specify at least an Entity Type or ID in entitySelector.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param tag_key - the key of the tag(s) to be deleted\n
    @param tag_value - the value for the tag key to be deleted.
                       Use "all" to delete all values for the key.\n
    @kwargs entitySelector - must specify at least either type or entityId.
                             use EntityTypes enum for type.\n\n
    @throws TypeError - if tag_key is empty or missing\n
    @throws ValueError - if neither entity_type nor entity_id are specified
    """
    # Sanity checking, error handling
    if not tag_key:
        try:
            raise TypeError("No tag key provided")
        except TypeError:
            logger.exception("Error: Must provide a tag key")
            raise
    if 'type' not in kwargs['entitySelector'] \
            and 'entityId' not in kwargs['entitySelector']:
        try:
            raise ValueError("entitySelector must have at least type or entityId")
        except ValueError:
            logger.exception("Error: entitySelector missing required values")
            raise

    # Set params for tag key & value
    kwargs['key'] = tag_key
    if tag_value == "all":
        kwargs['deleteAllWithKey'] = True
        logger.info(f"Deleting all {tag_key} tags from entities")
    elif tag_value:
        kwargs['value'] = tag_value
        logger.info(f"Deleting {tag_key}:{tag_value} tags from entities")
    else:
        logger.info(f"Deleting {tag_key} tag from entities.")

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.DELETE,
        endpoint=rh.TenantAPIs.TAGS,
        params=kwargs
    )
    return response


def custom_device(cluster, tenant, json_data):
    """Creates or updates a custom device based on given JSON data.\n

    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @param json_data - device properties in JSON format. Valid properties are:\n
    ---------- str: customDeviceId (mandatory)\n
    ---------- str: displayName (mandatory)\n
    ---------- str: group\n
    ---------- list(str): ipAddress\n
    ---------- list(int): listenPorts\n
    ---------- str: type (mandatory)\n
    ---------- str: faviconUrl\n
    ---------- str: configUrl\n
    ---------- dict(str: str): properties\n
    ---------- list(str): dnsNames\n
    @throws ValueError - if mandatory properties missing from JSON data
    """
    # Sanity checking, error handling
    try:
        if not json_data.get('customDeviceId') or not json_data.get('displayName'):
            raise ValueError("JSON data is missing Device ID and/or Name.")
        # json_data.type can be NoneType when device already exists
        if not get_entity(cluster, tenant, json_data.get('customDeviceId')) \
                and not json_data.get('type'):
            raise ValueError("type must be in JSON data when creating a device")
    except ValueError:
        logger.exception("Error: Missing mandatory details.")
        raise

    logger.info("Creating/updating custom device.")
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.POST,
        json=json_data,
        endpoint=f'{rh.TenantAPIs.ENTITIES}/custom'
    )
    return response

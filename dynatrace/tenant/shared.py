"""Module for core entity operations"""

from enum import Enum, auto
from dynatrace.framework import request_handler as rh


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


def get_entities(cluster, tenant, entity_type, params=None):
    """Get all Entities of specified type. Use EntityTypes enum."""
    if not params:
        params = {}

    # If params already contains entitySelector, don't overwrite
    if params.get('entitySelector'):
        params['entitySelector'] += f'type("{entity_type}")'
    else:
        params['entitySelector'] = f'type("{entity_type}")'

    response = rh.v2_get_results_whole(
        cluster=cluster,
        tenant=tenant,
        item='entities',
        endpoint=rh.TenantAPIs.ENTITIES,
        params=params
    )
    return response.json().get('entities')


def get_entities_by_page(cluster, tenant, entity_type, params=None):
    """Get all Entities of a given type, page by page.
    Returns a generator, page by page.
    """
    if not params:
        params = {}

    # If params already contains entitySelector, don't overwrite
    if params.get('entitySelector'):
        params['entitySelector'] += f'type("{entity_type}")'
    else:
        params['entitySelector'] = f'type("{entity_type}")'

    response = rh.v2_get_results_by_page(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.ENTITIES,
        item='entities',
        params=params
    )

    for entity in response:
        yield entity


def get_entity(cluster, tenant, entity_id, params=None):
    """
    Get the details of an entity specified by ID.
    You can use more than one ID if it's quoted and comma separated ("id-1","id-2")
    """
    if not params:
        params = {}

    # If params already contains entitySelector, don't overwrite
    if params.get('entitySelector'):
        params['entitySelector'] += f'entityId({entity_id})'
    else:
        params['entitySelector'] = f'entityId({entity_id})'

    response = rh.v2_get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.ENTITIES,
        item='entities',
        params=params
    )

    if response.get('totalCount') == 1:
        return response.json().get('entities')[0]

    return response.json().get('entities')


def get_env_entity_count(cluster, tenant, entity_type, params=None):
    """
    Get total number of entities of a given type in an environment.
    Use EntityType enum.
    """
    if not params:
        params = {}

    if 'from' not in params:
        params['from'] = "now-24h"

    # If params already contains entitySelector, don't overwrite
    if params.get('entitySelector'):
        params['entitySelector'] += f'type("{entity_type}")'
    else:
        params['entitySelector'] = f'type("{entity_type}")'

    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=rh.TenantAPIs.ENTITIES,
                                params=params)
    env_layer_count = response.json().get('totalCount')
    return env_layer_count


def get_cluster_entity_count(cluster, entity_type, params=None):
    """
    Get total number of entitites of a given type for all environments
    in cluster. Use EntityType enum.
    """
    if not params:
        params = {}

    count = 0
    for tenant in cluster['tenant']:
        count += get_env_entity_count(
            cluster=cluster,
            tenant=tenant,
            entity_type=entity_type,
            params=params
        )
    return count


def get_set_entity_count(full_set, entity_type, params=None):
    """Get total count for all clusters definied in variable file"""
    if not params:
        params = {}

    count = 0
    for cluster in full_set.values():
        count += get_cluster_entity_count(
            cluster=cluster,
            entity_type=entity_type,
            params=params
        )
    return count


def add_tags(cluster, tenant, tag_list, entity_type=None, entity_id=None, params=None):
    """
    Add tags to entities. Must specify tag key. Must specify at least
    an Entity Type or ID.\n

    @param cluster - Dynatrace Cluster\n
    @param tenant - Dynatrace Tenant\n
    @param tag_list - list of tags as dictionaries with "key" and
                      optionally "value" attributes\n
    @param entity_type - use EntityTypes enum for this\n
    @param entity_id - ID of entity. You can specify several IDs, quoted and
                       separated by a comma ("id-1","id-2").\n
    @param params - other query string parameters compatible with this API.\n\n
    @throws TypeError - if tag_list is empty or not a list\n
    @throws ValueError - if neither entity_type nor entity_id are specified
    """
    if not params:
        params = {}

    # Sanity checking, error handling
    if not tag_list:
        raise TypeError("No tags provided")
    if not isinstance(tag_list, list):
        raise TypeError("tags_list is not a list")
    if not any([entity_type, entity_id]):
        raise ValueError("Must specifiy at least either entity_type or entity_id")

    # Params may already contain an entitySelector, we mustn't overwrite
    if entity_type:
        if params.get('entitySelector'):
            params['entitySelector'] += f'type("{entity_type}")'
        else:
            params['entitySelector'] = f'type("{entity_type}")'
    if entity_id:
        if params.get('entitySelector'):
            params['entitySelector'] += f'entityId({entity_id})'
        else:
            params['entitySelector'] = f'entityId({entity_id})'

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.POST,
        endpoint=rh.TenantAPIs.TAGS,
        params=params,
        json=dict(tags=tag_list)
    )

    return response


def delete_tag(cluster, tenant, tag_key, entity_type=None, entity_id=None,
               tag_value=None, params=None):
    """
    Delete tag from entities. Must specify at least an Entity Type or ID.\n

    @param cluster - Dynatrace Cluster\n
    @param tenant - Dynatrace Tenant\n
    @param tag_key - the key of the tag(s) to be deleted\n
    @param tag_value - the value for the tag key to be deleted.
                       Use "all" to delete all values for the key.\n
    @param entity_type - use EntityTypes enum for this\n
    @param entity_id - ID of entity. You can specify several IDs, quoted and
                       separated by a comma ("id-1","id-2").\n
    @param params - other query string parameters compatible with this API.\n\n
    @throws TypeError - if tag_key is empty or missing\n
    @throws ValueError - if neither entity_type nor entity_id are specified
    """
    if not params:
        params = {}

    # Sanity checking, error handling
    if not tag_key:
        raise TypeError("No tag key provided")
    if not any([entity_type, entity_id]):
        raise ValueError("Must specifiy at least either entity_type or entity_id")

    # Params may already contain an entitySelector, we mustn't overwrite
    if entity_type:
        if params.get('entitySelector'):
            params['entitySelector'] += f'type("{entity_type}")'
        else:
            params['entitySelector'] = f'type("{entity_type}")'
    if entity_id:
        if params.get('entitySelector'):
            params['entitySelector'] += f'entityId({entity_id})'
        else:
            params['entitySelector'] = f'entityId({entity_id})'

    # Set params for tag key & value
    params['key'] = tag_key
    if tag_value == "all":
        params['deleteAllWithKey'] = True
    elif tag_value:
        params['value'] = tag_value

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.DELETE,
        endpoint=rh.TenantAPIs.TAGS,
        params=params
    )
    return response

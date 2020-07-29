"""Shared topology operations for multiple layers from the Dynatrace API"""
from dynatrace.requests import request_handler as rh
# Layer Compatibility
# 1. Get all entities - application, host, process, process group, service
#   1a. Count all entities
# 2. Get specific entity - application, host process, process group, service
# 3. Update properties of entity - application, custom, host, process group, service

ENDPOINT = "entity/infrastructure/"


def check_valid_layer(layer, layer_dict):
    """Check if the operation is valid for the layer"""
    if layer is None or layer_dict is None:
        raise Exception('Provide layer and layer_dict!')
    if layer not in layer_dict:
        raise Exception(
            layer + " layer does not exist or is invalid for this use!")
    return


def get_env_layer_entities(cluster, tenant, layer, params=None):
    """Get all Entities of Specified Layer"""
    layer_dict = {
            'applications': 'applications',
            'hosts': "infrastructure/hosts",
            'processes': "infrastructure/processes",
            'process-groups': "infrastructure/process-groups",
            'services': "infrastructure/services"
    }
    check_valid_layer(layer, layer_dict)
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{rh.TenantAPIs.V1_TOPOLOGY}/{layer_dict[layer]}",
        params=params
    )
    return response.json()


def get_env_layer_entity(cluster, tenant, layer, entity, params=None):
    """Get Entity Information for Specified Layer"""
    layer_dict = {
            'applications': 'applications',
            'hosts': "infrastructure/hosts",
            'processes': "infrastructure/processes",
            'process-groups': "infrastructure/process-groups",
            'services': "infrastructure/services"
    }
    check_valid_layer(layer, layer_dict)
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{rh.TenantAPIs.V1_TOPOLOGY}/{layer_dict[layer]}/{entity}",
        params=params
    )
    return response.json()


def set_env_layer_properties(cluster, tenant, layer, entity, prop_json):
    """Update Properties of Entity"""
    layer_dict = {
            'applications': 'applications',
            'custom': "infrastructure/custom",
            'hosts': "infrastructure/hosts",
            'process-groups': "infrastructure/process-groups",
            'services': "infrastructure/services"
    }
    check_valid_layer(layer, layer_dict)
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        method=rh.HTTP.POST,
        endpoint=f"{rh.TenantAPIs.V1_TOPOLOGY}/{layer_dict[layer]}/{entity}",
        json=prop_json
    )
    return response.status_code


def get_env_layer_count(cluster, tenant, layer, params=None):
    """Get total hosts in an environment"""
    layer_dict = {
            'applications': 'applications',
            'hosts': "infrastructure/hosts",
            'processes': "infrastructure/processes",
            'process-groups': "infrastructure/process-groups",
            'services': "infrastructure/services"
    }

    if 'relativeTime' not in params.keys():
        params['relativeTime'] = "day"
    if 'includeDetails' not in params.keys():
        params['includeDetails'] = False

    check_valid_layer(layer, layer_dict)
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{rh.TenantAPIs.V1_TOPOLOGY}/{layer_dict[layer]}",
                                params=params)
    env_layer_count = len(response.json())
    return env_layer_count


def get_cluster_layer_count(cluster, layer, params=None):
    """Get total count for all environments in cluster"""
    cluster_layer_count = 0
    for env_key in cluster['tenant']:
        cluster_layer_count += get_env_layer_count(cluster=cluster,
                                                   tenant=env_key,
                                                   layer=layer,
                                                   params=params)
    return cluster_layer_count


def get_set_layer_count(full_set, layer, params=None):
    """Get total count for all clusters definied in variable file"""
    full_set_layer_count = 0
    for cluster in full_set.values():
        full_set_layer_count += get_cluster_layer_count(cluster,
                                                        layer,
                                                        params)
    return full_set_layer_count


def add_env_layer_tags(cluster, tenant, layer, entity, tag_list):
    layer_dict = {
            'applications': 'applications',
            'hosts': "infrastructure/hosts",
            'custom': "infrastructure/custom",
            'process-groups': "infrastructure/process-groups",
            'services': "infrastructure/services"
    }

    check_valid_layer(layer, layer_dict)
    if not tag_list:
        raise Exception("tag_list cannot be None type")
    tag_json = {
        'tags': tag_list
    }
    return set_env_layer_properties(cluster, tenant, layer, entity, tag_json)

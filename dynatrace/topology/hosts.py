"""Host operations from the Dynatrace API"""
import dynatrace.topology.shared as topology_shared
from dynatrace.requests import request_handler as rh


def get_hosts_tenantwide(cluster, tenant, params=None):
    """Get Information for all hosts in a tenant"""
    return topology_shared.get_env_layer_entities(cluster, tenant, 'hosts', params=params)


def get_host(cluster, tenant, entity, params=None):
    """Get Information on one host for in a tenant"""
    return topology_shared.get_env_layer_entity(cluster, tenant, 'hosts', entity, params=params)


def set_host_properties(cluster, tenant, entity, prop_json):
    """Update properties of host entity"""
    return topology_shared.set_env_layer_properties(cluster, tenant, 'hosts', entity, prop_json)


def get_host_count_tenantwide(cluster, tenant, params=None):
    """Get total count for all hosts in a tenant"""
    return topology_shared.get_env_layer_count(cluster, tenant, 'hosts', params=params)


def get_host_count_clusterwide(cluster, params=None):
    """Get total count for all hosts in cluster"""
    return topology_shared.get_cluster_layer_count(cluster, 'hosts', params=params)


def get_host_count_setwide(full_set, params=None):
    """Get total count of hosts for all clusters definied in variable file"""
    return topology_shared.get_set_layer_count(full_set, 'hosts', params=params)


def add_host_tags(cluster, tenant, entity, tag_list):
    """Add tags to host"""
    return topology_shared.add_env_layer_tags(cluster, tenant, 'hosts', entity, tag_list)


def delete_host_tag(cluster, tenant, entity, tag):
    """Remove single tag from host"""
    if tag is None:
        raise Exception("Tag cannot be None!")
    return rh.make_api_call(cluster=cluster,
                            tenant=tenant,
                            method=rh.HTTP.DELETE,
                            endpoint=f"{rh.TenantAPIs.V1_TOPOLOGY}/infrastructure/hosts/{entity}/tags/{tag}")


def get_host_units_tenantwide(cluster, tenant, params=None):
    consumed_host_units = 0
    host_list = get_hosts_tenantwide(cluster, tenant, params=params)
    for host in host_list:
        consumed_host_units = consumed_host_units + host['consumedHostUnits']
    return consumed_host_units


def get_oneagents_tenantwide(cluster, tenant, params=None):
    oneagents = []
    nextPageKey = 1

    while nextPageKey:
        if nextPageKey != 1:
            params['nextPageKey'] = nextPageKey

        response = rh.make_api_call(cluster=cluster,
                                    endpoint=rh.TenantAPIs.ONEAGENTS,
                                    tenant=tenant,
                                    params=params)

        oneagents.extend(response.json().get('hosts'))
        nextPageKey = response.json().get('nextPageKey')

    return oneagents

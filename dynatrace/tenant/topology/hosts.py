"""Module for host type entity operations"""

import dynatrace.tenant.topology.shared as entity_api
import dynatrace.requests.request_handler as rh


def get_hosts_tenantwide(cluster, tenant, params=None):
    """Get Information for all hosts in a tenant"""
    return entity_api.get_entities(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.HOST,
        params=params
    )


def get_host(cluster, tenant, entity, params=None):
    """Get Information for one host in a tenant"""
    return entity_api.get_entity(
        cluster=cluster,
        tenant=tenant,
        entity_id=entity,
        params=params
    )


def set_host_properties(cluster, tenant, entity, prop_json):
    """Update properties of host entity"""
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.TAGS,
        params={
            'entitySelector': f'entityId("{entity}")'
        },
        method=rh.HTTP.POST,
        json=prop_json
    )

    return response.json()


def get_host_count_tenantwide(cluster, tenant, params=None):
    """Get total count for all hosts in a tenant"""
    return entity_api.get_env_entity_count(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.HOST,
        params=params
    )


def get_host_count_clusterwide(cluster, params=None):
    """Get total count for all hosts in cluster"""
    return entity_api.get_cluster_entity_count(
        cluster=cluster,
        entity_type=entity_api.EntityTypes.HOST,
        params=params
    )


def get_host_count_setwide(full_set, params=None):
    """Get total count of hosts in cluster set"""
    return entity_api.get_set_entity_count(
        full_set=full_set,
        entity_type=entity_api.EntityTypes.HOST,
        params=params
    )


def add_host_tags(cluster, tenant, entity, tag_list):
    """Add tags to host"""
    return entity_api.add_tags(
        cluster=cluster,
        tenant=tenant,
        tag_list=tag_list,
        entity_id=entity
    )


def delete_host_tag(cluster, tenant, entity, tag):
    """Remove single tag from host"""
    return entity_api.delete_tag(
        cluster=cluster,
        tenant=tenant,
        tag_key=tag,
        entity_id=entity
    )


def get_host_units_tenantwide(cluster, tenant, params=None):
    """Get Host Units used by tenant

    Args:
        cluster (cluster dict): Currently selected cluster
        tenant (str): Tenant to operate in
        params (dict, optional): Available parameters to filter by. Defaults to None.

    Returns:
        float: total consumed units used in tenant
    """
    consumed_host_units = 0
    host_list = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f'{rh.TenantAPIs.V1_TOPOLOGY}/infrastructure/hosts',
        params=params
    ).json()
    for host in host_list:
        consumed_host_units += host['consumedHostUnits']
    return consumed_host_units


def get_oneagents_tenantwide(cluster, tenant, params=None):
    oneagents = []
    next_page_key = 1

    while next_page_key:
        if next_page_key != 1:
            params['nextPageKey'] = next_page_key

        response = rh.make_api_call(cluster=cluster,
                                    endpoint=rh.TenantAPIs.ONEAGENTS,
                                    tenant=tenant,
                                    params=params)

        oneagents.extend(response.json().get('hosts'))
        next_page_key = response.json().get('nextPageKey')

    return oneagents

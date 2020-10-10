"""Module for service type entity operations"""

import dynatrace.tenant.shared as entity_api
import dynatrace.framework.request_handler as rh


def get_services_tenantwide(cluster, tenant):
    """Get Information for all services in a tenant"""
    return entity_api.get_entities(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.SERVICE
    )


def get_service(cluster, tenant, entity):
    """Get Information for one service in a tenant"""
    return entity_api.get_entity(
        cluster=cluster,
        tenant=tenant,
        entity_id=entity
    )


def set_service_properties(cluster, tenant, entity, prop_json):
    """Update properties of service entity"""
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


def get_service_count_tenantwide(cluster, tenant, params=None):
    """Get total count for all services in a tenant"""
    return entity_api.get_env_entity_count(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.SERVICE,
        params=params
    )


def get_service_count_clusterwide(cluster, params=None):
    """Get total count for all services in cluster"""
    return entity_api.get_cluster_entity_count(
        cluster=cluster,
        entity_type=entity_api.EntityTypes.SERVICE,
        params=params
    )


def get_service_count_setwide(full_set, params=None):
    """Get total count of services in cluster set"""
    return entity_api.get_set_entity_count(
        full_set=full_set,
        entity_type=entity_api.EntityTypes.SERVICE,
        params=params
    )


def add_service_tags(cluster, tenant, entity, tag_list):
    """Add tags to a service"""
    return entity_api.add_tags(
        cluster=cluster,
        tenant=tenant,
        tag_list=tag_list,
        entity_id=entity
    )

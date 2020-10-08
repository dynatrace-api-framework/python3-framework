import dynatrace.tenant.topology.shared as entity_api
import dynatrace.requests.request_handler as rh


def get_applications_tenantwide(cluster, tenant):
    """Get Information for all applications in a tenant"""
    return entity_api.get_entities(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.APPLICATION
    )


def get_application(cluster, tenant, entity):
    """Get Information for one application in a tenant"""
    return entity_api.get_entity(
        cluster=cluster,
        tenant=tenant,
        entity_id=entity
    )


def set_application_properties(cluster, tenant, entity, prop_json):
    """Update properties of application entity"""
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


def get_application_count_tenantwide(cluster, tenant):
    """Get total count for all applications in a tenant"""
    params = {
        "from": "now-24h"
    }

    return entity_api.get_env_entity_count(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.APPLICATION,
        params=params
    )


def get_application_count_clusterwide(cluster):
    """Get total count for all applications in cluster"""
    return entity_api.get_cluster_entity_count(
        cluster=cluster,
        entity_type=entity_api.EntityTypes.APPLICATION
    )


def get_application_count_setwide(full_set):
    """Get total count of applications in cluster set"""
    return entity_api.get_set_entity_count(
        full_set=full_set,
        entity_type=entity_api.EntityTypes.APPLICATION
    )


def add_application_tags(cluster, tenant, entity, tag_list):
    """Add tags to application"""
    if tag_list is None:
        raise TypeError("tag_list cannot be None type")
    tag_json = {
        'tags': tag_list
    }
    return set_application_properties(cluster, tenant, entity, tag_json)


def get_application_baseline(cluster, tenant, entity):
    """Get baselines on one application for in a tenant"""
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{rh.TenantAPIs.V1_TOPOLOGY}/applications/{entity}/baseline"
    )
    return response.json()

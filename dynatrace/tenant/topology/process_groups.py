import dynatrace.tenant.topology.shared as entity_api
import dynatrace.requests.request_handler as rh


def get_process_groups_tenantwide(cluster, tenant):
    """Get Information for all process groups in a tenant"""
    return entity_api.get_entities(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.PROCESS_GROUP
    )


def get_process_group(cluster, tenant, entity):
    """Get Information for one process group in a tenant"""
    return entity_api.get_entity(
        cluster=cluster,
        tenant=tenant,
        entity_id=entity
    )


def set_process_group_properties(cluster, tenant, entity, prop_json):
    """Update properties of process group entity"""
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


def get_process_group_count_tenantwide(cluster, tenant, params=None):
    """Get total count for all process groups in a tenant"""
    return entity_api.get_env_entity_count(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.PROCESS_GROUP,
        params=params
    )


def get_process_group_count_clusterwide(cluster, params=None):
    """Get total count for all process groups in cluster"""
    return entity_api.get_cluster_entity_count(
        cluster=cluster,
        entity_type=entity_api.EntityTypes.PROCESS_GROUP,
        params=params
    )


def get_process_group_count_setwide(full_set, params=None):
    """Get total count of process groups in cluster set"""
    return entity_api.get_set_entity_count(
        full_set=full_set,
        entity_type=entity_api.EntityTypes.PROCESS_GROUP,
        params=params
    )


def add_process_group_tags(cluster, tenant, entity, tag_list):
    """Add tags to a process group"""
    return entity_api.add_tags(
        cluster=cluster,
        tenant=tenant,
        tag_list=tag_list,
        entity_id=entity
    )

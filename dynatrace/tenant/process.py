"""Module for process type entity operations"""

import dynatrace.tenant.shared as entity_api


def get_processes_tenantwide(cluster, tenant, params=None):
    """Get Information for all processes in a tenant"""
    return entity_api.get_entities(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.PROCESS_GROUP_INSTANCE,
        params=params
    )


def get_process(cluster, tenant, entity, params=None):
    """Get Information on one process for in a tenant"""
    return entity_api.get_entity(
        cluster=cluster,
        tenant=tenant,
        entity_id=entity,
        params=params
    )

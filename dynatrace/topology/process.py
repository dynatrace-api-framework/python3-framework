"""Process operations from the Dynatrace API"""
import dynatrace.topology.shared as topology_shared


def get_processes_tenantwide(cluster, tenant, params=None):
    """Get Information for all processes in a tenant"""
    return topology_shared.get_env_layer_entities(cluster, tenant, 'processes', params=params)


def get_process(cluster, tenant, entity, params=None):
    """Get Information on one process for in a tenant"""
    return topology_shared.get_env_layer_entity(cluster, tenant, 'processes', entity, params=params)

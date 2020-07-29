"""Service operations from the Dynatrace API"""
import dynatrace.tenant.topology.shared as topology_shared


def get_services_tenantwide(cluster, tenant):
    """Get Information for all services in a tenant"""
    return topology_shared.get_env_layer_entities(cluster, tenant, 'services')


def get_service(cluster, tenant, entity):
    """Get Information on one service for in a tenant"""
    return topology_shared.get_env_layer_entity(cluster, tenant, 'services', entity)


def set_service_properties(cluster, tenant, entity, prop_json):
    """Update properties of service entity"""
    return topology_shared.set_env_layer_properties(cluster, tenant, 'services', entity, prop_json)


def get_service_count_tenantwide(cluster, tenant, params=None):
    """Get total count for all services in a tenant"""
    return topology_shared.get_env_layer_count(cluster, tenant, 'services', params=params)


def get_service_count_clusterwide(cluster, params=None):
    """Get total count for all services in cluster"""
    return topology_shared.get_cluster_layer_count(cluster, 'services', params=params)


def get_service_count_setwide(full_set, params=None):
    """Get total count of services for all clusters definied in variable file"""
    return topology_shared.get_set_layer_count(full_set, 'services', params=params)


def add_service_tags(cluster, tenant, entity, tag_list):
    """Add tags to a service"""
    return topology_shared.add_env_layer_tags(cluster, tenant, 'services', entity, tag_list)

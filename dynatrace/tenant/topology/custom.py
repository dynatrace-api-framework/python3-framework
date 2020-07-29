import dynatrace.tenant.topology.shared as topology_shared


def set_custom_properties(cluster, tenant, entity, prop_json):
    """Update properties of process_group entity"""
    return topology_shared.set_env_layer_properties(cluster, tenant, 'custom', entity, prop_json)

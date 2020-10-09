"""Module for host group type entity operations"""
import dynatrace.tenant.topology.shared as entity_api

# TODO redo export function (break out to export function?)
# def export_host_groups_setwide(full_set):

#   get_host_groups_setwide(full_set)
#   with open('txt/HostGroups - ' + envName + '.txt', 'w') as outFile:
#     for groupName in hostGroups.values():
#       outFile.write(groupName+"\n")
#   print(envName + " writing to 'HostGroups - " + envName + ".txt'")


def get_host_groups_tenantwide(cluster, tenant):
    """Get all Host Groups in the Tenant

    Args:
        cluster (Cluster Dict): Dictionary containing all Cluster info
        tenant (str): String with the tenant name that is being selected

    Returns:
        Dict: List of Host Groups in the tenant
    """
    response = entity_api.get_entities(
        cluster=cluster,
        tenant=tenant,
        entity_type=entity_api.EntityTypes.HOST_GROUP,
        params={
            'from': 'now-24h'
        }
    )
    host_groups = {
        hg.get('entityId'): hg.get('displayName')
        for hg in response
    }
    return host_groups


def get_host_groups_clusterwide(cluster, tenant_split=False):
    """Get all Host Groups used in the Cluster

    Args:
        cluster (cluster dict): Current cluster to operate on
        tenant_split (bool): whether to split results by tenant or not

    Returns:
        dict: Dictionary of all Host Groups used in the Cluster.
              If split by tenant, keys are tenants, values are dicts of
              tenant's host groups.
    """
    host_groups = {}

    if tenant_split:
        for tenant in cluster['tenant']:
            host_groups[tenant] = get_host_groups_tenantwide(cluster, tenant)
    else:
        for tenant in cluster['tenant']:
            host_groups.update(
                get_host_groups_tenantwide(cluster, tenant)
            )

    return host_groups


def get_host_groups_setwide(full_set, tenant_split=False):
    """Get all Host Groups used in the Cluster Set

    Args:
        full_set (dict of cluster dict): Current cluster to operate on
        tenant_split (bool): whether to split results by tenant or not

    Returns:
        dict: Dictionary of all Host Groups used in the Cluster Set
              If split by tenant, keys are tenants, values are dicts of
              tenant's host groups.
    """
    host_groups = {}

    if tenant_split:
        for cluster in full_set.values():
            host_groups.update(get_host_groups_clusterwide(
                cluster=cluster,
                tenant_split=True))
    else:
        for cluster in full_set.values():
            host_groups.update(get_host_groups_clusterwide(cluster))

    return host_groups

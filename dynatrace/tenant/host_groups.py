"""Host Group Information for Tenant"""
from dynatrace.tenant.topology import hosts as topology_hosts

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
    params = {
        'relativeTime': 'day',
        'includeDetails': 'true'
    }
    response = topology_hosts.get_hosts_tenantwide(cluster,
                                                   tenant,
                                                   params=params)
    host_groups = {}
    for host in response:
        if host.get('hostGroup'):
            host_groups[host['hostGroup']['meId']] = host['hostGroup']['name']
    return host_groups


def get_host_groups_clusterwide(cluster):
    """Get all Host Groups used in the Cluster

    Args:
        cluster (cluster dict): Current cluster to operate on

    Returns:
        dict: Dictionary of all Host Groups used in the Cluster
    """
    # TODO add split_by_tenant optional variable
    host_groups_custerwide = {}
    for tenant in cluster['tenant']:
        host_groups_custerwide.update(
            get_host_groups_tenantwide(cluster, tenant)
        )
    return host_groups_custerwide


def get_host_groups_setwide(full_set):
    # TODO add split_by_tenant optional variable
    """Get all Host Groups used in the Cluster Set

    Args:
        full_set (dict of cluster dict): Current cluster to operate on

    Returns:
        dict: Dictionary of all Host Groups used in the Cluster Set
    """
    host_groups_setwide = {}
    for cluster in full_set.values():
        host_groups_setwide.update(get_host_groups_clusterwide(cluster))
    return host_groups_setwide

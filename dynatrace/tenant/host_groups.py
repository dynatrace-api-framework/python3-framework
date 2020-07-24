"""Host Group Information for Tenant"""
from dynatrace.topology import hosts as topology_hosts

# TODO redo export function (break out to export function?)
# def export_host_groups_setwide(full_set):

#   get_host_groups_setwide(full_set)
#   with open('txt/HostGroups - ' + envName + '.txt', 'w') as outFile:
#     for groupName in hostGroups.values():
#       outFile.write(groupName+"\n")
#   print(envName + " writing to 'HostGroups - " + envName + ".txt'")


def get_host_groups_tenantwide(cluster, tenant):
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
    # TODO add split_by_tenant optional variable
    host_groups_custerwide = {}
    for tenant in cluster['tenant']:
        host_groups_custerwide.update(
            get_host_groups_tenantwide(cluster, tenant)
        )
    return host_groups_custerwide


def get_host_groups_setwide(full_set):
    # TODO add split_by_tenant optional variable
    host_groups_setwide = {}
    for cluster in full_set.values():
        host_groups_setwide.update(get_host_groups_clusterwide(cluster))
    return host_groups_setwide

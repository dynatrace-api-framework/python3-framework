"""Module for OneAgent operations."""

import dynatrace.framework.request_handler as rh
from dynatrace.framework.request_handler import v2_get_results_whole


def get_host_units_tenantwide(cluster, tenant, **kwargs):
    """Get Host Units used by the tenant
    \n
    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @kwargs - dictionary of query parameters valid with the API.\n
    @returns - total number of host units consumed
    """
    host_units = 0

    host_list = rh.v2_get_results_whole(
        cluster=cluster,
        tenant=tenant,
        item='hosts',
        endpoint=rh.TenantAPIs.ONEAGENTS,
        **kwargs
    ).get('hosts')

    for host in host_list:
        host_units += host['hostInfo']['consumedHostUnits']

    return host_units


def get_host_units_clusterwide(cluster, aggregated=True, **kwargs):
    """Get Host Units used by the cluster.
    \n
    @param cluster - Dynatrace Cluster (from variable set)\n
    @param aggregated - return results aggregated or split  by tenant\n
    @kwargs - dictionary of query parameters valid with the API.\n
    @returns - total number of host units consumed or dict object
               with tenants as keys if not aggregated.
    """
    total_host_units = 0
    host_units = {}

    for tenant in cluster['tenant']:
        tenant_host_units = get_host_units_tenantwide(
            cluster=cluster,
            tenant=tenant,
            **kwargs
        )
        total_host_units += tenant_host_units
        host_units[tenant] = tenant_host_units

    return total_host_units if aggregated else host_units


def get_host_units_setwide(full_set, aggregated=True, **kwargs):
    """Get Host Units used by the full set of clusters.
    \n
    @param full_set - Variable Set\n
    @param aggregated - return results aggregated or split by cluster\n
    @kwargs - dictionary of query parameters valid with the API.\n
    @returns - total number of host units consumed or dict object
               with clusters as keys if not aggregated.
    """
    total_host_units = 0
    host_units = {}

    for cluster in full_set.values():
        cluster_host_units = get_host_units_clusterwide(
            cluster=cluster,
            **kwargs
        )
        total_host_units += cluster_host_units
        host_units[cluster] = cluster_host_units

    return total_host_units if aggregated else host_units


def get_oneagents_tenantwide(cluster, tenant, **kwargs):
    """Get OneAgent details for all hosts in the tenant.
    \n
    @param cluster - Dynatrace Cluster (from variable set)\n
    @param tenant - Dynatrace Tenant (from variable set)\n
    @kwargs - dictcionary of query parameters valid with the API\n

    @returns - list of OneAgents
    """
    return v2_get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=rh.TenantAPIs.ONEAGENTS,
        item='hosts',
        **kwargs
    ).get('hosts')

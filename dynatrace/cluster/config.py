"""Cluster Config Operations for Dynatrace Managed"""
import dynatrace.framework.request_handler as rh


def get_node_info(cluster):
    """Get Current Cluster Information

    Args:
        cluster (cluster dict): Currently selected cluster

    Returns:
        dict: cluster node info dictionary
    """
    response = rh.make_api_call(cluster=cluster,
                                endpoint=rh.ClusterAPIs.CLUSTER)
    return response.json()


def get_node_config(cluster):
    """Get current cluster config for each node

    Args:
        cluster (cluster dict): Currently selected cluster

    Returns:
        dict: current cluster configuration properties
    """
    response = rh.make_api_call(cluster=cluster,
                                endpoint=rh.ClusterAPIs.CONFIG)
    return response.json()


def set_node_config(cluster, json):
    """Set cluster config for each node

    Args:
        cluster (cluster dict): Currently selected cluster
        json (dict): Dict of all desired settings

    Returns:
        int: status code of pass/failed
    """
    response = rh.make_api_call(cluster=cluster,
                                endpoint=rh.ClusterAPIs.CONFIG,
                                method=rh.HTTP.POST,
                                json=json)
    return response.status_code

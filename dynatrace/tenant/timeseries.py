"""Timerseries Operations from Environment V1 API"""
from dynatrace.framework import request_handler as rh

ENDPOINT = "timeseries/"


def get_timeseries_list(cluster, tenant, params=None):
    """Get List of Timeseries Metics"""
    response = rh.make_api_call(cluster, tenant, ENDPOINT, params=params)
    return response.json()


def get_timeseries_metric(cluster, tenant, metric, params=None):
    """Get Timeseries Metric"""
    # Chose to do GET, but could also be done as POST. Don't think there are any advantages to post
    response = rh.make_api_call(cluster, tenant, ENDPOINT + metric, params=params)
    return response.json()


def create_custom_metric(cluster, tenant, metric, json, params=None):
    """Create a custome timeseries metric

    Args:
        cluster (cluster dict): Currently selected cluster
        tenant (str): tenant to pull metrics from
        metric (str): selected metric to store as
        json (dict): json payload required to created custom metric
        params (dict, optional): [description]. Defaults to None.

    Returns:
        int: response status code
    """
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{ENDPOINT}{metric}",
                                params=params,
                                method=rh.HTTP.PUT,
                                json=json)
    return response.status_code


def delete_custom_metic(cluster, tenant, metric):
    """[summary]

    Args:
        cluster (cluster dict): Currently selected cluster
        tenant (str): Tenant to operate in
        metric (str): custom metric to be deleted

    Returns:
        [type]: [description]
    """
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.DELETE,
                                endpoint=f"{ENDPOINT}{metric}")
    return response.status_code

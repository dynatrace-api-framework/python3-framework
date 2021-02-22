"""Timerseries Operations from Environment V1 API
Note: module contains only use cases not currently fulfilled via Metrics (V2) API
"""
from dynatrace.framework import request_handler as rh

ENDPOINT = rh.TenantAPIs.TIMESERIES


def get_metric_data_with_prediction(cluster, tenant, timeseries_id, **kwargs):
    """Get datapoints for a metric, including prediction.
    This returns a dictionary, where the timeseries ID is a key and the value is a list
    of datapoints (timestamp + data). Cannot use timeframe larger than 30 min.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set \n
    @param timeseries_id (str) - ID of the Timeseries to extract
    \n
    @returns dict - predicted datapoints of the timeseries
    """
    kwargs["includeData"] = True
    kwargs["predict"] = True
    if not (("startTimestamp" in kwargs and "endTimestamp" in kwargs)
            or "relativeTime" in kwargs):
        kwargs["relativeTime"] = "30mins"

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{timeseries_id}",
        params=kwargs
    ).json()

    return response.get("dataResult").get("dataPoints")

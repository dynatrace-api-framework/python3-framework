"""Module for interacting with the Metrics API"""
from dynatrace.framework import request_handler as rh

ENDPOINT = rh.TenantAPIs.METRICS


def get_metrics(cluster, tenant, params=None):
    """Gets the list of metrics and their details"""
    next_page_key = 1
    metrics = []

    while next_page_key:
        # Upon subsequent calls, clear all other params
        if next_page_key != 1:
            params = dict(nextPageKey=next_page_key)

        response = rh.make_api_call(cluster=cluster,
                                    tenant=tenant,
                                    endpoint=ENDPOINT,
                                    params=params)

        metrics.extend(response.json().get('metrics'))
        next_page_key = response.json().get('nextPageKey')

    return metrics

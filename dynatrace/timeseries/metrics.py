from dynatrace.requests import request_handler as rh

ENDPOINT = rh.TenantAPIs.METRICS


def get_metrics(cluster, tenant, params=None):
    """Gets the list of metrics and their details"""
    nextPageKey = 1
    metrics = []

    while nextPageKey:
        # Upon subsequent calls, clear all other params
        if nextPageKey != 1:
            params = dict(nextPageKey=nextPageKey)

        response = rh.make_api_call(cluster=cluster,
                                    tenant=tenant,
                                    endpoint=ENDPOINT,
                                    params=params)

        metrics.extend(response.json().get('metrics'))
        nextPageKey = response.json().get('nextPageKey')

    return metrics

from dynatrace.requests import request_handler as rh

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
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{ENDPOINT}{metric}",
                                params=params,
                                method=rh.HTTP.PUT,
                                json=json)
    return response.status_code


def delete_custom_metic(cluster, tenant, metric):
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.DELETE,
                                endpoint=f"{ENDPOINT}{metric}")
    return response.status_code

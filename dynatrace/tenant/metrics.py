"""Module for interacting with the Metrics API"""
from dynatrace.framework import request_handler as rh

ENDPOINT = str(rh.TenantAPIs.METRICS)


def get_metric_descriptor(cluster, tenant, **kwargs):
    """Get a list of metric descriptors and their details.
    Valid metricSelector must be provided in kwargs. List contains all default
    details or anything specified through 'fields' kwarg.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    \n
    @returns list - list of metric descriptors mathing the metricSelector
    """
    descriptors = rh.v2_get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        item='metrics',
        **kwargs
    ).get('metrics')

    return descriptors


def get_metric_count(cluster, tenant, **kwargs):
    """Get the number of metrics matching the metricSeletor
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    \n
    @returns int - Number of metrics matching the metricSelector
    """
    count = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        params=kwargs
    ).json().get('totalCount')

    return count


def get_metric_data(cluster, tenant, **kwargs):
    """Gets data points for given metrics.
    One or more metrics and aggregations can be specified using a metricSelector.
    The function grabs the datapoints for all entities matching entitySelector if
    this was specified. Results are indexed in a dictionary with the metric_id as
    key and the data as a list.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    \n
    @kwargs metricSelector (str) - mandatory. used to pass in ID of queried metri(s)
    \n
    @returns dict - metric data as dictionary with metric id as key
    \n
    @throws Exception - exception as thrown from downstream
    """
    nextPageKey = 1
    results = {}

    while nextPageKey:
        # Upon subsequent calls, clear all other params
        if nextPageKey != 1:
            kwargs = dict(nextPageKey=nextPageKey)

        try:
            response = rh.make_api_call(cluster=cluster,
                                        tenant=tenant,
                                        endpoint=f"{ENDPOINT}/query",
                                        params=kwargs)
        except Exception as err:
            if 'metric key that could not be resolved in the metric registry' in str(err):
                break
            else:
                raise Exception(err)
        else:
            for result in response.json().get('result'):
                metric = result.get('metricId')
                if results.get(metric):
                    results[metric].extend(result.get('data'))
                else:
                    results[metric] = result.get('data')

            nextPageKey = response.json().get('nextPageKey')

    return results

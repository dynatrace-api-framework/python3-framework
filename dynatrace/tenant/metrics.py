"""Module for interacting with the Metrics API"""
from dynatrace.framework import request_handler as rh
from dynatrace.framework.exceptions import InvalidAPIResponseException

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
    @kwargs metricSelector (str) - mandatory. used to pass in ID of queried metric(s)
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
        except InvalidAPIResponseException as err:
            if 'metric key that could not be resolved in the metric registry' in str(err):
                break
            else:
                raise err

        for result in response.json().get('result'):
            metric = result.get('metricId')
            if results.get(metric):
                results[metric].extend(result.get('data'))
            else:
                results[metric] = result.get('data')

        nextPageKey = response.json().get('nextPageKey')

    return results


def get_metric_dimension_count(cluster, tenant, metricSelector):
    """Function returns the sum total of dimensions defined for one or more metrics.
    Useful in DDU calculations for estimating the max number of DDUs that will be
    consumed.

    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    @param metricSelector (str) - mandatory. used to pass in ID of queried metric(s)
    \n
    @returns int - the sum total of dimensions across all matched metrics
    """
    details = get_metric_descriptor(
        cluster=cluster,
        tenant=tenant,
        metricSelector=metricSelector,
        fields='dimensionDefinitions',
        pageSize=5000
    )

    dimensions = sum(
        [len(detail.get('dimensionDefinitions'))
         for detail in details]
    ) if details else 0

    return dimensions


def get_metric_estimated_ddus(cluster, tenant, metricSelector):
    """Function returns the total maximum yearly DDUs that the metrics are allowed
    to consume. This is calculated by multiplying the total number of dimensions
    by 525.6 (yearly DDUs for 1 metric). This assumes the metric is collected every
    minute. Useful for understanding DDU budget requirements.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    @param metricSelector (str) - mandatory. used to pass in ID of queried metric(s)
    \n
    @returns (float) - total number of yearly DDUs
    """
    return get_metric_dimension_count(
        cluster=cluster,
        tenant=tenant,
        metricSelector=metricSelector
    ) * 525.6


# TODO: Refactor make_api_call (PAF-48)
# Payload data must be plain text, not serialised JSON like make_api_call require it.
# Before this functionality can be implemented we must refactor make_api_call to
# use any **kwargs that are valid for the requests module.
#
# def ingest_metrics(cluster, tenant, payload):
#     r = rh.make_api_call(
#         cluster=cluster,
#         tenant=tenant,
#         endpoint=f"{ENDPOINT}/ingest",
#         json=payload,
#         method=rh.HTTP.POST
#     )
#
#     return r

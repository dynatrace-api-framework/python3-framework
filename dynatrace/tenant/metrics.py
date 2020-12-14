"""Module for interacting with the Metrics API"""
from dynatrace.framework import request_handler as rh, logging
from dynatrace.framework.exceptions import InvalidAPIResponseException

ENDPOINT = str(rh.TenantAPIs.METRICS)
logger = logging.get_logger(__name__)


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
    logger.info("Getting metric descriptors")
    descriptors = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        api_version=2,
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
    logger.info("Getting the total metric count for the query.")
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
    next_page_key = 1
    results = {}

    logger.info("Getting metric datapoints")
    while next_page_key:
        # Upon subsequent calls, clear all other params
        if next_page_key != 1:
            kwargs = dict(nextPageKey=next_page_key)

        try:
            response = rh.make_api_call(cluster=cluster,
                                        tenant=tenant,
                                        endpoint=f"{ENDPOINT}/query",
                                        params=kwargs)
        except InvalidAPIResponseException as err:
            if 'metric key that could not be resolved in the metric registry' in str(err):
                logger.warn("Invalid metric ID encountered. Returning results so far.")
                break
            logger.exception("Error: Invalid API response")
            raise

        for result in response.json().get('result'):
            metric = result.get('metricId')
            if results.get(metric):
                results[metric].extend(result.get('data'))
            else:
                results[metric] = result.get('data')

        next_page_key = response.json().get('nextPageKey')

    return results


def get_metric_dimension_count(cluster, tenant, metric_selector):
    """Function returns the sum total of dimensions defined for one or more metrics.
    Useful in DDU calculations for estimating the max number of DDUs that will be
    consumed.

    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    @param metric_selector (str) - mandatory. used to pass in ID of queried metric(s)
    \n
    @returns int - the sum total of dimensions across all matched metrics
    """
    logger.info("Getting dimension count for metric(s)")
    details = get_metric_descriptor(
        cluster=cluster,
        tenant=tenant,
        metricSelector=metric_selector,
        fields='dimensionDefinitions',
        pageSize=5000
    )

    dimensions = sum(
        [len(detail.get('dimensionDefinitions'))
         for detail in details]
    ) if details else 0

    return dimensions


def get_metric_estimated_ddus(cluster, tenant, metric_selector):
    """Function returns the total maximum yearly DDUs that the metrics are allowed
    to consume. This is calculated by multiplying the total number of dimensions
    by 525.6 (yearly DDUs for 1 metric). This assumes the metric is collected every
    minute. Useful for understanding DDU budget requirements.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)
    @param metric_selector (str) - mandatory. used to pass in ID of queried metric(s)
    \n
    @returns (float) - total number of yearly DDUs
    """
    logger.info("Getting DDUs for metric(s)")
    return get_metric_dimension_count(
        cluster=cluster,
        tenant=tenant,
        metric_selector=metric_selector
    ) * 525.6


def ingest_metrics(cluster, tenant, payload):
    """Ingests metrics based on given payload.
    Payload must be formatted according to Dynatrace line-protocol for metric ingest.
    \n
    @param cluster (dict) - Dynatrace cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace tenant (as taken from variable set)\n
    @param payload (str) - payload for metric ingestion. must be formatted according to
                           Dynatrace line protocol.
    \n
    @returns (dict) - response to HTTP request
    """
    logger.info("Sending metrics to Dynatrace")
    return rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/ingest",
        data=payload,
        method=rh.HTTP.POST
    )

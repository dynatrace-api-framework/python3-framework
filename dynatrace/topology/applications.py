"""Application operations from the Dynatrace API"""
# Applications needs a seperate definition since the url is not the same (not /infrastructre/)
from dynatrace.requests import request_handler as rh

ENDPOINT = f"{rh.TenantAPIs.V1_TOPOLOGY}/applications"


def get_applications_tenantwide(cluster, tenant):
    """Get Information for all applications in a tenant"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=ENDPOINT)
    return response.json()


def get_application(cluster, tenant, entity):
    """Get Information on one application for in a tenant"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{ENDPOINT}/{entity}")
    return response.json()


def set_application_properties(cluster, tenant, entity, prop_json):
    """Update properties of application entity"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{ENDPOINT}/{entity}",
                                method=rh.HTTP.POST,
                                json=prop_json)
    return response.json()


def get_application_count_tenantwide(cluster, tenant):
    """Get total count for all applications in a tenant"""
    params = {
        "relativeTime": "day",
        "includeDetails": "false"
    }

    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=ENDPOINT,
                                params=params)
    env_app_count = len(response.json())
    return env_app_count


def get_application_count_clusterwide(cluster):
    """Get total count for all applications in cluster"""
    cluster_app_count = 0
    for env_key in cluster['tenant']:
        cluster_app_count = cluster_app_count \
                            + get_application_count_tenantwide(cluster,
                                                               env_key)
    return cluster_app_count


def get_application_count_setwide(full_set):
    full_set_app_count = 0
    for cluster_items in full_set.values():
        full_set_app_count = full_set_app_count \
                             + get_application_count_clusterwide(cluster_items)
    return full_set_app_count


def add_application_tags(cluster, tenant, entity, tag_list):
    """Add tags to application"""
    if tag_list is None:
        raise Exception("tag_list cannot be None type")
    tag_json = {
        'tags': tag_list
    }
    return set_application_properties(cluster, tenant, entity, tag_json)


def get_application_baseline(cluster, tenant, entity):
    """Get baselines on one application for in a tenant"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{ENDPOINT}/{entity}/baseline")
    return response.json()

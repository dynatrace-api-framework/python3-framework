"""Operations Interacting with Dynatrace Extensions"""
from dynatrace.requests import request_handler as rh

ENDPOINT = rh.TenantAPIs.EXTENSIONS


def get_all_extensions(cluster, tenant, params=None):
    """ Gets the list of all extensions available"""
    # TODO: Add pagination

    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=ENDPOINT,
                                params=params)
    return response.json().get('extensions')


def get_extension_details(cluster, tenant, extension_id):
    """ Get the details of a specific extension"""

    response = rh.make_api_call(cluster=cluster,
                                endpoint=f"{ENDPOINT}/{extension_id}",
                                tenant=tenant)
    return response.json()


def get_extension_states(cluster, tenant, extension_id, params=None):
    """ Gets all the deployment states of a specific extension"""
    # TODO: Add pagination
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{ENDPOINT}/{extension_id}/states",
                                params=params)

    return response.json().get('states')

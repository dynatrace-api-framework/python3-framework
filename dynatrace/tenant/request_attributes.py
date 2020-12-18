"""Module for Request Attributes Operations via Configuration API"""

import os
import json
from dynatrace.framework import request_handler as rh, logging

ENDPOINT = str(rh.TenantAPIs.REQUEST_ATTRIBUTES)
logger = logging.get_logger(__name__)


def get_all_request_attributes(cluster, tenant):
    """Get all request attributes within a tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set
    \n
    @returns list - list of Request Attributes from tenant
    """
    logger.info("Getting all request attributes in tenant %s", tenant)
    req_attrs = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT
    ).json().get("values")

    return req_attrs


def get_request_attribute_details(cluster, tenant, ra_id):
    """Get the full details of a request attribute in the tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_id (str) - ID of the request attribute to fetch
    \n
    @returns dict - Request Attribute details
    """
    logger.info(
        "Getting details for request attribute with id %s in tenant %s", ra_id, tenant
    )
    details = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{ra_id}"
    ).json()

    return details


def create_request_attribute(cluster, tenant, ra_json):
    """Creates a new request attribute from given JSON and adds it to the tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_json (dict) - details of the request attribute to be sent as JSON payload
    \n
    @returns Response - HTTP Response for the request
    """
    logger.info(
        "Adding a request attribute called %s in tenant %s", ra_json.get("name"), tenant
    )
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        method=rh.HTTP.POST,
        json=ra_json
    )

    return response


def update_request_attribute(cluster, tenant, ra_id, ra_json):
    """Updates an existing request attribute in the tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_json (dict) - details of the request attribute to be sent as JSON payload
    \n
    @returns Response - HTTP Response for the request
    """
    logger.info(
        "Updating request attribute with ID %s in tenant %s", ra_id, tenant
    )
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{ra_id}",
        method=rh.HTTP.PUT,
        json=ra_json
    )

    return response


def delete_request_attribute_by_id(cluster, tenant, ra_id):
    """Deletes an existing request attribute, referenced by ID.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_id (str) - ID of the request attribute to delete
    \n
    @returns Response - HTTP Response
    """
    logger.info(
        "Deleting request attribute with ID %s from tenant %s", ra_id, tenant
    )
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{ra_id}",
        method=rh.HTTP.DELETE
    )

    return response


def delete_request_attribute_by_name(cluster, tenant, ra_name):
    """Deletes an existing request attribute, referenced by name.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_name (str) - name of the request attribute to delete
    \n
    @returns Response - HTTP Response
    \n
    @throws RuntimeError - when no ID was found for the request attribute
    """
    ra_id = get_request_attribute_id(cluster, tenant, ra_name)

    if not ra_id:
        try:
            raise RuntimeError(
                f"Error: request attribute with name {ra_name} was not found"
            )
        except RuntimeError:
            logger.exception("Error: request attribute not found.", stack_info=True)
            raise

    return delete_request_attribute_by_id(cluster, tenant, ra_id)


def create_or_update_request_attribute(cluster, tenant, ra_json):
    """Either creates a new request attribute from the provided JSON or updates it if it
    already exists in the tenant. Either way, the request attribute will be in the
    tenant. It will check if there is an ID present in the JSON for the update.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_json (dict) - details of the request attribute to be sent as JSON payload
    \n
    @returns Response - HTTP Response to the request
    """
    ra_id = ra_json.get("id")

    if ra_id:
        return update_request_attribute(cluster, tenant, ra_id, ra_json)

    return create_request_attribute(cluster, tenant, ra_json)


def get_request_attribute_id(cluster, tenant, ra_name):
    """Gets the ID for a request attribute referenced by name.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param ra_name (str) - name of the Request Attribute
    \n
    @returns str - ID of the request attribute if found. None otherwise.
    """
    logger.info("Finding the ID for request attribute with name %s", ra_name)
    req_attrs = get_all_request_attributes(cluster, tenant)

    for req_attr in req_attrs:
        if req_attr.get("name") == ra_name:
            return req_attr.get("id")
    return None


def export_to_files(cluster, tenant, folder):
    """Export all the request attributes in the tenant to files.
    Each request attribute is written to a separate file in the folder provided.
    The folder must exist already.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param folder (str) - path to folder where to write the export files
    \n
    @throws RuntimeError - when the specified folder is not found
    """
    if not os.path.exists(folder):
        try:
            raise RuntimeError("Error: the given folder path does not exist")
        except RuntimeError:
            logger.exception("Error: folder path not found.", stack_info=True)
            raise

    if "/" in folder and not folder.endswith("/"):
        folder = f"{folder}/"
    if "\\" in folder and not folder.endswith("\\"):
        folder = f"{folder}\\"

    req_attrs = get_all_request_attributes(cluster, tenant)

    logger.info("Exporting request attributes. Writing files inside %s", folder)
    for req_attr in req_attrs:
        logger.debug("Exporting request attribute called %s", req_attr.get("name"))
        ra_data = get_request_attribute_details(cluster, tenant, req_attr.get("id"))
        with open(file=f"{folder}{req_attr.get('name')}.json", mode="w") as ra_file:
            json.dump(ra_data, ra_file, indent=4)

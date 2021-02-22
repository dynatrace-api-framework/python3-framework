"""Service Request Naming Rule Operations via the Configuration API"""

import os
import json
from dynatrace.framework import request_handler as rh

ENDPOINT = str(rh.TenantAPIs.REQUEST_NAMING)


def delete_naming_rule(cluster, tenant, rule_id):
    """Deletes an already existing request naming rule, referenced by its ID.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param rule_id (str) - ID of the request naming rule to delete
    \n
    @returns Response - HTTP Response to the request
    """
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{rule_id}",
        method=rh.HTTP.DELETE
    )

    return response


def update_naming_rule(cluster, tenant, rule_id, rule_json):
    """Updates an already existing request naming rule, referenced by its ID.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param rule_id (str) - ID of the request naming rule to update\n
    @param rule_json (dict) - new rule definition, to be sent as JSON payload
    \n
    @returns Response - HTTP Response to the request
    """
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{rule_id}",
        method=rh.HTTP.PUT,
        json=rule_json
    )

    return response


def create_naming_rule(cluster, tenant, rule_json):
    """Creates a new request naming rule.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param rule_json (dict) - new rule definition, to be sent as JSON payload
    \n
    @returns Response - HTTP Response to the request
    """
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        method=rh.HTTP.POST,
        json=rule_json
    )

    return response


def get_rule_details(cluster, tenant, rule_id):
    """Gets the definition of an already existing request naming rule, referenced
    by its ID.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param rule_id (str) - ID of the request naming rule to fetch
    \n
    @returns dict - the rule definition (details)
    """
    details = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{rule_id}",
        method=rh.HTTP.GET
    ).json()

    return details


def get_all_rules(cluster, tenant):
    """Gets a list of all request naming rules in the tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set
    \n
    @returns list - list of request naming rules
    """
    rules = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        method=rh.HTTP.GET
    ).json().get("values")

    return rules


def export_to_files(cluster, tenant, folder):
    """Exports request naming rules from the tenant to .json files.
    Each rule is written to its own file, in JSON format. The file is named after the
    rule.
    \n
    @param cluster (dict) - Dynatrace Cluster dictionary, as taken from variable set\n
    @param tenant (str) - Dynatrace Tenant name, as taken from variable set\n
    @param folder (str) - path to folder where to create the files.
    \n
    @throws RuntimeError - when the folder path does not exist.
    """
    if not os.path.exists(folder):
        raise RuntimeError("Error: export folder path does not exist")

    if "/" in folder and not folder.endswith("/"):
        folder += "/"
    if "\\" in folder and not folder.endswith("\\"):
        folder += "\\"

    rules = get_all_rules(cluster, tenant)

    for rule in rules:
        rule_details = get_rule_details(cluster, tenant, rule.get("id"))
        rule_name = rule.get("name")
        with open(file=f"{folder}{rule_name}.json", mode="w") as rule_file:
            json.dump(rule_details, rule_file, indent=4)

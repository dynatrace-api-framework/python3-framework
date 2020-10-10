# This script's function is too add Management Zones
# for an application based on application and environment if provided
"""Management Zone Operations for Environment"""
import copy
import json
from dynatrace.framework import request_handler as rh

ENDPOINT = rh.TenantAPIs.MANAGEMENT_ZONES


def generate_mz_payload(application, env_zone=None):
    """Create Payload for Management Zone based on Application and Environment"""
    with open('../templates/mz_template.json', 'r') as mz_template:
        mz_payload = json.load(mz_template)

    mz_payload['name'] = str(application)
    # The Template will have
    # Service Rules(0), Process Group Rules(1), Application Rules(2),
    # Browser Monitors(3), HTTP Monitor(4), External Monitors(5), Manually Tagged Services (6),
    # Manually Tagged Process Groups (7), Mobile Application (8), Custom Device Groups (9),
    # Service and Process Groups are different because they allow Key/Value Pairs

    # TODO Consolidate by checking if Key/Value Pair exists
    mz_payload['rules'][0]['conditions'][0]['comparisonInfo']['value']['value'] = str(
        application)
    mz_payload['rules'][1]['conditions'][0]['comparisonInfo']['value']['value'] = str(
        application)

    for rule_num in range(2, 10):
        mz_payload['rules'][rule_num]['conditions'][0]['comparisonInfo']['value']['key'] = \
            "APP: " + str(application)

    if env_zone:
        # If environment exists, rename MZ and add environment conditions
        mz_payload['name'] = str(application) + " - " + str(env_zone)

        # Service and Process Groups are different because they allow Key/Value Pairs
        condition_payload = copy.deepcopy(
            mz_payload['rules'][0]['conditions'][0])
        condition_payload['comparisonInfo']['value']['key'] = "ENV"
        condition_payload['comparisonInfo']['value']['value'] = str(env_zone)
        mz_payload['rules'][0]['conditions'].append(condition_payload)

        del condition_payload
        condition_payload = copy.deepcopy(
            mz_payload['rules'][1]['conditions'][0])
        condition_payload['comparisonInfo']['value']['key'] = "ENV"
        condition_payload['comparisonInfo']['value']['value'] = str(env_zone)
        mz_payload['rules'][1]['conditions'].append(condition_payload)
        # Application, Browser Monitors, HTTP Monitor, External Monitors (in that order)

        for rule_num in range(2, 10):
            del condition_payload
            condition_payload = copy.deepcopy(
                mz_payload['rules'][rule_num]['conditions'][0])
            condition_payload['comparisonInfo']['value']['key'] = "ENV: " + \
                str(env_zone)
            mz_payload['rules'][rule_num]['conditions'].append(
                condition_payload)

    return mz_payload


def add_management_zone(cluster, tenant, application, env_zone=None):
    """Add Management Zone based on Application and Environment"""
    mz_payload = generate_mz_payload(application, env_zone)

    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.POST,
                                endpoint=ENDPOINT,
                                json=mz_payload)
    if "id" in response.json():
        return (response.json())['id']
    return response.text


def change_management_zone(cluster, tenant, mz_id, application, env_zone=None):
    """Add Management Zone based on Application and Environment"""
    mz_payload = generate_mz_payload(application, env_zone)

    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.PUT,
                                endpoint=f"{ENDPOINT}/{mz_id}",
                                json=mz_payload)
    print(response.status_code)


def delete_management_zone_by_id(cluster, tenant, mz_id):
    """Delete Management Zone by Management Zone ID"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.DELETE,
                                endpoint=f"{ENDPOINT}/{mz_id}")
    print(response.status_code)


def delete_management_zone_by_name(cluster, tenant, mz_name):
    """Delete Management Zone by Management Zone Name"""
    # TODO This function
    return "TODO " + cluster + tenant + mz_name


def get_management_zone_list(cluster, tenant):
    """Get all Management Zones in Environment"""
    # TODO Cache Management Zone list for Env, and add a cleanup script to remove after run.
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=ENDPOINT)
    mz_list_raw = response.json()
    return mz_list_raw['values']


def get_management_zone_id(cluster, tenant, mz_name):
    """Get Management Zone ID of Management Zone Name"""
    mz_list = get_management_zone_list(cluster, tenant)

    for m_zone in mz_list:
        if m_zone['name'] == mz_name:
            return m_zone['id']
    return None

#!/bin/python3
"""Cluster Group Operations"""
import user_variables  # pylint: disable=import-error
from dynatrace.framework import request_handler as rh
from dynatrace.tenant import management_zones as mzh

MZ_USER_PERMISSONS = {
    "access_env": "VIEWER",
    "change_settings": "MANAGE_SETTINGS",
    "view_logs": "LOG_VIEWER",
    "view_senstive": "VIEW_SENSITIVE_REQUEST_DATA"
}


def generate_group_name(template, user_type, tenant, app_name):
    """Generate User Group according to template

    Args:
        template (str): template with replacable values for variables
        user_type (str): user permission type
        tenant (str): tenant for user_group to match to
        app_name (str): Application name

    Returns:
        [type]: [description]
    """
    # TODO Refactor for more replacements
    template = template.replace("{USER_TYPE}", user_type)
    template = template.replace("{TENANT}", tenant)
    template = template.replace("{APP_NAME}", app_name)
    template = template.lower()
    return template


def create_app_groups(cluster, app_name):
    """Create Dynatrace User Groups for Applications"""
    role_types = user_variables.USER_GROUPS['role_types']
    role_tenants = user_variables.USER_GROUPS['role_tenants']

    all_new_groups = {}
    for current_tenant in role_tenants:
        all_new_groups[current_tenant] = {}
        for current_type_key, current_type_value in role_types.items():
            group_id = generate_group_name(
                user_variables.USER_GROUP_TEMPLATE, current_type_value, current_tenant, app_name)
            current_group = {
                "isClusterAdminGroup": False,
                "name": group_id,
                "ldapGroupNames": [
                    group_id,
                ],
                "accessRight": {}
            }

            response = rh.make_api_call(
                cluster=cluster,
                endpoint=rh.ClusterAPIs.GROUPS,
                method=rh.HTTP.POST,
                json=current_group
            )
            all_new_groups[current_tenant][current_type_key] = (
                (response.json())['id'])
    return all_new_groups


def create_app_groups_setwide(app_name):
    """Create Dynatrace User Groups for Applications"""
    for cluster in user_variables.FULL_SET.values():
        if cluster['is_managed']:
            create_app_groups(cluster, app_name)


def delete_app_groups(cluster, app_name):
    """Delete Uesr Groups for Application

    Args:
        cluster (cluster dict): Currently selected cluster
        app_name (str): Application to remove all groups
    """
    role_types = user_variables.USER_GROUPS['role_types']
    role_tenants = user_variables.USER_GROUPS['role_tenants']

    for current_tenant in role_tenants:
        for current_type_value in role_types:
            group_id = generate_group_name(
                user_variables.USER_GROUP_TEMPLATE, current_type_value, current_tenant, app_name)
            group_id = ''.join(e for e in group_id if e.isalnum())
            rh.make_api_call(
                cluster=cluster,
                method=rh.HTTP.DELETE,
                endpoint=f"{rh.ClusterAPIs.GROUPS}/{group_id}"
            )


def delete_app_groups_setwide(app_name):
    """Create Dynatrace User Groups for Applications"""
    for cluster in user_variables.FULL_SET.values():
        if cluster['is_managed']:
            delete_app_groups(cluster, app_name)


def create_app_clusterwide(cluster, app_name, zones=None):
    """Create App User Groups and Management Zones"""
    # Create Standard App MZs
    mz_list = {}
    for tenant_key in cluster['tenant'].keys():
        mzh.add_management_zone(
            cluster,
            tenant_key,
            str.upper(app_name)
        )
        if tenant_key in zones:
            mz_list[tenant_key] = []
            for zone in zones[tenant_key]:
                mz_id = mzh.add_management_zone(
                    cluster,
                    tenant_key,
                    str.upper(app_name),
                    zone
                )
                if mz_id is not None:
                    mz_list[tenant_key].append(mz_id)

    # Create User Groups
    user_groups = create_app_groups(cluster, app_name)
    print(user_groups)

    # for tenant in user_variables.USER_GROUPS['role_tenants']:
    #   if "access_env" in user_groups [tenant]:
    #     add_mz_to_user

#!/bin/python3
"""Request Attributes Operations"""
import json
from dynatrace.framework import request_handler as rh

ENDPOINT = rh.TenantAPIs.REQUEST_ATTRIBUTES


def pull_to_files(cluster, tenant, ignore_disabled=True):
    """Pull files from an environment to local"""
    # API Calls needed: Pull RA, take the ID and pull the details of each RA
    all_ra_call = rh.make_api_call(cluster=cluster,
                                   tenant=tenant,
                                   endpoint=ENDPOINT)
    all_ra_json = all_ra_call.json()
    all_ra_json = all_ra_json['values']
    # print (json.dumps(all_ra_json, indent=2))
    ra_file_list = []
    for request_attribute in all_ra_json:
        single_ra_call = rh.make_api_call(cluster=cluster,
                                          tenant=tenant,
                                          endpoint=f"{ENDPOINT}/{request_attribute['id']}")
        if single_ra_call.status_code == 200:
            single_ra_json = single_ra_call.json()
            if single_ra_json['enabled'] and ignore_disabled:
                single_ra_json.pop("metadata")
                single_ra_json.pop("id")
                ra_file_name = "jsons/request_attributes/" + \
                    str(single_ra_json['name']) + ".json"
                with open(ra_file_name, 'w') as current_file:
                    json.dump(single_ra_json, current_file, indent=2)
                ra_file_list.append(ra_file_name)
        else:
            print(single_ra_call.status_code)
    return ra_file_list


def push_from_files(file_list, cluster, tenant):
    """Push Request Attributes in JSONs to a tenant"""

    # Checks for Existing RAs to update them put request rather than a post that would fail
    existing_ra_get = rh.make_api_call(cluster=cluster, tenant=tenant, endpoint=ENDPOINT)
    existing_ra_json = existing_ra_get.json()
    existing_ra_json = existing_ra_json['values']
    existing_ra_list = {}
    for existing_ra in existing_ra_json:
        existing_ra_list["jsons/request_attributes/" +
                         str(existing_ra['name']) + ".json"] = existing_ra['id']

    for file in file_list:
        with open(file, 'r') as ra_file:
            ra_json = json.load(ra_file)
            if file in existing_ra_list:
                single_ra_post = rh.make_api_call(
                    cluster=cluster,
                    tenant=tenant,
                    method=rh.HTTP.PUT,
                    endpoint=f"{ENDPOINT}/{existing_ra_list[file]}",
                    json=ra_json
                )
            else:
                single_ra_post = rh.make_api_call(
                    cluster=cluster,
                    tenant=tenant,
                    method=rh.HTTP.POST,
                    endpoint=ENDPOINT,
                    json=ra_json
                )
            if single_ra_post.status_code >= 400:
                # NOTE: what about the check response in req handler!?
                # That will throw an exception first, which this should except
                print("Error with " + file + ". Status Code: " +
                      str(single_ra_post.status_code))
            else:
                print("Success " + file + "   " + single_ra_post.text)

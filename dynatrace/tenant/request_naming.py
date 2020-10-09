#!/bin/python3
"""Global Service Request Naming Class"""

import os
import json
from dynatrace.framework import request_handler as rh

ENDPOINT = rh.TenantAPIs.REQUEST_NAMING


def pull_to_files(cluster, tenant, ignore_disabled=True):
    """Pull Service Naming Rules to Files"""
    all_rules_call = rh.make_api_call(cluster=cluster,
                                      tenant=tenant,
                                      endpoint=ENDPOINT)
    all_rules_list = all_rules_call.json()
    all_rules_list = all_rules_list['values']
    # print (json.dumps(all_rules_list, indent=2))

    rules_file_list = []
    rule_num = 0
    for naming_rule in all_rules_list:
        rule_call = rh.make_api_call(cluster=cluster,
                                     tenant=tenant,
                                     endpoint=f"{ENDPOINT}/{naming_rule['id']}")
        if rule_call.status_code == 200:
            rule_json = rule_call.json()
            if rule_json['enabled'] and ignore_disabled:
                rule_json.pop('metadata')
                rule_json.pop('id')
                rule_file_name = f"jsons/request_naming/{rule_num}.json"
                with open(rule_file_name, 'w') as current_file:
                    json.dump(rule_json, current_file, indent=2)
                rules_file_list.append(rule_file_name)
        else:
            print(rule_call.status_code)
        rule_num = rule_num + 1
    return rules_file_list


def generate_file_list():
    """Generate File List from files in JSON directory"""
    file_list = os.listdir("./jsons/request_naming/")
    for file_name in file_list:
        print(str.isdigit(file_name))
    # print(file_list.sort(key=lambda f: filter(str.isdigit, f)))

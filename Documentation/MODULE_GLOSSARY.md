# Function Glossary
*Explain all functions in one file to help find the ones you may need*
<br/>
<br/>

*\* Asterisk means optional argument*
## dynatrace.cluster
### cluster_config.py
- get_node_info(Cluster Dict: cluster)
  - Return: JSON Dict
  - Status: Ready for Use
  - Description: Get cluster node information, such as node id, Hardware Info, JVM info, URIs
- get_node_config(Cluster Dict: cluster)
  - Return: JSON Dict
  - Status: Ready for Use
  - Description: Get node configurations such as, WebUI enabled, Agent enabled, id, IP Addresses, datacenter 
- set_node_config(Cluster Dict: cluster, Dict: json)
  - Return: HTTP Status Code
  - Status: **UNTESTED**
  - Description: Set node configurations such as, WebUI enabled, Agent enabled, id, IP Addresses, datacenter

### ssl.py
Notes: 
Entity Type can only be "COLLECTOR" or "SERVER" (case sensitive). 
In addition, when pushing SSL certs via the API, it is HIGHLY RECOMMENDED to allow local logins (aka Non-SSO logins) during the change. Enable SSO-only after you can manually check the cluster to verify there are no issues with SSO.

- get_cert_details (Cluster Dict: cluster, String: entity_type, String: entity_id)
  - Return: Dict
  - Status: Ready for Use
  - Description: Get JSON of information about the current SSL certificate in use by a specific Server Node(For sure) or Cluster ActiveGate(I think?) 
- get_cert_install_status(Cluster Dict: cluster, String: entity_id)
  - Return: String
  - Status: **UNTESTED**
  - Description: Not sure fully of the usage. I think it is for getting the status of a certificate update.
- set_cert(Cluster Dict: cluster, String: entity_type, String: entity_id, Dict: ssl_json)
  - Return: Dict
  - Status: Ready to Use

### sso.py
Notes: Some of these API commands are not advertised in the Cluster Management API

- disable_sso (Cluster Dict: cluster)
  - Return: HTTP Status Code
  - State: Ready for Use
  - Description: Turns off SSO in the environment. Can be especially useful if SSO breaks and you need to login with a local account
- enable_sso (Cluster Dict: cluster, Boolean: disable_local*, Boolean: groups_enabled*, Boolean: is_openid*)
  - Return: HTTP Status Code
  - State: Ready for Use (Only tested with already linked SSO)
  - Description: Enables SSO that is already configured but disabled. By default, local login is still enabled, groups are not passed via SSO and uses SAML over OpenID.
- get_sso_status (Cluster Dict: cluster)
  - Return: Dict
  - State: Ready for Use
  - Description: Shows the current authentication settings related to SSO

### user_groups.py
- create_app_groups (String: app_name)<br />
    - Return: Nothing
    - Status: **LIMITED**
    - Description: Takes the application and creates user groups for an application set-wide.<br> This is currently only applying a single format:<br/> ({User_Prefix}\_{Role_Type}\_{Tenant}_{User_Suffix})<br/> User Prefix/Suffix and Role Type are set in the variable sets
    - Current Plans: 
      - Refactor to a function that is for a single cluster and one for the set
      - Ignore any SaaS environments in the set
      - Allow for user group definited to be templated, so that a user can plug in their own group format
      - Add Suffix logic
- delete_app_groups (String: app_name)<br />
  - Return: Nothing
  - Status: **LIMITED**
  - Description: Takes the application and removes user groups for an application set-wide.<br> This is currently only applying a single format:<br/> ({User_Prefix}\_{Role_Type}\_{Tenant}_{User_Suffix})<br/> User Prefix/Suffix and Role Type are set in the variable sets
  - Current Plans: 
    - Refactor to a function that is for a single cluster and one for the set
    - Ignore any SaaS environments in the set
    - Allow for user group definited to be templated, so that a user can plug in their own group format
    - Add Suffix Logic
- create_app_clusterwide (Cluster Dict: cluster, String: app_name, Dict of String List: zones*)
  - Return: Nothing
  - Status: **INCOMPLETE**
  - Description: Create all user groups, and management zones and assign the new user groups to have appropriate permissions of the new management zones created<br/>
  "zones" is an optional argument. it is a dict of string lists. The intention is that each key would be the same as the cluster tenant name, and the embedded list will contain all the customer environments/lifecycles that will need their own management zone. <br/> Management would be created in the format "{APP}" or "{APP} - {ENV}"
  - Current Plans:
    - Assign appropriate permissions to the user group from the new management zones
    - Creating user groups has same limitations as "[create_app_groups](#create_app_groups)"

### users.py
Module Notes: If SaaS is passed, by default it is ignored without error or notice. For notice, pass ignore_saas=False into the functions and it will raise an exception

- check_is_managed(Cluster Dict: cluster, Boolean: ignore_saas)
  - Return: If current cluster is Managed
  - Status: Ready for Use
  - Description: Internal function mostly to check if the cluster is Managed.
- get_users(Cluster Dict: cluster, Boolean: ignore_saas*)
  - Return: JSON of users data in cluster
  - Status: Ready for Use
  - Description: Get all users in cluster and details. 
- add_user(Cluster Dict: cluster, Dict: user_json, Boolean: ignore_saas*)
  - Return: 'OK'
  - Status: Ready for Use
  - Description: Add user to the cluster according to user_json Dict
- update_user(Cluster Dict: cluster, Dict: user_json, Boolean: ignore_saas*)
  - Return: 'OK'
  - Status: Ready for Use
  - Description: Update user information for the cluster according to user_json Dict
- get_user (Cluster Dict: cluster, String: user_id, Boolean: ignore_saas*)
  - Return: JSON
  - Status: Ready for Use
  - Description: Get information for a single user by giving the user id
- delete_user (Cluster Dict: cluster, String: user_id, Boolean: ignore_saas*)
  - Return: JSON
  - Status: Ready for Use
  - Description: Delete single user from the Managed Cluster
- add_user_bulk (Cluster Dict: cluster, Dict: user_json, Boolean: ignore_saas*)
  - Return: 'OK'
  - Status: Ready for Use
  - Description: Add multiple users to the cluster according to the user_json Dict

## dynatrace.requests

### request_hander.py
*Class Notes:<br/>
Cluster Dict is a single cluster defined in the FULL_SET set in user_variables and follows that structure<br/>
Endpoints should not start with a "/"<br/>
Params are Dict of parameters that are directly passed to the API, Key should match Dynatrace param name*

- check_response (Cluster Dict: cluster, String: endpoint, Dict: params\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: Checks if the response is within the HTTP 200-299 for a successful transaction. Otherwise raises an exception with the error <br/>
- check_managed (Cluster Dict: cluster, String: endpoint, Dict: params\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: Checks if the cluster instance provided is Managed or SaaS. <br/>
    - Current Plans: 
      - Allow ignore by default, so exception isn't raised and the function just carries on, skipping SaaS instances.
- cluster_get (Cluster Dict: cluster, String: endpoint, Dict: params\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: GET Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- cluster_post (Cluster Dict: cluster, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: POST Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- cluster_put (Cluster Dict: cluster, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: PUT Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- cluster_delete (Cluster Dict: cluster, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: DELETE Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- env_get (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: GET Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- env_post (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: POST Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- env_put (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: PUT Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- env_delete (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: DELETE Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- config_get (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: GET Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- config_post (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: POST Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- config_put (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Description: PUT Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
    - Current Plans: 
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function
- config_delete (Cluster Dict: cluster, String: tenant, String: endpoint, Dict: params\*, Dict: json\*)
    - Return: Response Object
    - Status: Ready for Use
    - Current Plans: 
    - Description: DELETE Request for Cluster API Operations, passing in the Cluster Dictionary, this will ensure that the cluster passed through is managed. <br/>
      - Allow specifications of what to return (e.g full response object, status code, json payload) with an option argument in function

## dynatrace.tenant

### host_groups.py

- get_host_groups_tenantwide(Cluster Dict: cluster, String: tenant)
  - Return: Dict
  - Status: Ready for Use
  - Description: Get all Host Groups in a tenant. Dict uses HostGroup ID for the Key
- get_host_groups_tenantwide(Cluster Dict: cluster, String: tenant)
- get_host_groups_clusterwide (Cluster Dict: cluster)
  - Return: Dict
  - Status: Ready for Use
  - Description: Get all Host Groups in a Cluster. Dict uses HostGroup ID for the Key
  - Current Plan:
    - Add split_by_tenant optional variable to return all host groups in nested Dicts by tenant
- get_host_groups_setwide (Dict of Cluster Dict: setwide)
  - Return: Dict
  - Status: Ready for Use
  - Description: Get all Host Groups in the full_set of Clusters. Dict uses HostGroup ID for the Key
  - Current Plan:
    - Add split_by_tenant optional variable to return all host groups in nested Dicts by cluster and then again by tenant

## dynatrace.timeseries

### timeseries.py
Note: Currently V1 only

- get_timeseries_list (Cluster Dict: cluster, String: tenant, Dict: params\*)
  - Return: Dict
  - Status: Ready for Use
  - Description: Get list of Timeseries Metric Available
- get_timeseries_list (Cluster Dict: cluster, String: tenant, String metric, Dict: params\*)
  - Return: List/Dict (Varies based on Metric)
  - Status: Ready for Use
  - Description: Get individual timeseries metric 
- create_custom_metric (Cluster Dict: cluster, String: tenant, String metric, Dict: json, Dict: params\*)
  - Return: HTTP Status Code
  - Status: **Untested**
  - Description: Create custom metric
- delete_custom_metric (Cluster Dict: cluster, String: tenant, String metric)
  - Return: HTTP Status Code
  - Status: **Untested**
  - Description: Delete custom metric using metric ID

## dynatrace.topology

### applications.py

- get_applications_tenantwide (Cluster Dict: cluster, String: Tenant)
  - Return: Dict
  - Status: Ready for Use
  - Description: Returns JSON payload for the list of applications
- get_application (Cluster Dict: cluster, String: tenant, String: entity)
  - Return: Dict
  - Status: Ready for Use
  - Description: Returns a specific application JSON payload referred by its Entity ID
- set_application_properties(Cluster Dict: cluster, String: tenant, String: entity, Dict: prop_json)
  - Return: Dict
  - Status: Ready for Use
  - Description: Update Properties of the Application (at the moment the API only allows adding manual tags)
- get_application_count_tenantwide (Cluster Dict: cluster, String: Tenant)
  - Return: Int
  - Status: Ready for Use
  - Description: Get the number of Applications defined in the tenant
- get_application_count_clusterwide (Cluster Dict: cluster)
  - Return: Int
  - Status: Ready for Use
  - Description: Get the number of Applications defined in the cluster
- get_application_count_setwide (Dict of Cluster Dict: setwide)
  - Return: Int
  - Status: Ready for Use
  - Description: Get the number of Applications defined all the clusters/instances in the set
- get_application_baseline(cluster, tenant, entity)
  - Return: Dict
  - Status: **UNTESTED**
  - Description: Returns baseline information about the application requested

### custom.py

- set_custom_properties (Cluster Dict: cluster. String tenant, String: Entity, Dict: prop_json)
  - Return: Dict
  - Status: **UNTESTED**
  - Description: Create/Update custom device.

### hosts.py
- get_hosts_tenantwide (Cluster Dict: cluster, String: Tenant, Dict: params\*)
  - Return: Dict
  - Status: Ready for Use
  - Description: Returns JSON payload for the list of hosts
- get_hosts_tenantwide (Cluster Dict: cluster, String: Tenant, String: Entity, Dict: params\*)
  - Return: Dict
  - Status: Ready for Use
  - Description: Returns JSON payload for a single host
- set_host_properties(Cluster Dict: cluster, String: tenant, String: entity, Dict: prop_json)
  - Return: Dict
  - Status: Ready for Use
  - Description: Update Properties of the host (at the moment the API only allows adding manual tags)
- get_host_count_clusterwide (Cluster Dict: cluster)
  - Return: Int
  - Status: Ready for Use
  - Description: Get the number of hosts defined in the cluster
- get_host_count_setwide (Dict of Cluster Dict: setwide)
  - Return: Int
  - Status: Ready for Use
  - Description: Get the number of hosts defined all the clusters/instances in the set
- add_host_tags (Cluster Dict: cluster, String: tenant, String: entity, List: tag_list)
  - Return: HTTP Status Code
  - Status: Ready for Use
  - Description: Add tags to host
- get_host_units_tenantwide(Cluster Dict: cluster, String: tenant, List: params\*):
  - Return: Number
  - Status: Ready for Use
  - Description: Tally host units consumed by tenant (can be filtered down with params)

### process_groups.py
TODO - refer to above topology explanations for now
### process.py
TODO - refer to above topology explanations for now
### services.py
TODO - refer to above topology explanations for now

### shared.py
NOTE: This is unifying shared operations of multiple layers of the topology. It is advised that you do not use this module and use the other topology functions built on top of this.



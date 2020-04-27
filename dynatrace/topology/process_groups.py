"""Process Group operations from the Dynatrace API"""
import dynatrace.topology.shared as topology_shared
from dynatrace.requests import request_handler as rh

def get_process_groups_tenantwide(cluster, tenant):
  """Get Information for all process-groups in a tenant"""
  return topology_shared.get_env_layer_entities(cluster, tenant, 'process-groups')

def get_process_group(cluster, tenant, entity):
  """Get Information on one process-group for in a tenant"""
  return topology_shared.get_env_layer_entity(cluster, tenant,'process-groups', entity)

def set_process_group_properties(cluster, tenant, entity, prop_json):
  """Update properties of process-group entity"""
  return topology_shared.set_env_layer_properties(cluster, tenant, 'process-groups', entity, prop_json)

def get_process_group_count_tenantwide(cluster, tenant, params=None):
  """Get total count for all process-groups in a tenant"""
  return topology_shared.get_env_layer_count(cluster, tenant, 'process-groups', params=params)

def get_process_group_count_clusterwide(cluster, params=None):
  """Get total count for all process-groups in cluster"""
  return topology_shared.get_cluster_layer_count(cluster, 'process-groups', params=params)

def get_process_group_count_setwide(full_set, params=None):
  """Get total count of process-groups for all clusters defined in variable file"""
  return topology_shared.get_set_layer_count(full_set, 'process-groups', params=params)

def add_process_group_tags (cluster, tenant, entity, tag_list):
  """Add tags to a process group"""
  return topology_shared.add_env_layer_tags (cluster, tenant, 'process-groups', entity, tag_list)
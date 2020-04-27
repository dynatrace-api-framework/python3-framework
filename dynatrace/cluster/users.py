"""User Operations in Cluster Mangement"""
import dynatrace.requests.request_handler as rh

# TODO add check for is_managed

def check_is_managed(cluster, ignore_saas):
  """Checks if the cluster is Managed"""
  if not cluster['is_managed'] and not ignore_saas:
    raise Exception ('Cannot run operation on SaaS instances!')
  return cluster['is_managed']

def get_users(cluster, ignore_saas=True):
  """Get the list of Users on the Cluster"""
  check_is_managed(cluster, ignore_saas)
  response = rh.cluster_get(cluster, "users")
  return response.json()

def add_user(cluster, user_json, ignore_saas=True):
  """Add User to Cluster"""
  check_is_managed(cluster, ignore_saas)
  rh.cluster_post(cluster, "/users", json=user_json)
  return 'OK'

def update_user(cluster, user_json, ignore_saas=True):
  """Update User to Cluster"""
  check_is_managed(cluster, ignore_saas)
  rh.cluster_put(cluster, "/users", json=user_json)
  return 'OK'

def get_user(cluster, user_id, ignore_saas=True):
  """Get Details for a Single User"""
  check_is_managed(cluster, ignore_saas)
  response = rh.cluster_get(cluster, "users/" + user_id)
  return response.json()

def delete_user(cluster, user_id, ignore_saas=True):
  """Delete a Single User"""
  check_is_managed(cluster, ignore_saas)
  response = rh.cluster_delete(cluster, "users/" + user_id)
  return response.json()

def get_user_count(cluster, ignore_saas=True):
  """Return the number of, users in a cluster"""
  check_is_managed(cluster, ignore_saas)
  return len(get_users(cluster))

def add_user_bulk(cluster, user_json, ignore_saas=True):
  """Add Multiple Users"""
  check_is_managed(cluster, ignore_saas)
  rh.cluster_put(cluster, "/users/bulk", json=user_json)
  return 'OK'

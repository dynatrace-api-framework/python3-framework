import dynatrace.requests.request_handler as rh

def get_node_info(cluster):
  response = rh.cluster_get(cluster,"cluster")
  return response.json()

def get_node_config(cluster):
  response = rh.cluster_get(cluster,"cluster/configuration")
  return response.json()

def set_node_config(cluster, json):
  response = rh.cluster_post(cluster,"cluster/configuration", json=json)
  return response.status_code
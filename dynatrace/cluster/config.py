import dynatrace.requests.request_handler as rh


def get_node_info(cluster):
    response = rh.make_api_call(cluster=cluster,
                                endpoint=rh.ClusterAPIs.CLUSTER)
    return response.json()


def get_node_config(cluster):
    response = rh.make_api_call(cluster=cluster,
                                endpoint=rh.ClusterAPIs.CONFIG)
    return response.json()


def set_node_config(cluster, json):
    response = rh.make_api_call(cluster=cluster,
                                endpoint=rh.ClusterAPIs.CONFIG,
                                method=rh.HTTP.POST,
                                json=json)
    return response.status_code

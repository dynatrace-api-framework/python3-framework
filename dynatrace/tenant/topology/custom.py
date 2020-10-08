import dynatrace.requests.request_handler as rh


def set_custom_properties(cluster, tenant, entity, prop_json):
    """Creates or updates properties of custom device entity"""
    if not prop_json.get('customDeviceId'):
        prop_json['customDeviceId'] = entity
        
    return rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f'{rh.TenantAPIs.ENTITIES}/custom',
        method=rh.HTTP.POST,
        json=prop_json
    )

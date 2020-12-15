"""Operations Interacting with Dynatrace Extensions API"""
from dynatrace.framework import request_handler as rh, logging
from dynatrace.tenant import metrics

ENDPOINT = rh.TenantAPIs.EXTENSIONS
logger = logging.get_logger(__name__)


def get_all_extensions(cluster, tenant, page_size=200):
    """Gets a list of all extensions available on the tenant.
    List is returned whole regardless of page size; page size can be used to control the
    number of API calls.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param page_size (int) - page size between 1 and 500 (default 200)
    \n
    @returns list - list of extensions
    """
    logger.info("Getting all extensions in %s tenant", tenant)
    extension_list = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        api_version=2,
        pageSize=page_size,
        item="extensions"
    ).get('extensions')

    return extension_list


def get_extension_details(cluster, tenant, extension_id):
    """Get the details of a specific extension.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to get the details for
    \n
    @returns (dict) - JSON response containing extension details
    """
    logger.info("Getting extension details for %s", extension_id)
    details = rh.make_api_call(
        cluster=cluster,
        endpoint=f"{ENDPOINT}/{extension_id}",
        tenant=tenant
    ).json()

    return details


def get_extension_metrics(cluster, tenant, extension_id):
    """Gets a list of metric IDs that are collected by the extension.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension
    \n
    @returns list - list of metric IDs
    """
    logger.info("Getting metrics collected by extension %s", extension_id)
    metric_group = get_extension_details(cluster, tenant, extension_id).get('metricGroup')
    ext_metrics = metrics.get_metric_descriptor(
        cluster=cluster,
        tenant=tenant,
        metricSelector=f"ext:{metric_group}.*"
    )

    return list(m.get('metricId') for m in ext_metrics)


def get_extension_global_config(cluster, tenant, extension_id):
    """Gets the global configuration for a given extension.
    Does not apply to ActiveGate extensions.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to get the config for
    \n
    @returns dict - global configuration
    """
    logger.info("Getting global configuration for extension %s", extension_id)
    config = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{extension_id}/global"
    ).json()

    return config


def get_extension_instance_config(cluster, tenant, extension_id, instance_id):
    """Gets the configuration for an instance of an extension.
    For remote extensions this is an endpoint config, otherwise a host config.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to get the config for\n
    @param instance_id (str) - ID of extension instance to get config for
    \n
    @returns dict - instance configuration
    """
    logger.info(
        "Getting configuration for instance %s on extension %s", instance_id, extension_id
    )
    config = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{extension_id}/instances/{instance_id}"
    ).json()

    return config


def get_extension_states(cluster, tenant, extension_id):
    """Gets all the deployment states (instances) of a specific extension.
    For remote extensions these are endpoints, for other extensions these are
    processes/hosts. States are independent of global/instance configuration.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to get the states for
    \n
    @returns list - states/instances of this extension
    """
    logger.info("Getting states for extension %s", extension_id)
    states = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{extension_id}/states",
        api_version=2,
        item="states"
    ).get('states')

    return states


def get_extension_instances(cluster, tenant, extension_id):
    """Gets all the configuration instances of a specific extension.
    An instance is an endpoint for a remote extension, otherwise a host.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to get the states for
    \n
    @returns list - configuration instances for this extension
    """
    logger.info("Getting instances for extension %s", extension_id)
    instances = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{extension_id}/instances",
        api_version=2,
        item="configurationsList"
    ).get('configurationsList')

    return instances


def enable_global_config(cluster, tenant, extension_id):
    """Enables the global configuration for an extension.
    Not applicable to remote extensions.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to enable
    \n
    @returns dict - HTTP response for the request
    """
    config = get_extension_global_config(cluster, tenant, extension_id)

    config['enabled'] = True
    logger.info("Enabling global config for extension %s", extension_id)
    response = update_global_config(cluster, tenant, extension_id, config)

    return response


def disable_global_config(cluster, tenant, extension_id):
    """Disables the global configuration for an extension.
    Not applicable to remote extensions.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to disable
    \n
    @returns dict - HTTP response for the request
    """
    config = get_extension_global_config(cluster, tenant, extension_id)

    config['enabled'] = False
    logger.info("Disabling global config for extension %s", extension_id)
    response = update_global_config(cluster, tenant, extension_id, config)

    return response


def update_global_config(cluster, tenant, extension_id, config):
    """Updates the global configuration for an extension.
    Not applicable to remote extensions.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to update\n
    @param config (dict) - new configuration as JSON dictionary
    \n
    @returns dict - HTTP response to request
    """
    logger.info("Updating global config for extension %s", extension_id)
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{extension_id}/global",
        method=rh.HTTP.PUT,
        json=config
    )

    return response


def enable_instance_config(cluster, tenant, extension_id, instance_id):
    """Enables the configuration for an instance of an extension.
    Instance is endpoint for a remote extension, otherwise a host.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to enable\n
    @param instance_id (str) - ID of extension instance to enable
    \n
    @returns dict - HTTP response to request
    """
    config = get_extension_instance_config(
        cluster, tenant, extension_id, instance_id
    )

    config['enabled'] = True

    # API BUG: For remote extensions useGlobal is null, but API call doesn't support it
    if config.get('useGlobal') is None:
        config['useGlobal'] = False
    # API BUG: For remote extensions the extension ID in the config is the instance id
    #          this needs to be set back to the extension ID otherwise fails.
    if 'activeGate' in config:
        config['extensionId'] = extension_id

    logger.info("Enabling config for instance %s of %s", instance_id, extension_id)
    response = update_instance_config(
        cluster, tenant, extension_id, instance_id, config
    )

    return response


def disable_instance_config(cluster, tenant, extension_id, instance_id):
    """Disables the configuration for an instance of an extension.
    Instance is endpoint for a remote extension, otherwise a host.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to enable\n
    @param instance_id (str) - ID of extension instance to disable
    \n
    @returns dict - HTTP response to request
    """
    config = get_extension_instance_config(
        cluster, tenant, extension_id, instance_id
    )

    config['enabled'] = False

    # API BUG: For remote extensions useGlobal is null, but API call doesn't support it
    if config.get('useGlobal') is None:
        config['useGlobal'] = False
    # API BUG: For remote extensions the extension ID in the config is the instance id
    #          this needs to be set back to the extension ID otherwise fails.
    if 'activeGate' in config:
        config['extensionId'] = extension_id

    logger.info("Disabling config for instance %s of %s", instance_id, extension_id)
    response = update_instance_config(
        cluster, tenant, extension_id, instance_id, config
    )

    return response


def update_instance_config(cluster, tenant, extension_id, instance_id, config):
    """Updates the configuration for an instance of an extension.
    Instance is endpoint for a remote extension, otherwise a host.
    \n
    @param cluster (dict) - Cluster dictionary (as taken from variable set)\n
    @param tenant (str) - Tenant name (as taken from variable set)\n
    @param extension_id (str) - ID of extension to update\n
    @param instance_id (str) - ID of extension instance to update
    @param config (dict) - new configuration as JSON dictionary
    \n
    @returns dict - HTTP response to request
    """
    logger.info("Updating config for instance %s of %s", instance_id, extension_id)
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{extension_id}/instances/{instance_id}",
        method=rh.HTTP.PUT,
        json=config
    )

    return response

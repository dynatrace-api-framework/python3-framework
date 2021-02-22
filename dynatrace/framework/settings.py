"""Module for retreiving settings safely"""
import json
import yaml

__IMPORTED_SETTINGS__ = {}

try:
    import user_variables  # pylint: disable=import-error
    for attr in dir(user_variables):
        if not str.startswith(attr, "__"):
            __IMPORTED_SETTINGS__[attr] = getattr(user_variables, attr)
except ImportError:
    pass

DefaultSettings = {
    "LOG_LEVEL": "ERROR",
    "LOG_DIR": "logs/",
    "LOG_OUTPUT": [
        "CONSOLE",
    ],
    "LOG_ENABLED": True,

    # ROLE TYPE KEYS
    # access_env
    # change_settings
    # install_agent
    # view_logs
    # view_senstive
    # change_sensitive

    'USER_GROUPS': {
        "role_types": {
            "access_env": "accessenv",
            "change_settings": "changesettings",
            "view_logs": "logviewer",
            "view_sensitive": "viewsensitive"
        },
        "role_tenants": [
            "nonprod",
            "prod"
        ]
    },
    'USER_GROUP_TEMPLATE': "prefix_{USER_TYPE}_{TENANT}_{APP_NAME}_suffix",
    'DEFAULT_TIMEZONE': "UTC",
}




def get_setting(attribute):
    """Fetch setting from user-defined files or else default values

    Args:
        attribute (str): attribute/setting to retreive

    Raises:
        AttributeError: Setting not defaulted nor user-defined

    Returns:
        [type]: attribute in it's correct variable type if found
    """
    global __IMPORTED_SETTINGS__ # pylint: disable=global-statement
    if attribute in __IMPORTED_SETTINGS__:
        return __IMPORTED_SETTINGS__[attribute]
    if attribute in DefaultSettings:
        return DefaultSettings[attribute]
    raise AttributeError(
        f"{attribute} is not a valid user variable attribute!")

def get_cluster_dict(cluster):
    """Get Cluster Dict\n
    @param cluster_name (dict, str) - Name of the cluster to return\n
    @return - Cluster dictionary
    """
    if isinstance(cluster, dict):
        return cluster

    if 'FULL_SET' in __IMPORTED_SETTINGS__ and cluster in __IMPORTED_SETTINGS__['FULL_SET']:
        return __IMPORTED_SETTINGS__['FULL_SET'][cluster]

    raise ValueError ("Cluster not found")

def create_cluster(cluster_name, url, **kwargs):
    """Allow user to dynamically create cluster
     \n
    @param cluster_name (str) - Name of cluster to be added to the Cluster Set \n
    @param url (str) - URL for cluster \n
    \n
    @kwargs tenant_ids (dict) - Dynatrace tenant name or dictionary of tenant ids\n
    @kwargs tenant_tokens (dict) - Dynatrace tenant tokens\n
    @kwargs cluster_token - provide cluster_token (Managed only)\n
    @kwargs verify_ssl - Verify SSL Cert. Either Bool or path to cert\n
    @kwargs is_managed - Manual flag if cluster is a managed instance\n\n
    @return - number of entities
    """

    verify_ssl = True if 'verify_ssl' not in kwargs else kwargs['verify_ssl']
    is_managed =  True if 'is_managed' not in kwargs else kwargs['is_managed']
    tenant_ids =  None if 'tenant_ids' not in kwargs else kwargs['tenant_ids']
    tenant_tokens =  None if 'tenant_tokens' not in kwargs else kwargs['tenant_tokens']

    cluster = {
        'url': url,
        'tenant': {},
        'api_token': {},
        'verify_ssl': verify_ssl,
        'is_managed': is_managed,
    }

    if 'cluster_token' in kwargs:
        cluster['cluster_token'] = kwargs['cluster_token']

    if isinstance(tenant_ids, dict) and isinstance(tenant_tokens, dict):
        for tenant in tenant_ids:
            cluster['tenant'][tenant] = tenant_ids [tenant]
            cluster['api_token'][tenant] = tenant_tokens [tenant]
    elif not(tenant_ids is None and tenant_tokens is None):
        raise ValueError("Tenant and tenant token must both be dict")

    if 'FULL_SET' not in __IMPORTED_SETTINGS__:
        __IMPORTED_SETTINGS__['FULL_SET'] = {}
    __IMPORTED_SETTINGS__['FULL_SET'][cluster_name] = cluster
    return __IMPORTED_SETTINGS__['FULL_SET'][cluster_name]

def add_tenant_to_cluster(cluster, tenant_id, tenant_token, tenant_name):
    """Add tenant to predefined cluster"""
    if isinstance (cluster, dict):
        raise NotImplementedError(
                "Cluster dicts are not supported yet. Please use str for the cluster's key"
        )
    if isinstance(tenant_id, str) and isinstance(tenant_token, str):
        if cluster in __IMPORTED_SETTINGS__['FULL_SET']:
            __IMPORTED_SETTINGS__['FULL_SET'][cluster]['tenant'][tenant_name] = tenant_id
            __IMPORTED_SETTINGS__['FULL_SET'][cluster]['api_token'][tenant_name] = tenant_token
        else:
            raise KeyError("Cluster not found")
        return __IMPORTED_SETTINGS__['FULL_SET'][cluster]

    raise ValueError("Tenant and tenant token must both be dict")

def load_settings_from_file(settings_file):
    """Assign setting value)s as defined by the cluster"""
    global __IMPORTED_SETTINGS__ # pylint: disable=global-statement

    if str.endswith(settings_file, ".yaml") or str.endswith(settings_file, ".yml"):
        with open(settings_file) as file:
            imported_settings = yaml.load(file, Loader=yaml.FullLoader)

    if str.endswith(settings_file, ".json"):
        with open(settings_file) as file:
            imported_settings = json.load(file)

    for setting, value in imported_settings.items():
        __IMPORTED_SETTINGS__[setting] = value

"""Module for retreiving settings safely"""
import yaml
import json
try:
    import user_variables  # pylint: disable=import-error
    FILE_IMPORTED = True
except ImportError:
    FILE_IMPORTED = False

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

__IMPORTED_SETTINGS__ = None


def get_setting(attribute):
    """Fetch setting from user-defined files or else default values

    Args:
        attribute (str): attribute/setting to retreive

    Raises:
        AttributeError: Setting not defaulted nor user-defined

    Returns:
        [type]: attribute in it's correct variable type if found
    """
    global __IMPORTED_SETTINGS__
    if attribute in __IMPORTED_SETTINGS__:
        return __IMPORTED_SETTINGS__[attribute]
    # print (__IMPORTED_SETTINGS__)
    if FILE_IMPORTED and hasattr(user_variables, attribute):
        return getattr(user_variables, attribute)
    if attribute in DefaultSettings:
        return DefaultSettings[attribute]
    raise AttributeError(
        f"{attribute} is not a valid user variable attribute!")

def create_cluster(url, tenant_ids, tenant_tokens, **kwargs):
    """Allow user to dynamically create cluster
     \n
    @param tenant_ids (dict) - Dynatrace tenant name or dictionary of tenant ids\n
    @param tenant_tokens (dict) - Dynatrace tenant tokens\n
    @param cluster_token (str) - Dynatrace cluster tokens\n
    \n
    @kwargs cluster_token - provide cluster_token (Managed only)\n
    @kwargs verify_ssl - Verify SSL Cert. Either Bool or path to cert\n
    @kwargs is_managed - Manual flag if cluster is a managed instance\n\n
    @return - number of entities
    """

    verify_ssl = True if 'verify_ssl' not in kwargs else kwargs['verify_ssl']
    is_managed =  False if 'is_managed' not in kwargs else kwargs['is_managed']

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
    else:
        raise ValueError("tenant and tenant token must both be dict")
    return cluster

def add_tenant_to_cluster(cluster, tenant_id, tenant_token, tenant_name):
    """Add tenant to predefined cluster"""
    if isinstance(tenant_id, str) and isinstance(tenant_token, str):
        cluster ['tenant'] [tenant_name] = tenant_id
        cluster ['api_token'] [tenant_name] = tenant_token

def load_settings_from_file(settings_file):
    """Assign setting value)s as defined by the cluster"""
    global __IMPORTED_SETTINGS__

    if str.endswith(settings_file, ".yaml") or str.endswith(settings_file, ".yml"):
        with open(settings_file) as file:
            imported_settings = yaml.load(file, Loader=yaml.FullLoader)

    if str.endswith(settings_file, ".json"):
        with open(settings_file) as file:
            imported_settings = json.load(file)

    if __IMPORTED_SETTINGS__ is None:
        __IMPORTED_SETTINGS__ = imported_settings
    else:
        for setting, value in imported_settings.items():
            __IMPORTED_SETTINGS__[setting] = value

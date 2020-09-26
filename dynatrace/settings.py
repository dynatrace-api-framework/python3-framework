"""Module for retreiving settings safely"""
try:
    import user_variables
    FILE_IMPORTED = True
except ImportError:
    FILE_IMPORTED = False


DefaultSettings = {
    'LOG_LEVEL': None,
    'LOG_DIR': "logs/",

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
    if FILE_IMPORTED and hasattr(user_variables, attribute):
        return getattr(user_variables, attribute)
    if attribute in DefaultSettings:
        return DefaultSettings[attribute]
    raise AttributeError(
        f"{attribute} is not a valid user variable attribute!")

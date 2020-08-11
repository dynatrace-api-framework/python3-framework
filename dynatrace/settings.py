try:
    import user_variables
    FILE_IMPORTED = True
except ImportError:
    FILE_IMPORTED = False


class DefaultSettings():
    LOG_LEVEL = None
    LOG_DIR = "logs/"

    # ROLE TYPE KEYS
    # access_env
    # change_settings
    # install_agent
    # view_logs
    # view_senstive
    # change_sensitive

    USER_GROUPS = {
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
    }
    USER_GROUP_TEMPLATE = "prefix_{USER_TYPE}_{TENANT}_{APP_NAME}_suffix"
    DEFAULT_TIMEZONE = "UTC"


def get_setting(attribute):
    if FILE_IMPORTED and hasattr(user_variables, attribute):
        return getattr(user_variables, attribute)
    elif hasattr(DefaultSettings, attribute):
        return getattr(DefaultSettings, attribute)
    else:
        raise AttributeError(
            f"{attribute} is not a valid user variable attribute!")

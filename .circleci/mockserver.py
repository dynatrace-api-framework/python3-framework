"""User variables to use toolkit for Dynatrace"""
FULL_SET = {
    "mockserver1": {
        "url": "mockserver:1080",
        "tenant": {
            "tenant1": "mockenv",
        },
        "api_token": {
            "tenant1": "sample_api_token",
        },
        "verify_ssl": False,
        "is_managed": True,
        "cluster_token": "Required for Cluster Operations in Managed"
    }
}

LOG_OUTPUT = "FILE"
LOG_LEVEL = "INFO"

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

DEFAULT_TIMEZONE = "America/Chicago"

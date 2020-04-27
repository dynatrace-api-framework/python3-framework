"""User variables to use toolkit for Dynatrace"""
FULL_SET = {
    "CLUSTER_NAME": {
        "url":"URL GOES HERE (EVEN FOR SAAS)",
        "tenant": {
            "tenant1": "TENANT UUID GOES HERE",
            "tenant2": "TENANT UUID GOES HERE"
        },
        "api_token": {
            "tenant1": "API TOKEN GOES HERE",
            "tenant2": "API TOKEN GOES HERE",
        },
        "is_managed": True,
        "cluster_token": "Required for Cluster Operations in Managed"
    }
}

# ROLE TYPE KEYS
# access_env
# change_settings
# install_agent
# view_logs
# view_senstive
# change_sensitive

USER_GROUPS = {
    "role_types":{
        "access_env": "accessenv",
        "change_settings": "changesettings",
        "view_logs": "logviewer",
        "view_sensitive": "viewsensitive"
    },
    "role_tenants":[
        "nonprod",
        "prod"
    ]
}

USER_GROUP_TEMPLATE = "prefix_{USER_TYPE}_{TENANT}_{APP_NAME}_suffix"

DEFAULT_TIMEZONE = "America/Chicago"

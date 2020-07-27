"""SSO Operations for Dynatrace"""
import dynatrace.requests.request_handler as rh

ENDPOINT = "sso/ssoProvider"


def disable_sso(cluster):
    """Disable SSO Sign-in"""
    disable_payload = {
        "ssoProvider": "NONE",
        "loginPage": "STANDARD",
        "ssoEnabled": False,
        "ssoGroupsEnabled": False,
        "ssoLoginDisabled": True
    }
    response = rh.make_api_call(cluster=cluster,
                                endpoint=ENDPOINT,
                                method=rh.HTTP.POST,
                                json=disable_payload)
    return response.status_code


def enable_sso(cluster, disable_local=False, groups_enabled=False, is_openid=False):
    """Turns on SSO that has already been configured"""
    enable_payload = {
        "ssoProvider": "SAML",
        "loginPage": "STANDARD",
        "ssoEnabled": True,
        "ssoGroupsEnabled": False,
        "ssoLoginDisabled": False
    }

    if disable_local:
        enable_payload['loginPage'] = "SSO"
    if groups_enabled:
        enable_payload['ssoGroupsEnabled'] = True
    if is_openid:
        enable_payload['ssoProvider'] = "OIDC"

    response = rh.make_api_call(cluster=cluster,
                                endpoint=ENDPOINT,
                                method=rh.HTTP.POST,
                                json=enable_payload)
    return response.status_code


def get_sso_status(cluster):
    response = rh.make_api_call(cluster=cluster,
                                endpoint=ENDPOINT)
    return response.json()

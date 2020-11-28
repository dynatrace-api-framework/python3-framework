"""Operations for interacting with the ActiveGates (environment v2) API"""
from dynatrace.framework import request_handler as rh

ENDPOINT = str(rh.TenantAPIs.ACTIVEGATES)


def get_all_activegates(cluster, tenant, **kwargs):
    """Gets all ActiveGates available in the tenant.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)
    \n
    @returns list - list of ActiveGates
    """
    ag_list = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        params=kwargs
    ).json().get("activeGates")

    return ag_list


def get_activegate_details(cluster, tenant, activegate_id):
    """Gets the details of an ActiveGate.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param activegate_id (str) - ID of ActiveGate
    \n
    @returns dict - ActiveGate details
    """
    details = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{activegate_id}"
    ).json()

    return details


def create_update_job(cluster, tenant, activegate_id, job):
    """Create a new job to trigger an update on an ActiveGate.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param activegate_id (str) - ID of ActiveGate\n
    @param job (dict) - job details to be sent as JSON payload
    \n
    @returns Response - HTTP response for the request
    """
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{activegate_id}/updateJobs",
        method=rh.HTTP.POST,
        json=job
    )

    return response


def get_update_job_details(cluster, tenant, activegate_id, job_id):
    """Get the details of an update job from an ActiveGate.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param activegate_id (str) - ID of ActiveGate\n
    @param job_id (str) - ID of job
    \n
    @returns dict - details of the updated job
    """
    details = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{activegate_id}/updateJobs/{job_id}"
    ).json()

    return details


def delete_update_job(cluster, tenant, activegate_id, job_id):
    """Deletes an update job from an ActiveGate.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param activegate_id (str) - ID of ActiveGate\n
    @param job_id (str) - ID of job
    \n
    @returns Response - HTTP response for the request
    """
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{activegate_id}/updateJobs/{job_id}",
        method=rh.HTTP.DELETE
    )

    return response


def get_all_update_jobs(cluster, tenant, **kwargs):
    """Gets a list of all update jobs in the tenant matching given criteria.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    \n
    @returns list - list of update jobs
    """
    jobs = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/updateJobs",
        params=kwargs
    ).json().get("allUpdateJobs")

    return jobs

"""Module for interactions with the Problems (V2) API"""
from dynatrace.framework import request_handler as rh, logging

ENDPOINT = str(rh.TenantAPIs.PROBLEMS)
logger = logging.get_logger(__name__)


def get_all_problems(cluster, tenant, **kwargs):
    """Gets the list of all problems mathing the query parameters.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)
    \n
    @returns list - list of problems
    """
    logger.info(f"Getting problems from tenant {tenant}")
    problems_list = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        api_version=2,
        item="problems",
        **kwargs
    ).get('problems')

    return problems_list


def get_problem_count(cluster, tenant, **kwargs):
    """Gets the total number of problems matching query parameters.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)
    \n
    @returns int - number of problems
    """
    logger.info(f"Getting the total problem count in tenant {tenant}")
    problems_list = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=ENDPOINT,
        params=kwargs
    ).json()
    count = problems_list.get('totalCount')

    return count


def get_problem_details(cluster, tenant, problem_id, **kwargs):
    """Retrieves the details of a specific problem.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem to retrieve
    \n
    @kwargs fields (str) - comma separated list of fields to include in details.
                           (evidenceDetails, impactAnalysis, recentComments)
    \n
    @returns (dict) - problem details
    """
    logger.info(f"Getting problem details for problem {problem_id}")
    details = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}",
        params=kwargs
    ).json()

    return details


def close_problem(cluster, tenant, problem_id, comment=""):
    """Manually closes an open problem, leaving a comment.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem to close\n
    @param comment (str) - closing comment
    \n
    @returns Response - HTTP response for the request
    """
    logger.info(f"Closing problem {problem_id}")
    logger.info(f"Closing comment: {comment}")
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}/close",
        method=rh.HTTP.POST,
        json=dict(message=comment)
    )

    return response


def get_all_comments(cluster, tenant, problem_id, **kwargs):
    """Gets a list of all comments of a problem.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem to close
    \n
    @kwargs pageSize (int) - affects number of API calls
    \n
    @returns list - list of comments
    """
    logger.info(f"Getting comments from problem {problem_id}")
    comments = rh.get_results_whole(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}/comments",
        api_version=2,
        item="comments",
        **kwargs
    ).get("comments")

    return comments


def get_comment(cluster, tenant, problem_id, comment_id):
    """Gets a comment from a Problem.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem containing the comment\n
    @param comment_id (str) - ID fo the comment to retrieve
    \n
    @returns dict - comment details
    """
    logger.info(f"Getting details for comment {comment_id} from problem {problem_id}")
    comment = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}/comments/{comment_id}"
    ).json()

    return comment


def add_comment(cluster, tenant, problem_id, **kwargs):
    """Adds a comment to a problem.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem to add the comment to
    \n
    @kwargs comment (str) - comment content\n
    @kwargs context (str) - comment context. added under "via ..."
    \n
    @returns Response - HTTP response for the request
    """
    logger.info(f"Adding comment to problem {problem_id}")
    comment = kwargs.get("comment") if "comment" in kwargs else ""
    context = kwargs.get("context") if "context" in kwargs else ""

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}/comments",
        method=rh.HTTP.POST,
        json=dict(comment=comment, context=context)
    )

    return response


def update_comment(cluster, tenant, problem_id, comment_id, **kwargs):
    """Updates an existing comment of a problem.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem containing the comment\n
    @param comment_id (str) - ID of the comment to update
    \n
    @kwargs comment (str) - comment content\n
    @kwargs context (str) - comment context. added under "via ..."
    \n
    @returns Response - HTTP response for the request
    """
    logger.info(f"Updating comment {comment_id} from problem {problem_id}")
    comment = get_comment(cluster, tenant, problem_id, comment_id)

    if "comment" in kwargs:
        comment["comment"] = kwargs.get("comment")
    if "context" in kwargs:
        comment["context"] = kwargs.get("context")

    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}/comments/{comment_id}",
        method=rh.HTTP.PUT,
        json=comment
    )

    return response


def delete_comment(cluster, tenant, problem_id, comment_id):
    """Deletes a comment from a problem.
    \n
    @param cluster (dict) - Dynatrace Cluster (as taken from variable set)\n
    @param tenant (str) - name of Dynatrace Tenant (as taken from variable set)\n
    @param problem_id (str) - ID of the problem containing the comment\n
    @param comment_id (str) - ID of the comment to delete
    \n
    @returns Response - HTTP response for the request
    """
    logger.info(f"Deleting comment {comment_id} from problem {problem_id}")
    response = rh.make_api_call(
        cluster=cluster,
        tenant=tenant,
        endpoint=f"{ENDPOINT}/{problem_id}/comments/{comment_id}",
        method=rh.HTTP.DELETE
    )

    return response

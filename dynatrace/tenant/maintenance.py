"""Maintenance Window Operations"""
import datetime
import re
from enum import Enum, auto
import dynatrace.requests.request_handler as rh
import user_variables
from dynatrace.exceptions import InvalidDateFormatException


MZ_ENDPOINT = rh.TenantAPIs.MAINTENANCE_WINDOWS


class Suppression(Enum):
    """
    Types of suppression for create Maintenance Window JSON. Suppression is required

    Args:
        Enum (DETECT_PROBLEMS_AND_ALERT): Full Detection and Alerting during Maintenance Window
        Enum (DETECT_PROBLEMS_DONT_ALERT): Problems detected but alerts in scope are not triggered
        Enum (DONT_DETECT_PROBLEMS): Problem detection completely off for the scope
    """
    DETECT_PROBLEMS_AND_ALERT = auto()
    DETECT_PROBLEMS_DONT_ALERT = auto()
    DONT_DETECT_PROBLEMS = auto()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class DayOfWeek(Enum):
    """
    Day of the Week

    Args:
        Enum (MONDAY): MONDAY
        Enum (TUESDAY): TUESDAY
        Enum (WEDNESDAY): WEDNESDAY
        Enum (THURSDAY): THURSDAY
        Enum (FRIDAY): FRIDAY
        Enum (SATURDAY): SATURDAY
        Enum (SUNDAY): SUNDAY
    """

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class Context(Enum):
    """Tag Contexts that are available"""
    AWS = auto()
    AWS_GENERIC = auto()
    AZURE = auto()
    CLOUD_FOUNDRY = auto()
    CONTEXTLESS = auto()
    ENVIRONMENT = auto()
    GOOGLE_CLOUD = auto()
    KUBERNETES = auto()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class RecurrenceType(Enum):
    """Recurrence of the Maintenance Window"""
    DAILY = auto()
    MONTHLY = auto()
    ONCE = auto()
    WEEKLY = auto()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class FilterType(Enum):
    """All Filter Types available for tag filters"""
    APM_SECURITY_GATEWAY = auto()
    APPLICATION = auto()
    APPLICATION_METHOD = auto()
    APPLICATION_METHOD_GROUP = auto()
    APPMON_SERVER = auto()
    APPMON_SYSTEM_PROFILE = auto()
    AUTO_SCALING_GROUP = auto()
    AUXILIARY_SYNTHETIC_TEST = auto()
    AWS_APPLICATION_LOAD_BALANCER = auto()
    AWS_AVAILABILITY_ZONE = auto()
    AWS_CREDENTIALS = auto()
    AWS_LAMBDA_FUNCTION = auto()
    AWS_NETWORK_LOAD_BALANCER = auto()
    AZURE_API_MANAGEMENT_SERVICE = auto()
    AZURE_APPLICATION_GATEWAY = auto()
    AZURE_COSMOS_DB = auto()
    AZURE_CREDENTIALS = auto()
    AZURE_EVENT_HUB = auto()
    AZURE_EVENT_HUB_NAMESPACE = auto()
    AZURE_FUNCTION_APP = auto()
    AZURE_IOT_HUB = auto()
    AZURE_LOAD_BALANCER = auto()
    AZURE_MGMT_GROUP = auto()
    AZURE_REDIS_CACHE = auto()
    AZURE_REGION = auto()
    AZURE_SERVICE_BUS_NAMESPACE = auto()
    AZURE_SERVICE_BUS_QUEUE = auto()
    AZURE_SERVICE_BUS_TOPIC = auto()
    AZURE_SQL_DATABASE = auto()
    AZURE_SQL_ELASTIC_POOL = auto()
    AZURE_SQL_SERVER = auto()
    AZURE_STORAGE_ACCOUNT = auto()
    AZURE_SUBSCRIPTION = auto()
    AZURE_TENANT = auto()
    AZURE_VM = auto()
    AZURE_VM_SCALE_SET = auto()
    AZURE_WEB_APP = auto()
    CF_APPLICATION = auto()
    CF_FOUNDATION = auto()
    CINDER_VOLUME = auto()
    CLOUD_APPLICATION = auto()
    CLOUD_APPLICATION_INSTANCE = auto()
    CLOUD_APPLICATION_NAMESPACE = auto()
    CONTAINER_GROUP = auto()
    CONTAINER_GROUP_INSTANCE = auto()
    CUSTOM_APPLICATION = auto()
    CUSTOM_DEVICE = auto()
    CUSTOM_DEVICE_GROUP = auto()
    DCRUM_APPLICATION = auto()
    DCRUM_SERVICE = auto()
    DCRUM_SERVICE_INSTANCE = auto()
    DEVICE_APPLICATION_METHOD = auto()
    DISK = auto()
    DOCKER_CONTAINER_GROUP = auto()
    DOCKER_CONTAINER_GROUP_INSTANCE = auto()
    DYNAMO_DB_TABLE = auto()
    EBS_VOLUME = auto()
    EC2_INSTANCE = auto()
    ELASTIC_LOAD_BALANCER = auto()
    ENVIRONMENT = auto()
    EXTERNAL_SYNTHETIC_TEST_STEP = auto()
    GCP_ZONE = auto()
    GEOLOCATION = auto()
    GEOLOC_SITE = auto()
    GOOGLE_COMPUTE_ENGINE = auto()
    HOST = auto()
    HOST_GROUP = auto()
    HTTP_CHECK = auto()
    HTTP_CHECK_STEP = auto()
    HYPERVISOR = auto()
    KUBERNETES_CLUSTER = auto()
    KUBERNETES_NODE = auto()
    MOBILE_APPLICATION = auto()
    NETWORK_INTERFACE = auto()
    NEUTRON_SUBNET = auto()
    OPENSTACK_PROJECT = auto()
    OPENSTACK_REGION = auto()
    OPENSTACK_VM = auto()
    OS = auto()
    PROCESS_GROUP = auto()
    PROCESS_GROUP_INSTANCE = auto()
    RELATIONAL_DATABASE_SERVICE = auto()
    SERVICE = auto()
    SERVICE_INSTANCE = auto()
    SERVICE_METHOD = auto()
    SERVICE_METHOD_GROUP = auto()
    SWIFT_CONTAINER = auto()
    SYNTHETIC_LOCATION = auto()
    SYNTHETIC_TEST = auto()
    SYNTHETIC_TEST_STEP = auto()
    VIRTUALMACHINE = auto()
    VMWARE_DATACENTER = auto()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


def validate_datetime(datetime_text, required_format):
    """Validate input against expected DateTime format

    Args:
        datetime_text (str): Time inputted
        required_format (str): Expected format to validate against

    Raises:
        InvalidDateFormatException: Used for incorrect format provided
    """
    try:
        datetime.datetime.strptime(datetime_text, required_format)
    except ValueError:
        raise InvalidDateFormatException(required_format) from ValueError


def generate_tag_scope(tag, filter_type=None, management_zone_id=None):
    """Generating Tag portion of scope

    Args:
        tag (list, dict, str): single or collection of tags
        filter_type (str, optional): Type of entity to match against. Defaults to None.
        management_zone_id (str, optional): Management Zone to match against. Defaults to None.

    Raises:
        ValueError: Filter Type is not in acceptable values

    Returns:
        dict: tag payload to be used as part of the main scope payload
    """
    tag_payload = {}

    if management_zone_id:
        tag_payload['mzId'] = str(management_zone_id)

    if filter_type:
        if filter_type in FilterType._member_names_:  # pylint: disable=no-member,protected-access
            tag_payload['type'] = filter_type
        else:
            raise ValueError(
                "Invalid Filter Type! " +
                "Please Refer to Enum or Dynatrace Documentation"
            )

    if isinstance(tag, list) and len(tag) > 0:
        tag_payload['tags'] = tag
    elif isinstance(tag, dict):
        tag_payload['tags'] = [tag]
    elif isinstance(tag, str):
        tag_payload['tags'] = [{'context': "CONTEXTLESS", 'key': tag}]

    return tag_payload


def generate_scope(
    entities=None,
    tags=None,
    filter_type=None,
    management_zone_id=None,
    match_any_tag=True
):
    """Generate the total scope for maintenance window payload

    Args:
        entities (list, optional): List of specific entities. Defaults to None.
        tags (List,Dict,str, optional): List/Set/Individual Tags. Defaults to None.
        filter_type (str, optional): Specific Entity Type for tag. Defaults to None.
        management_zone_id ([type], optional): Specific MZ for tag. Defaults to None.
        match_any_tag (bool, optional): Any vs All. Defaults to True.

    Returns:
        dict: sub payload for maintenance window payload containing scope
    """
    if entities is None:
        entities = []
    matches = []

    if match_any_tag and isinstance(tags, list) and len(tags) > 1:
        for tag in tags:
            matches.append(
                generate_tag_scope(
                    tag,
                    filter_type=filter_type,
                    management_zone_id=management_zone_id
                )
            )
    else:
        matches.append(
            generate_tag_scope(
                tags,
                filter_type=filter_type,
                management_zone_id=management_zone_id
            )
        )

    scope = {
        'entities': entities,
        'matches': matches
    }
    return scope


def generate_window_json(name, description, suppression, schedule, scope=None, is_planned=False,):
    """Generate JSON information needed for creating Maintenance Window"""
    window_json = {
        "name": name,
        "description": description,
        "suppression": str(suppression),
        "schedule": schedule
    }
    window_json['type'] = "PLANNED" if is_planned else "UNPLANNED"
    if scope is not None:
        window_json['scope'] = scope
    return window_json


def generate_schedule(
    recurrence_type,
    start_time,
    duration,
    range_start,
    range_end,
    day=None,
    zone_id=None,
):
    """Create schedule structure for maintenance window"""
    # This structure requires a lot of input validation
    recurrence_type = str(recurrence_type).upper()

    # Check Recurrence
    if recurrence_type not in RecurrenceType._member_names_:  # pylint: disable=no-member,protected-access
        raise ValueError(
            "Invalid Recurrence Type! Allowed values are: ONCE, DAILY, WEEKLY, MONTHLY")

    # Check ranges
    validate_datetime(range_start, "%Y-%m-%d %H:%M")
    validate_datetime(range_end, "%Y-%m-%d %H:%M")

    schedule = {
        "recurrenceType": recurrence_type,
        "start": range_start,
        "end": range_end
    }

    if zone_id is None:
        schedule['zoneId'] = user_variables.DEFAULT_TIMEZONE

    if recurrence_type != "ONCE":
        # Check Start Time
        validate_datetime(start_time, "%H:%M")

        # Check Duration
        try:
            int(duration)
        except ValueError:
            print("Duration time must be integer! Duration of Maintainence Window in minutes")

        schedule['recurrence'] = {
            "startTime": start_time,
            "durationMinutes": duration
        }

    # Check Weekly Day
    if recurrence_type == "WEEKLY":
        day = str(day).upper()
        if day in DayOfWeek._member_names_:  # pylint: disable=no-member,protected-access
            schedule['recurrence']['dayOfWeek'] = day
        else:
            raise ValueError("Invalid Weekly Day! Allowed values are "
                             + "SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY")

    # Check Monthly Day
    if recurrence_type == "MONTHLY":
        if not isinstance(day, int):
            raise TypeError("Invalid type for Day of Month! Int between 1-31 required")
        if 1 <= int(day) <= 31:
            schedule['recurrence']['dayOfMonth'] = day
        else:
            raise ValueError("Invalid Monthly Day! Allowed values are 1-31")

    return schedule


def create_window(cluster, tenant, json):
    """Create Maintenance Window"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.POST,
                                endpoint=MZ_ENDPOINT,
                                json=json)
    return response.json()


def update_window(cluster, tenant, window_id, json):
    """Update Maintenance Window"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.PUT,
                                endpoint=f"{MZ_ENDPOINT}/{window_id}",
                                json=json)
    return response.status_code


def delete_window(cluster, tenant, window_id):
    """Delete Maintenance Window"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                method=rh.HTTP.DELETE,
                                endpoint=f"{MZ_ENDPOINT}/{window_id}")
    return response.status_code


def get_windows(cluster, tenant):
    """Return List of Maintenance Windows in Effect"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=MZ_ENDPOINT)
    return response.json()


def get_window(cluster, tenant, window_id):
    """Return Maintenance Window Details"""
    response = rh.make_api_call(cluster=cluster,
                                tenant=tenant,
                                endpoint=f"{MZ_ENDPOINT}/{window_id}")
    return response.json()


def parse_tag(tag_string):
    # Need a way to process literal colon inside a key
    "Parsing Tag to to Context, Key and Value"
    tag_match = re.match(
        r"(?:\[(\w+)\])?([\w\-\/`\+\.\!\@\#\$\%\^\&\*\(\)\?\[\]\{\}\,\<\>\ \:\;]+)(?:\:(\w*))?",
        tag_string
    )
    tag_dictionary = {}
    if tag_match.group(1):
        tag_dictionary['context'] = tag_match.group(1)
    else:
        tag_dictionary['context'] = "CONTEXTLESS"

    tag_dictionary['key'] = tag_match.group(2)  # Key is always required

    if tag_match.group(3):
        tag_dictionary['value'] = tag_match.group(3)

    return tag_dictionary

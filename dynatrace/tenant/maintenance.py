"""Maintenance Window Operations"""
import datetime
import re
import dynatrace.requests.request_handler as rh
import user_variables as uv
from dynatrace.exceptions import InvalidDateFormatException
from enum import Enum, auto


MZ_ENDPOINT = rh.TenantAPIs.MAINTENANCE_WINDOWS

class Suppression(Enum):
    """
    Types of suppression for create Maintenance Window JSON. Suppression is required

    Args:
        Enum (DETECT_PROBLEMS_AND_ALERT): Full Alerting. Entites in scope will have notes that a Maintenance Window was active
        Enum (DETECT_PROBLEMS_DONT_ALERT): Problems detected but alerting profiles in that scope are not triggered
        Enum (DONT_DETECT_PROBLEMS): Problem detection completely off for the scope
    """
    DETECT_PROBLEMS_AND_ALERT = auto()
    DETECT_PROBLEMS_DONT_ALERT = auto()
    DONT_DETECT_PROBLEMS = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Day(Enum):
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
        return self.name

    def __repr__(self):
        return self.name

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
        return self.name

    def __repr__(self):
        return self.name
class RecurrenceType(Enum):
    """Recurrence of the Maintenance Window"""
    DAILY = auto()
    MONTHLY = auto()
    ONCE = auto()
    WEEKLY = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

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
        return self.name

    def __repr__(self):
        return self.name

def validate_datetime(datetime_text, required_format):
    try:
        datetime.datetime.strptime(datetime_text, required_format)
    except ValueError:
        raise InvalidDateFormatException(required_format)

def generate_tag_scope(tag, filter_type=None, management_zone_id=None):
    tag_payload = {}

    if management_zone_id:
        tag_payload ['managementZoneId'] = str(management_zone_id)

    if isinstance (tag, list) and len(tag) > 0:
        tag_payload ['tags'] = tag
    elif isinstance (tag, dict):
        tag_payload ['tags'] = [tag]
    elif isinstance (tag, str):
        tag_payload ['tags'] = [{'context': "CONTEXTLESS",'key': tag}]

    return tag_payload

def generate_scope(entities=None, filter_type=None, management_zone_id=None, tags=None, match_any_tag=True):
    if entities is None:
        entities = []
    matches = []
    matches_payload = {}
    # if isinstance(filter_type, str):
        # matches_payload['type'] = filter_type

    if match_any_tag and isinstance(tags, list) and len(tags)>1:
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

    # if isinstance(match_any_tag, bool):
    #     matches_payload['tagsCombination'] = "OR" if match_any_tag \
    #             else "AND"

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
        "suppression": suppression,
        "schedule": schedule
    }
    window_json['type'] = "PLANNED" if is_planned else "UNPLANNED"
    if scope is not None:
        window_json['scope'] = scope
    return window_json


def generate_schedule(recurrence_type, start_time, duration, range_start, range_end, day=None, zoneId=None,):
    """Create schedule structure for maintenance window"""
    # This structure requires a lot of input validation
    types_available = ["DAILY", "MONTHLY", "ONCE", "WEEKLY"]
    days_of_week = ["FRIDAY", "MONDAY", "SATURDAY",
                    "SUNDAY", "THURSDAY", "TUESDAY", "WEDNESDAY"]

    recurrence_type = str(recurrence_type).upper()

    # Check Recurrence
    if recurrence_type not in types_available:
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

    if zoneId is None:
        schedule['zoneId'] = uv.DEFAULT_TIMEZONE

    if recurrence_type != "ONCE":
        # Check Start Time
        validate_datetime(start_time, "%H:%M")

        # Check Duration
        try:
            int(duration)
        except ValueError:
            ("Duration time must be an integer! Duration is length of Maintainence Window in minutes")

        schedule['recurrence'] = {
            "startTime": start_time,
            "durationMinutes": duration
        }

    # Check Weekly Day
    if recurrence_type == "WEEKLY":
        day = str(day).upper()
        if day in days_of_week:
            schedule['recurrence']['dayOfWeek'] = day
        else:
            raise ValueError("Invalid Weekly Day! Allowed values are "
                            + "SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY")

    # Check Monthly Day
    if recurrence_type == "MONTHLY":
        if (1 <= int(day) <= 31):
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
    m = re.match(
        r"(?:\[(\w+)\])?([\w\-\/`\+\.\!\@\#\$\%\^\&\*\(\)\?\[\]\{\}\,\<\>\ \:\;]+)(?:\:(\w*))?",
        tag_string
    )
    tag_dictionary = {}
    if m.group(1):
        tag_dictionary['context'] = m.group(1)
    else:
        tag_dictionary['context'] = "CONTEXTLESS"

    tag_dictionary['key'] = m.group(2)  # Key is always required

    if m.group(3):
        tag_dictionary['value'] = m.group(3)

    return tag_dictionary

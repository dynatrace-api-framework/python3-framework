"""Maintenance Window Operations"""
import datetime
import re
import dynatrace.requests.request_handler as rh
import user_variables as uv
from dynatrace.exceptions import InvalidDateFormatException


MZ_ENDPOINT = rh.TenantAPIs.MAINTENANCE_WINDOWS

def validate_datetime(datetime_text, required_format):
    try:
        datetime.datetime.strptime(datetime_text, required_format)
    except ValueError:
        raise InvalidDateFormatException(required_format)


def generate_scope(entities=None, filter_type=None, management_zone_id=None, tags=None, matches_any_tag=False):
    if entities is None:
        entities = []
    matches = []
    matches_payload = {}
    if isinstance(filter_type, str):
        matches_payload['type'] = filter_type
    if management_zone_id:
        matches_payload['managementZoneId'] = management_zone_id
    if isinstance(tags, list):
        matches_payload['tags'] = tags

    matches.append(matches_payload)

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
    return response.status_code


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

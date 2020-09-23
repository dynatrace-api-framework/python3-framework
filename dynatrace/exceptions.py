'''
Module containing all the custom exceptions for this project
'''
from sys import stderr


class InvalidAPIResponseException (Exception):
    """The framework did not get an expected result from the Dynatrace API"""
    def __init__(self, message):
        super(InvalidAPIResponseException, Exception).__init__(message)
        print(message, file=stderr)


class InvalidDateFormatException(ValueError):
    """The Date provided does not match the format needed"""
    def __init__(self, required_format):
        super(InvalidDateFormatException, ValueError).__init__(required_format)
        self.message = f"Incorrect Date for following entry: {required_format}"


class InvalidScopeException(ValueError):
    """The Scope is incomplete or misconfigured"""
    def __init__(self, required_format):
        super(InvalidScopeException, ValueError).__init__(required_format)
        self.required_format = required_format
        print("Invalid scope used. Tag required for management zone, matching rule: %s",
              required_format, file=stderr)


class ManagedClusterOnlyException(TypeError):
    """The operation is only supported on a managed cluster"""
    def __init__(self):
        super(ManagedClusterOnlyException, TypeError).__init__()
        print("This operation is only supported on Dynatrace Managed!", file=stderr)

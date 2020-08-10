'''
Module containing all the custom exceptions for this project
'''
from sys import stderr


class InvalidAPIResponseException (Exception):
    def __init__(self, message):
        print(message, file=stderr)


class InvalidDateFormatException(ValueError):
    def __init__(self, required_format):
        self.message = f"Incorrect Date for following entry: {required_format}"

class InvalidScopeException(ValueError):
    def __init__(self, required_format):
        self.required_format = required_format
        print("Invalid scope used. Tag required for management zone, matching rule: %s",
              required_format, file=stderr)


class ManagedClusterOnlyException(TypeError):
    def __init__(self):
        print("This operation is only supported on Dynatrace Managed!", file=stderr)

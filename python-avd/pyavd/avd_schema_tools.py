from typing import Generator

from .vendor.errors import AvdConversionWarning, AvdDeprecationWarning
from .vendor.schema.avdschema import AvdSchema

IGNORE_EXCEPTIONS = (AvdDeprecationWarning, AvdConversionWarning)


class AvdSchemaTools:
    """
    Tools that wrap the various schema components for easy use
    """

    def __init__(self, schema_id: str) -> None:
        self.avdschema = AvdSchema(schema_id=schema_id)

    def convert_data(self, data: dict) -> tuple[bool, list[str]]:
        """
        Convert data according to the schema (convert_types)
        The data conversion is done in-place (updating the original "data" dict).

        Returns
        bool
            True if Conversion succeeded. False if it failed.
        list[str]
            Any errors raised during variable conversion
        """
        result = True
        errors = []

        # avdschema.convert returns a Generator, so we have to iterate through it to perform the actual conversions.
        exceptions: Generator = self.avdschema.convert(data)
        for exception in exceptions:
            # Ignore conversions and deprecations
            if exception is None or isinstance(exception, IGNORE_EXCEPTIONS):
                continue

            errors.append(exception)
            result = False

        return result, errors

    def validate_data(self, data: dict) -> tuple[bool, list[str]]:
        """
        Validate data according to the schema

        Returns
        bool
            True if data is valid. False if not.
        list[str]
            Any errors raised during data validation.
            This will contain errors raised as well as data validation issues.
        """
        result = True
        errors = []

        # avdschema.validate returns a Generator, so we have to iterate through it to perform the actual validations.
        exceptions: Generator = self.avdschema.validate(data)
        for exception in exceptions:
            # Ignore conversions and deprecations
            if exception is None or isinstance(exception, IGNORE_EXCEPTIONS):
                continue

            errors.append(exception)
            result = False

        return result, errors

    def convert_and_validate_data(self, data: dict) -> tuple[bool, list[str]]:
        """
        Convert and validate data according to the schema

        Returns
        bool
            True if Conversion succeeded and data is valid. False if either failed.
        list[str]
            Any errors raised during variable conversion and validation
            This will contain errors raised as well as data validation issues.
        """
        result, conversion_errors = self.convert_data(data)
        if not result:
            return result, conversion_errors

        result, validation_errors = self.validate_data(data)
        return result, conversion_errors + validation_errors

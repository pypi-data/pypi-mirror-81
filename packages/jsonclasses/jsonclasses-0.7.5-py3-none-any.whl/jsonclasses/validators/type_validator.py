"""module for validator validator."""
from ..exceptions import ValidationException
from ..fields import FieldDescription, FieldType
from ..contexts import ValidatingContext
from .validator import Validator


class TypeValidator(Validator):
    """Abstract validator for checking object's type."""

    def __init__(self) -> None:
        self.cls: type = object
        self.field_type: FieldType = FieldType.ANY

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.STR

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if type(context.value) is self.cls:
            return
        raise ValidationException(
            {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be {self.cls.__name__}.'},
            context.root
        )

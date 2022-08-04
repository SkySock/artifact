from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


@deconstructible
class FileSizeValidator:
    message = _(
        "File size must be <= %(megabyte_limit)s megabytes. "
        "Current file size are: %(file_size)s megabytes."
    )
    code = "exceeded_size"

    def __init__(self, megabyte_limit=None, message=None, code=None):
        self.megabyte_limit = megabyte_limit

        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if (
            self.megabyte_limit is not None
            and self.megabyte_limit * 1024 * 1024 <= value.size
        ):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "file_size": str(value.size / 1024 / 1024),
                    "megabyte_limit": str(self.megabyte_limit),
                    "value": value,
                },
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.megabyte_limit == other.megabyte_limit
            and self.message == other.message
            and self.code == other.code
        )

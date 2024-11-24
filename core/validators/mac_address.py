from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class MacAddressValidator:
    message = "O valor não é um endereço MAC válido"
    HEX_DIGITS = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
    ]
    code = "invalid"

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code

    def __call__(self, value):
        value = str(value).upper()

        if len(value) != 17:
            raise ValidationError(self.message, code=self.code, params={"value": value})
        if "-" not in value and ":" not in value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if "-" in value:
            splited = value.split("-")
        else:
            splited = value.split(":")

        if len(splited) != 6:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        for item in splited:
            if len(item) != 2:
                raise ValidationError(
                    self.message, code=self.code, params={"value": value}
                )

            a = item[0]
            b = item[1]

            if a not in self.HEX_DIGITS or b not in self.HEX_DIGITS:
                raise ValidationError(
                    self.message, code=self.code, params={"value": value}
                )


validate_mac_address = MacAddressValidator()

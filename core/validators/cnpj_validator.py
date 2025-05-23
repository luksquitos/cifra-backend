import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CNPJValidator:
    def __init__(self):
        # pattern for the standard format 00.000.000/0000-00
        self.pattern = re.compile(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$")

    def _digit_calculator(self, remainder: int) -> int:
        return 0 if remainder < 2 else 11 - remainder

    def __call__(self, cnpj: str) -> None:
        # 1) check format
        if not self.pattern.match(cnpj):
            raise ValidationError("CNPJ deve estar no formato 00.000.000/0000-00")

        # 2) remove non-digit characters
        numbers = re.sub(r"\D", "", cnpj)

        # 3) reject sequences of the same digit
        if numbers == numbers[0] * 14:
            raise ValidationError("CNPJ inválido")

        # convert to list of integers
        digits = list(map(int, numbers))

        # 4) calculate check digits
        def calculate(base: list[int], weights: list[int]) -> int:
            total = sum(b * w for b, w in zip(base, weights))
            return self._digit_calculator(total % 11)

        first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        second_weights = [6] + first_weights

        first_check = calculate(digits[:12], first_weights)
        second_check = calculate(digits[:12] + [first_check], second_weights)

        # 5) validate final digits
        if digits[12] != first_check or digits[13] != second_check:
            raise ValidationError("CNPJ inválido")


validate_cnpj = CNPJValidator()

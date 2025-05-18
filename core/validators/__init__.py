from .cnpj_validator import validate_cnpj
from .cpf_validator import CPFValidator, validate_cpf
from .phone_validator import PhoneValidator, validate_phone
from .postal_code import PostalCodeValidator, validate_postal_code

__all__ = [
    "validate_postal_code",
    "PostalCodeValidator",
    "validate_phone",
    "PhoneValidator",
    "CPFValidator",
    "validate_cpf",
    "validate_cnpj",
]

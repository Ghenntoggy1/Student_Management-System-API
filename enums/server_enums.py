from enum import Enum

class JWTValidationResultsEnum(str, Enum):
    is_valid = 'IS_VALID'
    is_invalid = 'IS_INVALID'
    is_expired = 'IS_EXPIRED'
    invalid_signature = 'INVALID_SIGNATURE'
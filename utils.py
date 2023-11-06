import locale
import re


def get_system_language():
    lang, _ = locale.getlocale()
    return "ru" if lang and lang.startswith("ru") else "en"


class Status:
    """
    Constants representing the status codes from SmsHub.
    """

    ERROR = -1
    WAIT = 0
    SENT = 1
    REPEAT = 3
    SUCCESS = 6
    CANCEL = 8


class Methods:
    GET_NUMBER_STATUS = "getNumbersStatus"
    GET_BALANCE = "getBalance"
    GET_NUMBER = "getNumber"
    SET_STATUS = "setStatus"
    GET_STATUS = "getStatus"
    GET_PRICES = "getPrices"


GET_NUMBER_STATUS_ERROR_PATTERN = r"(BAD_KEY|ERROR_SQL|BAD_ACTION)"
GET_NUMBER_STATUS_ERROR_REGEX = re.compile(GET_NUMBER_STATUS_ERROR_PATTERN)
GET_BALANCE_ERROR_PATTERN = r"(BAD_KEY|ERROR_SQL|BAD_ACTION)"
GET_BALANCE_ERROR_REGEX = re.compile(GET_BALANCE_ERROR_PATTERN)
GET_NUMBER_ERROR_PATTERN = (
    r"(BAD_KEY|ERROR_SQL|BAD_ACTION|BAD_SERVICE|NO_NUMBERS|NO_BALANCE|API_KEY_NOT_VALID"
    r"|WRONG_SERVICE)"
)
GET_NUMBER_ERROR_REGEX = re.compile(GET_NUMBER_ERROR_PATTERN)
GET_NUMBER_OK_PATTERN = r"(ACCESS_NUMBER)"
GET_NUMBER_OK_REGEX = re.compile(GET_NUMBER_OK_PATTERN)
STATUS_ERROR_PATTERN = r"(BAD_KEY|ERROR_SQL|BAD_ACTION|NO_ACTIVATION)"
STATUS_ERROR_REGEX = re.compile(STATUS_ERROR_PATTERN)
STATUS_OK_PATTERN = r"(STATUS_WAIT_CODE|STATUS_CANCEL|STATUS_WAIT_RETRY|STATUS_OK)"
STATUS_OK_REGEX = re.compile(STATUS_OK_PATTERN)


def clean_params(params):
    """Remove None values from a dictionary."""
    return {k: v for k, v in params.items() if v is not None}

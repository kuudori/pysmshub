import json
import re

from pysmshub.exceptions import SmsHubApiException
from pysmshub.utils import (
    GET_BALANCE_ERROR_REGEX,
    Methods,
    GET_NUMBER_ERROR_REGEX,
    GET_NUMBER_OK_REGEX,
    STATUS_ERROR_REGEX,
    STATUS_OK_REGEX,
    Status,
    GET_NUMBER_STATUS_ERROR_REGEX,
)


def _parse_get_number_status_response(response) -> dict:
    if match := GET_NUMBER_STATUS_ERROR_REGEX.search(response):
        error_code = match.group(1)
        raise SmsHubApiException(method=Methods.GET_NUMBER_STATUS, error=error_code)
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise SmsHubApiException(
            method=Methods.GET_NUMBER_STATUS, error="JSON Decode Error"
        ) from e


def _parse_get_balance_response(response) -> float:
    if match := GET_BALANCE_ERROR_REGEX.search(response):
        error_code = match.group(1)
        raise SmsHubApiException(method=Methods.GET_BALANCE, error=error_code)
    balance_match = re.search(r"(\d+\.\d+)", response)
    return float(balance_match[0]) if balance_match else 0.0


def _parse_get_number_response(response) -> tuple:
    if match := GET_NUMBER_ERROR_REGEX.search(response):
        error_code = match.group(1)
        raise SmsHubApiException(method=Methods.GET_NUMBER, error=error_code)
    elif GET_NUMBER_OK_REGEX.search(response):
        parts = response.split(":")
        if len(parts) >= 3:
            return parts[1], parts[2]
    raise SmsHubApiException(
        method=Methods.GET_NUMBER,
        error="Unexpected response format when obtaining number",
    )


def _parse_get_status_response(response) -> tuple:
    if error_match := STATUS_ERROR_REGEX.search(response.upper()):
        error_code = error_match.group(1)
        raise SmsHubApiException(method=Methods.GET_STATUS, error=error_code)

    if not (ok_match := STATUS_OK_REGEX.search(response.upper())):
        raise SmsHubApiException(method=Methods.GET_STATUS, error="")
    status_code = ok_match.group(1)
    if status_code == "STATUS_WAIT_CODE":
        return Status.WAIT, None
    elif status_code == "STATUS_CANCEL":
        return Status.CANCEL, None
    elif status_code.startswith("STATUS_WAIT_RETRY"):
        return Status.REPEAT, response.split(":")[1]
    elif status_code.startswith("STATUS_OK"):
        return Status.SENT, response.split(":")[1]


def _parse_get_prices_response(response) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise SmsHubApiException(
            method=Methods.GET_PRICES, error="JSON Decode Error"
        ) from e

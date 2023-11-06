import requests
from pysmshub.base import BaseSmsHubApi
from pysmshub.exceptions import ConnectionErrorException
from pysmshub.handlers import (
    _parse_get_balance_response,
    _parse_get_number_response,
    _parse_get_status_response,
    _parse_get_prices_response,
    _parse_get_number_status_response,
)
from pysmshub.utils import (
    Status,
    Methods,
)


class SyncSmsHubApi(BaseSmsHubApi):
    def _make_request(self, action: str, **params) -> str:
        """
        Sends a GET request to the API's endpoint with the specified action and parameters.

        :param action: The API action to perform.
        :param params: Additional parameters for the action.
        :return: Text response from the server.
        """
        params |= {"api_key": self.api_key, "action": action}
        try:
            response = requests.get(self.base_url, params=params, proxies=self.proxies)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionErrorException() from e
        return response.text

    def get_numbers_status(self, country: str = None, operator: str = None) -> dict:
        """
        Fetches the status of available numbers for a given country and operator.

        :param country: Country code.
        :param operator: Mobile operator name.
        :return: Text response from the server.
        """
        response = self._make_request(
            Methods.GET_NUMBER_STATUS, country=country, operator=operator
        )
        return _parse_get_number_status_response(response)

    def get_balance(self) -> float:
        """
        Retrieves the current balance of the account.

        :return: The balance amount.
        """
        response = self._make_request(Methods.GET_BALANCE)
        return _parse_get_balance_response(response=response)

    def get_number(
        self,
        service: str,
        operator: str = None,
        country: int = None,
        max_price: int = None,
    ) -> tuple:
        """
        Obtains a number for the given service, country, and operator.

        :param service: The desired service for which the number is needed.
        :param operator: Mobile operator name.
        :param country: Country code.
        :param max_price: Max price to buy.
        :return: Tuple containing ID and the obtained number.
        """
        response = self._make_request(
            action=Methods.GET_NUMBER,
            service=service,
            operator=operator,
            country=country,
            maxPrice=max_price,
        )
        return _parse_get_number_response(response)

    def set_status(self, id: int, status: Status) -> str:
        """
        Updates the status for a given ID.

        :param id: The ID for which the status needs to be updated.
        :param status: The desired status to set.
        :return: Text response from the server.
        """
        return self._make_request(Methods.SET_STATUS, id=id, status=status)

    def get_status(self, id: int) -> tuple:
        """
        Retrieves the status for a given ID.

        :param id: The ID whose status needs to be fetched.
        :return: Tuple containing the status and associated message/code.
        """
        response = self._make_request(Methods.GET_STATUS, id=id)
        return _parse_get_status_response(response)

    def get_prices(self, service: str = None, country: str = None) -> dict:
        """
        Retrieves the prices for a specific service and country.

        :param service: The desired service for which prices are required.
        :param country: Country code.
        :return: Text response from the server.
        """
        response = self._make_request(
            Methods.GET_PRICES, service=service, country=country
        )
        return _parse_get_prices_response(response)

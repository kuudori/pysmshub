import aiohttp

from pysmshub.base import BaseSmsHubApi
from pysmshub.exceptions import ConnectionErrorException
from pysmshub.handlers import (
    _parse_get_number_status_response,
    _parse_get_balance_response,
    _parse_get_number_response,
    _parse_get_status_response,
    _parse_get_prices_response,
)
from pysmshub.utils import (
    Status,
    Methods,
    clean_params,
)


class AsyncSmsHubApi(BaseSmsHubApi):
    async def _make_request(self, action: str, **params):
        """
        Sends a GET request to the API's endpoint with the specified action and parameters.

        :param action: The API action to perform.
        :param params: Additional parameters for the action.
        :return: Text response from the server.
        """
        filtered_params = clean_params(params)
        filtered_params.update({"api_key": self.api_key, "action": action})
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url, params=filtered_params, proxy=self.proxy
                ) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError as e:
            raise ConnectionErrorException() from e

    async def get_numbers_status(
        self, country: str = None, operator: str = None
    ) -> dict:
        """
        Fetches the status of available numbers for a given country and operator.

        :param country: Country code.
        :param operator: Mobile operator name.
        :return: Text response from the server.
        """
        response = await self._make_request(
            Methods.GET_NUMBER_STATUS, country=country, operator=operator
        )

        return _parse_get_number_status_response(response)

    async def get_balance(self) -> float:
        """
        Retrieves the current balance of the account.

        :return: The balance amount.
        """
        response = await self._make_request(Methods.GET_BALANCE)
        return _parse_get_balance_response(response=response)

    async def get_number(
        self, service: str, operator: str = None, country: str = None
    ) -> tuple:
        """
        Obtains a number for the given service, country, and operator.

        :param service: The desired service for which the number is needed.
        :param operator: Mobile operator name.
        :param country: Country code.
        :param max_price: Max price to buy.
        :return: Tuple containing ID and the obtained number.
        """
        response = await self._make_request(
            Methods.GET_NUMBER, service=service, operator=operator, country=country
        )
        return _parse_get_number_response(response)

    async def set_status(self, id: int, status: Status) -> str:
        """
        Updates the status for a given ID.

        :param id: The ID for which the status needs to be updated.
        :param status: The desired status to set.
        :return: Text response from the server.
        """
        return await self._make_request(Methods.SET_STATUS, id=id, status=status)

    async def get_status(self, id: int) -> tuple:
        """
        Retrieves the status for a given ID.

        :param id: The ID whose status needs to be fetched.
        :return: Tuple containing the status and associated message/code.
        """
        response = await self._make_request(Methods.GET_STATUS, id=id)
        return _parse_get_status_response(response)

    async def get_prices(self, service: str, country: str = None) -> dict:
        """
        Retrieves the prices for a specific service and country.

        :param service: The desired service for which prices are required.
        :param country: Country code.
        :return: Text response from the server.
        """
        response = await self._make_request(
            Methods.GET_PRICES, service=service, country=country
        )
        return _parse_get_prices_response(response)

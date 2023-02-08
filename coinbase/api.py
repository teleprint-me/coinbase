# teleprint-me/coinbase - Another Unofficial Python Wrapper for Coinbase
# Copyright (C) 2021 Austin Berrio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from dataclasses import dataclass
from dataclasses import field

from dotenv import load_dotenv

from os import getenv

load_dotenv()


def get_api_settings() -> dict:
    """
    Retrieves the API settings from environment variables.

    Returns:
        dict: A dictionary containing the API key, secret, REST URL, and feed URL.
    """
    API_KEY = getenv("API_KEY")
    API_SECRET = getenv("API_SECRET")
    API_REST = getenv("API_REST")
    API_FEED = getenv("API_FEED")
    return {
        "key": API_KEY,
        "secret": API_SECRET,
        "rest": API_REST,
        "feed": API_FEED,
    }


@dataclass
class API:
    """A class to manage the coinbase API information.

    :param settings: a dictionary of API settings with keys "key", "secret", "rest", and "feed". Defaults to the result of `get_api_settings()`.
    :type settings: dict, optional
    """

    settings: dict = field(default_factory=get_api_settings)

    @property
    def key(self) -> str:
        """Return the API key, which is required for making requests."""
        return self.settings.get("key", "")

    @property
    def secret(self) -> str:
        """Return the API secret, which is required for making requests."""
        return self.settings.get("secret", "")

    @property
    def rest(self) -> str:
        """Return the API endpoint for REST API."""
        return self.settings.get("rest", "https://api.coinbase.com")

    @property
    def version(self) -> int:
        """Return the API version number 2."""
        return 2

    def path(self, value: str) -> str:
        """Return the API path by adding version and value as endpoint.

        :param value: the API endpoint that is passed in
        :return: the API path with the version and endpoint
        """
        if value.startswith(f"/v{self.version}"):
            return value
        return f'/v{self.version}/{value.lstrip("/")}'

    def url(self, value: str) -> str:
        return f'{self.rest}/{self.path(value).lstrip("/")}'


class AdvancedAPI(API):
    """A subclass of API that implements version 3 of the API and a modified path method.

    :param API: Base API class
    """

    @property
    def version(self) -> int:
        """Return the API version number 3"""
        return 3

    def path(self, value: str) -> str:
        """Return the API path with the version and brokerages added.

        :param value: API endpoint argument
        :return: the API path with the version and brokerages added
        """
        if value.startswith(f"/api/v{self.version}"):
            return value
        return f'/api/v{self.version}/brokerage/{value.lstrip("/")}'


# WIP
class WebSocketAPI(AdvancedAPI):
    """A subclass of `AdvancedAPI` that represents the Coinbase WebSocket API.

    Adds the `feed` property to retrieve the WebSocket URL from the `settings` dictionary.
    """

    @property
    def feed(self) -> str:
        """Retrieve the WebSocket URL from the `settings` dictionary.

        :return: the WebSocket URL, or the default URL if not found in `settings`
        """
        return self.settings.get(
            "feed", "wss://advanced-trade-ws.coinbase.com"
        )

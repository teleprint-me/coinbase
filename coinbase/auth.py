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
import hashlib
import hmac

from time import time

from requests.auth import AuthBase

from requests.models import PreparedRequest

from coinbase import __agent__
from coinbase import __source__
from coinbase import __version__

from coinbase.api import API


class Auth(AuthBase):
    """Create and return an HTTP request with authentication headers.

    :param api: Instance of the API class, if not provided, a default instance is created.
    """

    def __init__(self, api: API = None):
        """Create an instance of the Auth class.

        :param api: Instance of the API class, if not provided, a default instance is created.
        """
        self.__api: API = api if api else API()

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """Return the prepared request with updated headers.

        :param request: A prepared HTTP request.
        :return: The same request with updated headers.
        """
        timestamp: str = str(int(time()))
        body: str = (
            "" if request.body is None else request.body.decode("utf-8")
        )
        message: str = (
            f"{timestamp}{request.method.upper()}{request.path_url}{body}"
        )
        header: dict = self.header(timestamp, message)
        request.headers.update(header)
        return request

    @property
    def api(self) -> API:
        """Return the API instance.

        :return: The API instance.
        """
        return self.__api

    def signature(self, message: str) -> str:
        """Return the signature of a message.

        :param message: The message to sign.
        :return: The signature of the message.
        """
        key = self.api.secret.encode("ascii")
        msg = message.encode("ascii")
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def header(self, timestamp: str, message: str) -> dict:
        """Return the headers for an authenticated request.

        :param timestamp: The timestamp of the request.
        :param message: The message to sign.
        :return: The headers for an authenticated request.
        """
        return {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "CB-ACCESS-KEY": self.api.key,
            "CB-ACCESS-SIGN": self.signature(message),
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-VERSION": "2021-08-03",
            "Content-Type": "application/json",
        }

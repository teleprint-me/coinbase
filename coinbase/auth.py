# teleprint-me/coinbase - A Python Wrapper for Coinbase
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
    def __init__(self, api: API = None):
        self.__api: API = api if api else API()

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp: str = str(int(time()))
        body: str = "" if request.body is None else request.body.decode("utf-8")
        message: str = f"{timestamp}{request.method.upper()}{request.path_url}{body}"
        header: dict = self.header(timestamp, message)
        request.headers.update(header)
        return request

    @property
    def api(self) -> API:
        return self.__api

    def signature(self, message: str) -> str:
        key = self.api.secret.encode("ascii")
        msg = message.encode("ascii")
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def header(self, timestamp: str, message: str) -> dict:
        return {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "CB-ACCESS-KEY": self.api.key,
            "CB-ACCESS-SIGN": self.signature(message),
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-VERSION": "2021-08-03",
            "Content-Type": "application/json",
        }

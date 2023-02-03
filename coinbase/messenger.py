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
from dataclasses import dataclass, field
from time import sleep, time

from requests import Response, Session
from requests.auth import AuthBase
from requests.models import PreparedRequest

from coinbase import __agent__, __limit__, __page__, __source__, __version__
from coinbase.abstract import (
    AbstractAPI,
    AbstractAuth,
    AbstractMessenger,
    AbstractSubscriber,
)


@dataclass
class API(AbstractAPI):
    settings: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return self.settings.get("key", "")

    @property
    def secret(self) -> str:
        return self.settings.get("secret", "")

    @property
    def rest(self) -> str:
        return self.settings.get("rest", "https://api.coinbase.com")

    @property
    def version(self) -> int:
        return 2

    def path(self, value: str) -> str:
        if value.startswith(f"/v{self.version}"):
            return value
        return f'/v{self.version}/{value.lstrip("/")}'

    def url(self, value: str) -> str:
        return f'{self.rest}/{self.path(value).lstrip("/")}'


class Auth(AbstractAuth, AuthBase):
    def __init__(self, api: API = None):
        self.__api = api if api else API()

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = str(int(time()))
        body = "" if request.body is None else request.body.decode("utf-8")
        message = f"{timestamp}{request.method.upper()}{request.path_url}{body}"
        header = self.header(timestamp, message)
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


class Messenger(AbstractMessenger):
    def __init__(self, auth: Auth = None):
        self.__auth: AbstractAuth = auth if auth else Auth()
        self.__session: Session = Session()

    @property
    def auth(self) -> Auth:
        return self.__auth

    @property
    def api(self) -> API:
        return self.__auth.api

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def timeout(self) -> int:
        return 30

    def get(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.get(
            self.api.url(path), params=data, auth=self.auth, timeout=self.timeout
        )

    def post(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.post(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def put(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.put(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def delete(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.delete(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def page(self, path: str, data: dict = None) -> Response:
        responses = []
        if not data:
            data = {"limit": __page__}
        while True:
            response = self.get(path, data)
            payload = response.json()
            if 200 != response.status_code:
                return [response]
            if not payload:
                break
            if "pagination" not in payload:
                raise KeyError("This request does not support pagination")
            responses.append(response)
            page = payload["pagination"]
            if not page["next_uri"]:
                break
            data["starting_after"] = page["next_starting_after"]
        return responses

    def close(self):
        self.session.close()


class Subscriber(AbstractSubscriber):
    def __init__(self, messenger: AbstractMessenger):
        self.__messenger = messenger

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def error(self, response: Response) -> bool:
        return 200 != response.status_code


def get_messenger(settings: dict = None) -> Messenger:
    return Messenger(Auth(API(settings if settings else dict())))

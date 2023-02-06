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
from time import sleep

from requests import Response
from requests import Session

from coinbase import __agent__
from coinbase import __limit__
from coinbase import __source__
from coinbase import __version__

from coinbase.api import API
from coinbase.api import AdvancedAPI

from coinbase.auth import Auth


class Messenger:
    def __init__(self, auth: Auth = None):
        self.__auth: Auth = auth if auth else Auth()
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
            self.api.url(path),
            params=data,
            auth=self.auth,
            timeout=self.timeout,
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

    def page(self, path: str, data: dict = None) -> list[Response]:
        responses = []
        if not data:
            data = {"limit": 25}
        while True:
            response = self.get(path, data)
            if 200 != response.status_code:
                return [response]
            payload = response.json()
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


class AdvancedMessenger(Messenger):
    def get(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.get(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def page(self, path: str, data: dict = None) -> list[Response]:
        responses = []
        if not data:
            data = {"limit": 50}
        while True:
            response = self.get(path, data)
            if 200 != response.status_code:
                return [response]
            payload = response.json()
            if not payload:
                break
            if "has_next" not in payload:
                raise KeyError("This request does not support pagination")
            if not payload["has_next"]:
                break
            if "cursor" in data:
                if data["cursor"] == payload["cursor"]:
                    break
            responses.append(response)
            data["cursor"] = payload["cursor"]
        return responses


class Subscriber:
    def __init__(self, messenger: Messenger):
        self.__messenger = messenger

    @property
    def messenger(self) -> Messenger:
        return self.__messenger

    def error(self, response: Response) -> bool:
        return 200 != response.status_code


def get_messenger(settings: dict) -> Messenger:
    return Messenger(Auth(API(settings)))


def get_advanced_messenger(settings: dict) -> AdvancedMessenger:
    return AdvancedMessenger(Auth(AdvancedAPI(settings)))

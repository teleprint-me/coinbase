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
    """Class to manage HTTP request/response with authentication and session.

    :param auth: (optional) authentication instance to pass to this class
    """

    def __init__(self, auth: Auth = None):
        self.__auth: Auth = auth if auth else Auth()
        self.__session: Session = Session()

    @property
    def auth(self) -> Auth:
        """Return the authentication instance.

        :return: authentication instance
        """
        return self.__auth

    @property
    def api(self) -> API:
        """Return the API instance from the authentication instance.

        :return: API instance
        """
        return self.__auth.api

    @property
    def session(self) -> Session:
        """Return the session instance.

        :return: session instance
        """
        return self.__session

    @property
    def timeout(self) -> int:
        """Return the timeout value for HTTP request.

        :return: timeout value in seconds
        """
        return 30

    def get(self, path: str, data: dict = None) -> Response:
        """Perform a GET request to the specified API path.

        :param path: The API endpoint to be requested.
        :param data: (optional) Query parameters to be passed with the request.
        :return: The response of the GET request.
        """
        sleep(__limit__)
        return self.session.get(
            self.api.url(path),
            params=data,
            auth=self.auth,
            timeout=self.timeout,
        )

    def post(self, path: str, data: dict = None) -> Response:
        """Perform a POST request to the specified API path.

        :param path: The API endpoint to be requested.
        :param data: (optional) JSON payload to be sent with the request.
        :return: The response of the POST request.
        """
        sleep(__limit__)
        return self.session.post(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def put(self, path: str, data: dict = None) -> Response:
        """Perform a PUT request to the specified API path.

        :param path: The API endpoint to be requested.
        :param data: (optional) JSON payload to be sent with the request.
        :return: The response of the PUT request.
        """
        sleep(__limit__)
        return self.session.put(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def delete(self, path: str, data: dict = None) -> Response:
        """Perform a DELETE request to the specified API path.

        :param path: The API endpoint to be requested.
        :param data: (optional) JSON payload to be sent with the request.
        :return: The response of the DELETE request.
        """
        sleep(__limit__)
        return self.session.delete(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def page(self, path: str, data: dict = None) -> list[Response]:
        """Get paginated responses from the API.

        :param path: The API endpoint to send the request to.
        :param data: Data to include in the request query parameters.
        :return: A list of Response objects.
        """

        responses: list[Response] = []
        if not data:
            data = {"limit": 25}
        while True:
            response: Response = self.get(path, data)
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
        """Close the underlying session object.

        :param session: Close session object used to make API requests. This method should be called after all API requests are complete.

        :return: None
        """
        self.session.close()


class AdvancedMessenger(Messenger):
    """Class for making API requests. Inherits from the Messenger class.

    :param Messenger: Base class for making API requests.
    """

    def get(self, path: str, data: dict = None) -> Response:
        """Get a single API response.

        :param path: The API endpoint to send the request to.
        :param data: Data to include in the request query parameters.
        :return: A single Response object.
        """
        sleep(__limit__)
        return self.session.get(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def page(self, path: str, data: dict = None) -> list[Response]:
        """Get paginated responses from the API.

        :param path: The API endpoint to send the request to.
        :param data: Data to include in the request query parameters.
        :return: A list of Response objects.
        """

        responses: list[Response] = []
        if not data:
            data = {"limit": 50}
        while True:
            response: Response = self.get(path, data)
            if 200 != response.status_code:
                return [response]
            payload: dict = response.json()
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
    """Class for handling API requests as a subscriber.

    :param messenger: Messenger object for handling API requests.
    """

    def __init__(self, messenger: Messenger):
        self.__messenger = messenger

    @property
    def messenger(self) -> Messenger:
        """Return the messenger object used for API requests.

        :return: Messenger object.
        """
        return self.__messenger

    def error(self, response: Response) -> bool:
        """Check if a response from the API is an error.

        :param response: Response object returned from an API request.
        :return: True if response status code is not 200, False otherwise.
        """
        return 200 != response.status_code


def get_messenger(settings: dict) -> Messenger:
    """Create and return a Messenger object.

    :param settings: Dictionary containing API authentication and connection settings.
    :return: Messenger object.
    """
    return Messenger(Auth(API(settings)))


def get_advanced_messenger(settings: dict) -> AdvancedMessenger:
    """Create and return an AdvancedMessenger object.

    :param settings: Dictionary containing API authentication and connection settings.
    :return: AdvancedMessenger object.
    """
    return AdvancedMessenger(Auth(AdvancedAPI(settings)))

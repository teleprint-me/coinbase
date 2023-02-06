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
from dataclasses import dataclass
from dataclasses import field

from dotenv import load_dotenv

from os import getenv

load_dotenv()


def get_api_settings() -> dict:
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
    settings: dict = field(default_factory=get_api_settings)

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


class AdvancedAPI(API):
    @property
    def version(self) -> int:
        return 3

    def path(self, value: str) -> str:
        if value.startswith(f"/api/v{self.version}"):
            return value
        return f'/api/v{self.version}/brokerage/{value.lstrip("/")}'


# WIP
class WebSocketAPI(AdvancedAPI):
    @property
    def feed(self) -> str:
        return self.settings.get(
            "feed", "wss://advanced-trade-ws.coinbase.com"
        )

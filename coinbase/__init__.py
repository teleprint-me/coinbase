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
__agent__: str = "teleprint-me/coinbase"
# The name of the agent using the code

__source__: str = f"https://github.com/{__agent__}"
# The source of the code. This is a link to the GitHub repository.

__version__: str = "0.4.0"
# The version of the code.

__limit__: float = 1 / (10000 / 3600)
# The rate limit of the API requests, in seconds.
# This is calculated as 1 / (10000 requests per hour / 3600 seconds per hour)
# The rate limit is used to block a request for at least 0.36 seconds.

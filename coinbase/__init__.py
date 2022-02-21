# teleprint-me/coinbase - A Python Wrapper for Coinbase
# Copyright (C) 2021 teleprint.me
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
__source__: str = f"https://github.com/{__agent__}"
__version__: str = "0.0.1"
# the number of results per pagination
__page__: int = 25
# 10,000 requests per hour / 3,600 seconds per hour
# how many requests can we make per second?
# 1 request / 0.36 seconds
__limit__: float = 1 / (10000 / 3600)

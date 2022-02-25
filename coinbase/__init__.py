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
__version__: str = "0.2.2"
# the number of results per paginated request
__page__: int = 25
# how many requests can we make per second?
# we know we can make "10,000 requests per hour".
# we know that there are "3,600 seconds per hour".
# we need to know what "1 request per [n] seconds" is.
#       1 request / [n] seconds
# [n] is the number of requests we can make per second.
#       n -> 10000 requests per hour / 3600 seconds per hour
#       n -> [2.7...] requests / second; where [...] is repeating
# rate limit -> 1 request / (10000 rph / 3600 rph) second
# rate limit -> 1 request / [2.7...] second
# rate limit -> 0.36 seconds
# __limit__ is used to block a request for at least 0.36 seconds.
__limit__: float = 1 / (10000 / 3600)

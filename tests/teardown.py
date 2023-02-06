import time

from coinbase import __limit__


class Teardown:
    @staticmethod
    def teardown_method():
        # Avoid rate limit
        time.sleep(__limit__)

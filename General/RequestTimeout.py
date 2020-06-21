import time
import sys


class RequestTimeout:

    @staticmethod
    def check_availability(response):
        status = response.status_code
        if status == 429:
            return True
        else:
            return False

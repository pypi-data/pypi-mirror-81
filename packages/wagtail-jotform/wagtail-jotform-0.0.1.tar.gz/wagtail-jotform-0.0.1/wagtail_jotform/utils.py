import logging

from django.conf import settings
from django.core.cache import cache

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout

logger = logging.getLogger(__name__)


class CantPullFromAPI(Exception):
    pass


def fetch_data(url, headers=None, **params):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except Timeout:
        logger.exception(f"Timeout error occurred when fetching data from {url}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    except (HTTPError, ConnectionError):
        logger.exception(f"HTTP/ConnectionError occured when fetching data from {url}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    except Exception:
        logger.exception(f"Exception occured when fetching data from {url}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    else:
        return response.json()


def fetch_jotform_data():

    headers = {"APIKEY": settings.JOTFORM_API_KEY}
    url = f"{settings.JOTFORM_API_URL}/user/forms"

    return fetch_data(url, headers)


class _BaseContentAPI:
    def __init__(self, func, cache_key):
        self.func = func
        self.cache_key = cache_key

    def fetch_from_api(self):
        try:
            data = self.func()
        except CantPullFromAPI:
            pass
        else:
            cache.set(self.cache_key, data, None)

    def get_data(self):
        data = cache.get(self.cache_key)
        if data is not None:
            return data
        return []


class JotFormAPI(_BaseContentAPI):
    def __init__(self):
        super().__init__(fetch_jotform_data, "jotform_data")


def parse_jotform_data(data):
    return data

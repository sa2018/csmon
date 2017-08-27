import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from config import Config


class Client(object):

    def __init__(self, url=None):

        if not url:
            raise ValueError("URL is missing")

        self.__url = url
        self.__session = requests.Session()
        retries = Retry(total=Config.get('CHECK_CONN_MAX_RETRY'),
                        backoff_factor=Config.get('CHECK_BACK_OFF_FACTOR'),
                        status_forcelist=[500,  # Internal Server Error
                                          502,  # Bad Gateway
                                          503,  # Service Unavailable
                                          504   # Gateway Timeout
                                          ])

        self.__session.mount('http://', HTTPAdapter(max_retries=retries))
        self.__session.mount('https://', HTTPAdapter(max_retries=retries))
        self.response = None

    def get_try_count(self):
        return Config.get('CHECK_CONN_MAX_RETRY') - \
               self.response.raw.retries.total + 1

    def get(self):
        timeout = Config.get('CHECK_CONN_TIMEOUT')
        self.response = self.__session.get(self.__url, timeout=timeout)
        return self.response

    def get_response_code(self):
        return self.response.status_code

    def get_response_body(self):
        return self.response.content

    def get_response_time_in_ms(self, response):
        hours, minutes, seconds = str(response.elapsed).split(':')
        total = 0.00
        total += ((int(hours) / 60) / 60) / 1000
        total += (int(minutes) / 60) / 1000
        total += float(seconds) * 1000

        return "%i" % total

from requests.exceptions import ConnectionError, RetryError
from ..utils.config import Config
from ..utils.client import Client
import time
import re


class Task(object):
    """
    Process to run health checks
    """

    # Response code mappings
    response_codes = {
        "100": "Continue",
        "101": "Switching Protocols",
        "200": "OK",
        "201": "Created",
        "202": "Accepted",
        "203": "Non-Authoritative Information",
        "204": "No Content",
        "205": "Reset Content",
        "206": "Partial Content",
        "300": "Multiple Choices",
        "301": "Moved Permanently",
        "302": "Found",
        "303": "See Other",
        "304": "Not Modified",
        "305": "Use Proxy",
        "307": "Temporary Redirect",
        "400": "Bad Request",
        "401": "Unauthorized",
        "402": "Payment Required",
        "403": "Forbidden",
        "404": "Not Found",
        "405": "Method Not Allowed",
        "406": "Not Acceptable",
        "407": "Proxy Authentication Required",
        "408": "Request Timeout",
        "409": "Conflict",
        "410": "Gone",
        "411": "Length Required",
        "412": "Precondition Failed",
        "413": "Request Entity Too Large",
        "414": "Request-URI Too Long",
        "415": "Unsupported Media Type",
        "416": "Requested Range Not Satisfiable",
        "417": "Expectation Failed",
        "500": "Internal Server Error",
        "501": "Not Implemented",
        "502": "Bad Gateway",
        "503": "Service Unavailable",
        "504": "Gateway Timeout",
        "505": "HTTP Version Not Supported"
    }

    # Network error string to code mappings
    network_errors = {
        'Connection refused': 'NET_CONN',
        'nodename nor servname provided, or not known': 'NET_DNS',
        'No route to host': 'NET_ROUTE',
        "ReadTimeoutError": "NET_TIMEOUT",
        "CertificateError": "NET_SSL_CERT",
        "Network is unreachable": "NET_UNREACHABLE"
    }

    def __init__(self, lst, i, loggers, run_once=False):
        """
        Initialises the task process and runs forever
        :param lst:
        :param i:
        :param loggers:
        :return:
        """
        host = lst[i]
        client = Client(host.url)
        retry_code_regexp = re.compile(r"too many ([0-9]+) error responses")
        network_err_regexp = re.compile(r"\[Errno [0-9]+\](.*?)'")

        max_retry = str(Config.get('CHECK_CONN_MAX_RETRY'))

        while True:

            host.response_code = False
            host.response_time = False
            host.body = False

            try:
                # Acceptable Response Codes
                response = client.get()
                host.response_code = client.get_response_code()
                host.response_time = client.get_response_time_in_ms(response)
                host.retry_count = str(client.get_try_count())

                rc = str(host.response_code)
                host.response_code_msg = self.response_codes[rc]
                host.body = client.get_response_body()

            except ConnectionError as e:
                # Network errors
                err = network_err_regexp.findall(str(e.message))

                if len(err) > 0:
                        host.response_code_msg = self.network_errors[err[
                            0].strip()]
                else:
                    if 'ReadTimeoutError' in str(e.message):
                        host.response_code_msg = \
                            self.network_errors['ReadTimeoutError']
                    elif 'SSLError' in str(e.message):
                        host.response_code_msg = \
                            self.network_errors['CertificateError']

                host.retry_count = max_retry

            except RetryError as e:
                # Max limit reached
                msg = str(e.message)

                host.response_code = int(retry_code_regexp.findall(msg)[0])
                host.response_time = None
                rc = str(host.response_code)
                host.retry_count = max_retry
                host.response_code_msg = self.response_codes[rc]

            lst[i] = host

            loggers['monitor'].info(str(host.extra()), extra=host.extra())

            if not run_once:
                time.sleep(Config.get('CHECK_INTERVAL'))
            else:
                break

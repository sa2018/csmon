#!/usr/bin/env python
import unittest
from csmon.utils.client import Client
from requests import Response
from requests.exceptions import RetryError,ConnectionError

class TestClient(unittest.TestCase):

    def test_missing_url(self):
        with self.assertRaises(ValueError):
            Client()

    def test_get(self):
        client = Client('https://www.google.com')
        client.get()
        self.assertTrue(isinstance(client.response, Response))

    def test_get_content(self):
        client = Client('https://www.google.com')
        client.get()

        # Response Time
        self.assertTrue(isinstance(client.get_response_time_in_ms(
            client.response),str))
        self.assertTrue((client.get_response_time_in_ms(
            client.response).isdigit()))

        self.assertTrue(isinstance(client.get_response_body(),str))
        self.assertEqual(client.get_response_code(), 200)

        self.assertEqual(client.get_try_count(),1)

    def test_get_retry_err(self):

        with self.assertRaises(RetryError):
            client = Client('http://httpstat.us/500')
            client.get()

    def test_get_net_err(self):

        with self.assertRaises(ConnectionError):
            client = Client('http://nonexisting.nonexisting.org/')
            client.get()


if __name__ == '__main__':
    unittest.main()

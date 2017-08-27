#!/usr/bin/env python
import unittest
from csmon.healthcheck.task import Task
from csmon.healthcheck.host import Host
from csmon.utils.config import Config

import ast

import logging
from testfixtures import LogCapture

class TestTask(unittest.TestCase):

    def test_missing_url(self):
        with self.assertRaises(TypeError):
            Task()

    def test_logging(self):

        lst = [Host('https://www.google.com','<title>Google</title>')]
        i=0

        with LogCapture() as l:


            mon_logger = logging.getLogger('monitor')

            loggers = {'monitor':mon_logger}
            task =  Task(lst, i, loggers, True)

            lines = str(l).split("\n")
            message = ast.literal_eval(lines[-1:][0].strip())
            self.assertEqual(message['url'],"https://www.google.com")
            self.assertEqual(message['retry_count'],"1")
            self.assertTrue(message['finished_ts'].isdigit())
            self.assertTrue(message['response_time_ms'].isdigit())
            self.assertEqual(message['status_check'],'GREEN')

    def test_net_err(self):
        lst = [Host('https://www.googl.com','<title>Google</title>')]
        i=0

        with LogCapture() as l:

            mon_logger = logging.getLogger('monitor')

            loggers = {'monitor':mon_logger}
            task =  Task(lst, i, loggers, True)

            lines = str(l).split("\n")
            message = ast.literal_eval(lines[-1:][0].strip())
            self.assertEqual(message['url'],"https://www.googl.com")
            self.assertEqual(message['retry_count'],"3")
            self.assertTrue(message['finished_ts'].isdigit())
            self.assertEqual(message['response_time_ms'],False)
            self.assertEqual(message['status_check'],'NET_SSL_CERT')

    def test_retry_err(self):
        lst = [Host('http://httpstat.us/500','<title>Google</title>')]
        i=0

        with LogCapture() as l:

            mon_logger = logging.getLogger('monitor')

            loggers = {'monitor':mon_logger}
            task =  Task(lst, i, loggers, True)
            lines = str(l).split("\n")
            message = ast.literal_eval(lines[-1:][0].strip())
            self.assertEqual(message['url'],"http://httpstat.us/500")
            self.assertEqual(message['retry_count'],"3")
            self.assertTrue(message['finished_ts'].isdigit())
            self.assertEqual(message['response_time_ms'],None)
            self.assertEqual(message['status_check'],'500')

    def test_network_err(self):
        lst = [Host('http://wwww.ybookki.com.tr','<title>Google</title>')]
        i=0

        with LogCapture() as l:

            mon_logger = logging.getLogger('monitor')

            loggers = {'monitor':mon_logger}
            task =  Task(lst, i, loggers, True)
            lines = str(l).split("\n")
            message = ast.literal_eval(lines[-1:][0].strip())
            self.assertEqual(message['url'],"http://wwww.ybookki.com.tr")
            self.assertEqual(message['retry_count'],"3")
            self.assertTrue(message['finished_ts'].isdigit())
            self.assertEqual(message['response_time_ms'],False)
            self.assertTrue(message['status_check'] in ['NET_DNS','None'])

    def test_route_err(self):
        lst = [Host('http://www.google.com:81','<title>Google</title>')]
        i=0

        with LogCapture() as l:
            Config.set('CHECK_CONN_TIMEOUT',1)
            mon_logger = logging.getLogger('monitor')

            loggers = {'monitor':mon_logger}
            task =  Task(lst, i, loggers, True)
            lines = str(l).split("\n")
            message = ast.literal_eval(lines[-1:][0].strip())
            self.assertEqual(message['url'],"http://www.google.com:81")
            self.assertEqual(message['retry_count'],"3")
            self.assertTrue(message['finished_ts'].isdigit())
            self.assertEqual(message['response_time_ms'],False)
            self.assertTrue(message['status_check'] in ['NET_UNREACHABLE','NET_ROUTE'])


if __name__ == '__main__':
    unittest.main()



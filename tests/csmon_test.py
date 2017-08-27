#!/usr/bin/env python
import unittest
from csmon.csmon import CSMon
from csmon.utils.config import Config
from argparse import Namespace
import os

class TestCSMon(unittest.TestCase):

    def test_args_config(self):
        args = Namespace()

        args.monitor_log = './csmon-2-monitor.log'
        args.system_log = './csmon-2-system.log'
        args.back_off = 0.10
        args.timeout = 5
        args.interval = 6
        args.retry_count = 3
        args.urls = ['http://www.google.com!!!title']
        args.url_file = None

        csmon = CSMon(args)

        for key in csmon.config_arg_mapping:
            config_key = csmon.config_arg_mapping[key]
            self.assertEqual(Config.get(config_key),getattr(args,key))



    def test_loggers(self):
        args = Namespace()
        args.urls = ['http://www.google.com!!!title']
        args.url_file = None
        csmon = CSMon(args)
        self.assertEqual(len(csmon.loggers),2)


    def test_file(self):
        args = Namespace()
        args.urls = None
        with open('tmp.txt','w') as fp:
            fp.write('http://www.google.com!!!title')

        args.url_file = 'tmp.txt'
        csmon = CSMon(args)

        self.assertEqual(len(csmon._CSMon__urls),1)


if __name__ == '__main__':

    unittest.main()

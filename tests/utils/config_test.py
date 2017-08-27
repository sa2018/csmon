#!/usr/bin/env python
import unittest
from csmon.utils.config import Config


class TestConfig(unittest.TestCase):

    def test_set(self):
        value = Config.set('CHECK_INTERVAL',50)
        self.assertEqual(value, Config.get('CHECK_INTERVAL'))
        with self.assertRaises(NameError):
            Config.set('ABC', 50)

    def test_get(self):
        self.assertEqual(0.10, Config.get('CHECK_BACK_OFF_FACTOR'))
        with self.assertRaises(NameError):
            Config.get('ABC')


    def test__not_found(self):
        pass

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
import unittest
from csmon.utils.validation import Validation
from argparse import ArgumentTypeError
import os


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.files = []

    def tearDown(self):
        for filename in self.files:
            os.unlink(filename)

    def test_instance(self):
        with self.assertRaises(TypeError):
            Validation.instance("A", list, True)

        self.assertFalse(Validation.instance("A", list, False))
        self.assertTrue(Validation.instance([], list, False))

    def test___argtype_check(self):
        with self.assertRaises(ArgumentTypeError):
            Validation._Validation__argtype_check(
                value=10,
                validators=[lambda x: False],
                error="Error")

        result = Validation._Validation__argtype_check(
            value=10,
            validators=[lambda x: True],
            error="Error")

        self.assertTrue(result)

    def test___is(self):
        self.assertTrue(Validation._Validation__is(10, int))
        self.assertFalse(Validation._Validation__is("A", int))

    def test___file_(self):
        # Does not exists
        self.assertFalse(Validation._Validation__file_('/tmp/.12345', os.R_OK))
        self.assertFalse(Validation._Validation__file_('/root/.test', os.W_OK))

        # Exists doable
        file_name = '.UNIT_TEST_FILE'
        open(file_name, 'a').close()
        self.files.append(file_name)

        os.chmod(file_name, 0444)
        self.assertTrue(Validation._Validation__file_(file_name, os.R_OK))

        os.chmod(file_name, 0222)
        self.assertTrue(Validation._Validation__file_(file_name, os.W_OK))

        # Exists not doable
        os.chmod(file_name, 0444)
        self.assertFalse(Validation._Validation__file_(file_name, os.W_OK))

        os.chmod(file_name, 0222)
        self.assertFalse(Validation._Validation__file_(file_name, os.R_OK))

    def test_file_not_empty(self):
        file_name = '.UNIT_TEST_EMPTY'
        open(file_name, 'w').close()
        self.files.append(file_name)
        self.assertFalse(Validation.file_not_empty(file_name))
        a = open(file_name, 'a')
        a.write("content")
        a.close()
        self.assertTrue(Validation.file_not_empty(file_name))
        with self.assertRaises(TypeError):
            Validation.file_not_empty(None)

    def test_file_exists_and_not_empty(self):
        # Not exists
        self.assertFalse(Validation.file_exists_and_not_empty("/tmp/.12345"))
        # Exists Empty
        file_name = '.UNIT_TEST_EMPTY_2'
        open(file_name, 'w').close()
        self.files.append(file_name)
        self.assertFalse(Validation.file_exists_and_not_empty(file_name))
        # Exists not empty
        a = open(file_name, 'a')
        a.write("content")
        a.close()
        self.assertTrue(Validation.file_exists_and_not_empty(file_name))

        with self.assertRaises(TypeError):
            Validation.file_exists_and_not_empty(None)

    def test_file_read(self):
        file_name = '.UNIT_TEST_READ'
        open(file_name, 'a').close()
        self.files.append(file_name)
        # readable
        os.chmod(file_name, 0444)
        self.assertTrue(Validation.file_read(file_name))
        # not readable
        os.chmod(file_name, 0222)
        self.assertFalse(Validation.file_read(file_name))

        with self.assertRaises(TypeError):
            Validation.file_read(None)

    def test_file_write(self):
        file_name = '.UNIT_TEST_WRITE'
        open(file_name, 'a').close()
        self.files.append(file_name)
        # writable
        os.chmod(file_name, 0222)
        self.assertTrue(Validation.file_write(file_name))
        # not writable
        os.chmod(file_name, 0444)
        self.assertFalse(Validation.file_write(file_name))

        with self.assertRaises(TypeError):
            Validation.file_write(None)

    def test_argtype_file_exists_and_not_empty(self):
        file_name = '.UNIT_TEST_ARG_NEMPTY'
        a = open(file_name, 'a')
        a.write("content")
        a.close()
        self.files.append(file_name)

        self.assertEqual(file_name,
                         Validation.argtype_file_exists_and_not_empty(
                             file_name))

        open(file_name, 'w').close()
        with self.assertRaises(ArgumentTypeError):
            Validation.argtype_file_exists_and_not_empty(file_name)

        with self.assertRaises(TypeError):
            Validation.argtype_file_exists_and_not_empty(None)

    def test_is_number(self):
        self.assertTrue(Validation.is_number(1))
        self.assertTrue(Validation.is_number("100"))
        self.assertTrue(Validation.is_number(10.00))
        self.assertTrue(Validation.is_number(-1))
        self.assertTrue(Validation.is_number("100.05"))
        self.assertFalse(Validation.is_number("ABC"))
        self.assertFalse(Validation.is_number("100,05"))

    def test_is_integer(self):
        self.assertTrue(Validation.is_integer(1))
        self.assertFalse(Validation.is_integer("10.5"))

    def test_is_unsigned(self):
        self.assertTrue(Validation.is_unsigned(0.01))
        self.assertTrue(Validation.is_unsigned(1))
        self.assertTrue(Validation.is_unsigned(0.00))
        self.assertFalse(Validation.is_unsigned(-0.01))
        self.assertFalse(Validation.is_unsigned(-0.01))

    def test_is_positive(self):
        self.assertTrue(Validation.is_positive(0.01))
        self.assertFalse(Validation.is_positive(0.00))

    def test_argtype_positive_integer(self):
        with self.assertRaises(ArgumentTypeError):
            Validation.argtype_positive_integer(0)

        self.assertEqual(1, Validation.argtype_positive_integer(1))

    def test_argtype_unsigned_integer(self):
        with self.assertRaises(ArgumentTypeError):
            Validation.argtype_unsigned_integer(-1)

        self.assertEqual(1, Validation.argtype_unsigned_integer(1))

    def test_argtype_positive_float(self):
        with self.assertRaises(ArgumentTypeError):
            Validation.argtype_positive_float(0.00)

        self.assertEqual(1.1, Validation.argtype_positive_float(1.1))

    def test_argtype_unsigned_float(self):
        with self.assertRaises(ArgumentTypeError):
            Validation.argtype_unsigned_float(-0.01)

        self.assertEqual(0.01, Validation.argtype_unsigned_float(0.01))

    def test_url(self):
        self.assertTrue(Validation.url('http://www.google.com'))
        self.assertTrue(Validation.url('http://www.google.com:8080'))
        self.assertTrue(Validation.url('https://www.google.com:443/path/'))

        self.assertFalse(Validation.url('www.google.com'))
        self.assertFalse(Validation.url('gopher://www.google.com:8080'))


if __name__ == '__main__':
    unittest.main()

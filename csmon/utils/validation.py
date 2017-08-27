from argparse import ArgumentTypeError
import os


class Validation(object):

    @staticmethod
    def instance(obj, instance, exception=False):
        if not isinstance(obj, instance):
            if exception:
                raise TypeError("%s expected given %s" % (instance, type(obj)))

            return False

        return True

    @staticmethod
    def __argtype_check(value, validators, error):

        for item in validators:
            if not item(value):
                raise ArgumentTypeError(error)

        return True

    @staticmethod
    def __is(value, type_f):
        try:
            type_f(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def is_number(value):
        return Validation.__is(value, complex)

    @staticmethod
    def is_integer(value):
        return Validation.__is(value, int)

    @staticmethod
    def is_unsigned(value):
        return True if float(value) >= 0 else False

    @staticmethod
    def is_positive(value):
        return True if float(value) >= 0.01 else False

    @staticmethod
    def __file_(file_name, ok_status):
        return True if os.path.isfile(file_name) and \
                       os.access(file_name, ok_status) else False

    @staticmethod
    def file_not_empty(file_name):
        Validation.instance(file_name, str)

        return os.stat(file_name).st_size > 0

    @staticmethod
    def file_exists_and_not_empty(file_name):
        Validation.instance(file_name, str)

        return True if Validation.file_read(file_name) \
                       and Validation.file_not_empty(file_name) else False

    @staticmethod
    def file_read(file_name):
        Validation.instance(file_name, str)
        return Validation.__file_(file_name, os.R_OK)

    @staticmethod
    def file_write(file_name):
        Validation.instance(file_name, str)
        return Validation.__file_(file_name, os.W_OK)

    @staticmethod
    def argtype_file_exists_and_not_empty(file_name):
        Validation.instance(file_name, str)

        Validation.__argtype_check(
            value=file_name,
            validators=[Validation.file_exists_and_not_empty],
            error="File %s does not exists/readable or empty"
                  % file_name)
        return file_name

    @staticmethod
    def argtype_positive_integer(value):
        Validation.__argtype_check(
            value=value,
            validators=[Validation.is_integer, Validation.is_positive],
            error="%s is an invalid positive integer value, expected n > 1"
                  % value)

        return int(value)

    @staticmethod
    def argtype_unsigned_integer(value):
        Validation.__argtype_check(
            value=value,
            validators=[Validation.is_integer, Validation.is_unsigned],
            error="%s is an invalid unsigned integer value, expected n >= 0"
                  % value)

        return int(value)

    @staticmethod
    def argtype_positive_float(value):
        Validation.__argtype_check(
            value=value,
            validators=[Validation.is_number, Validation.is_positive],
            error="%s is an invalid positive float value, expected n > 0.01"
                  % value)

        return float(value)

    @staticmethod
    def argtype_unsigned_float(value):

        Validation.__argtype_check(
            value=value,
            validators=[Validation.is_number, Validation.__is_unsigned],
            error="%s is an invalid unsigned float value, expected n >= 0.00"
                  % value)

        return float(value)

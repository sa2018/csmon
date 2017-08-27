from validation import Validation
import logging


class Config(object):

    __configs = {
        'CHECK_INTERVAL': 10,
        'CHECK_CONN_TIMEOUT': 5,
        'CHECK_CONN_MAX_RETRY': 3,
        'CHECK_BACK_OFF_FACTOR': 0.10,
        'LOG_SYS_LEVEL': logging.INFO,
        'LOG_SYS_FILE': './csmon-system.log',
        'LOG_SYS_FORMAT': '[%(asctime)s] %(levelname)s [%(module)s.%(funcName)'
                          's:%(lineno)d] %(message)s',
        'LOG_SYS_TZ_FORMAT': '%m-%d-%Y %H:%M:%S.%f',
        'LOG_MON_FILE': './csmon-monitor.log',
        'LOG_MON_LEVEL': logging.INFO,
        'LOG_MON_TZ_FORMAT': '%s',
        'LOG_MON_FORMAT': '%(asctime)s,%(status_check)s,%(url)s,'
                          '%(response_time_ms)s',
    }

    @staticmethod
    def get(name):

        Config.__not_found(name)

        return Config.__configs[name]

    @staticmethod
    def set(name, value):

        Config.__not_found(name)

        Validation.instance(value, type(Config.__configs[name]), False)

        Config.__configs[name] = value

        return value

    @staticmethod
    def __not_found(name):

        if name not in Config.__configs.keys():
            raise NameError('%s configuration parameter not found' % name)

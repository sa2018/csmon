from multiprocessing import Process, Manager
from utils.validation import Validation
from healthcheck.task import Task
from healthcheck.host import Host
from utils.config import Config
import logging
import signal
import sys


class CSMon(object):
    """
    Process management
    """

    def __init__(self, args):
        """
        Initialises CSMon
        :param args:
        :return:
        """
        self.__args = args
        self.loggers = {}

        # Assign configuration from arguments
        self.config_arg_mapping = {
            'monitor_log': 'LOG_MON_FILE',
            'back_off': 'CHECK_BACK_OFF_FACTOR',
            'system_log': 'LOG_SYS_FILE',
            'timeout': 'CHECK_CONN_TIMEOUT',
            'interval': 'CHECK_INTERVAL',
            'retry_count': 'CHECK_CONN_MAX_RETRY',
        }

        args_as_dict = vars(args)

        for k in args_as_dict.keys():
            if k in self.config_arg_mapping.keys():
                Config.set(self.config_arg_mapping[k], args_as_dict[k])

        self.__init_loggers()
        self.__urls = self.__load_urls()

        manager = Manager()

        self.__health_checks = manager.list()

    def start(self):
        """
         Spawns processes to monitor URLs, each URL is one process.
        :return:
        """

        def signal_handler(r_signal, frame):
            """
            Internal Method for handling keyboard interrupt
            :param r_signal:
            :param frame:
            :return:
            """
            self.loggers['system'].info("Received signal %s" % r_signal)
            exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        for i in xrange(len(self.__urls)):
            self.__health_checks.append(Host(*self.__urls[i]))
            p = Process(target=Task, args=(self.__health_checks, i,
                                           self.loggers))
            p.start()

        while True:
            pass

    def __init_loggers(self):
        """
        Initialises monitor, system and monitor stdout loggers
        :return:
        """
        loggers = ['monitor', 'system']

        for logger in loggers:
            self.__init_logger(logger)

        self.__init_logger('monitor', 'stdout')

    def __init_logger(self, logger, handler="file"):
        """
        Initialises a single logger
        :return:
        """
        config_key = '_'.join(['LOG', logger.upper()[:3]])

        if not self.loggers.get(logger, None):
            self.loggers[logger] = logging.getLogger("csmon_%s" % logger)
            self.loggers[logger].setLevel(Config.get('_'.join([config_key,
                                                               'LEVEL'])))

        if handler == "file":
            logger_handler = logging.FileHandler(Config.get('_'.join(
                [config_key, 'FILE'])))
        else:
            logger_handler = logging.StreamHandler(stream=sys.stdout)

        logger_handler.setLevel(Config.get('_'.join([config_key, 'LEVEL'])))

        logger_formatter = logging.Formatter(Config.get('_'.join([config_key,
                                                                  'FORMAT'])
                                                        ),
                                             Config.get('_'.join([config_key,
                                                                  'TZ_FORMAT'])
                                                        ))
        logger_handler.setFormatter(logger_formatter)

        self.loggers[logger].addHandler(logger_handler)

    def __load_urls(self):
        """
        Loads url from a file or args
        :return:
        """
        urls = []

        if self.__args.url_file:
            urls_raw = self.__load_urls_from_file()
        else:
            urls_raw = self.__args.urls

        for url in urls_raw:
            if Validation.url(url):
                url = url.split('!!!')
                if len(url) == 2:
                    urls.append(tuple(url))
                else:
                    self.loggers['system'].error("URL %s has no content tag, "
                                                 "skipping" % url)
            else:
                self.loggers['system'].error("URL %s is invalid, skipping"
                                             % url)

        return urls

    def __load_urls_from_file(self):
        """
        Reads files with URLs
        :return:
        """
        filename = self.__args.url_file
        urls = []

        if Validation.file_read(filename):
            with open(filename, "r") as fp:
                urls = [i.strip() for i in fp.readlines()]

        return urls

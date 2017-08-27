# -*- coding: utf-8 -*-
import re
from datetime import datetime


class Host(object):

    def __init__(self, url, contain_text):

        self.__url = url
        self.__contain_text_raw = contain_text
        self.__contain_text = re.compile(contain_text)
        self.__last_result = {
                              'response_code': None,
                              'retry_count': None,
                              'response_time': None,
                              'body': None,
                              'response_code_msg': None,
                              'completed': None,
                              'prev_response_time': None,
                              }

    def __str__(self):
        return "<Item URL='%s' Search='%s' Status='%s' RetryCount='%s' " \
               "ResponseTime='%s' isSuccess='%s'>" % \
               (self.__url, self.__contain_text, self.__last_result['status'],
                self.__last_result['retry_count'],
                self.__last_result['response_time'],
                True if "Green" in self.status else False)

    def extra(self):
        return {'url': self.url, 'status_check': self.status,
                'response_time_ms': self.response_time,
                'retry_count': self.retry_count,
                'finished_ts': self.completed}

    @property
    def short_url(self):
        return self.__url if len(self.__url) <= 20 else self.__url[:18]+'..'

    @property
    def url(self):
        return self.__url

    @property
    def status(self):
        if self.response_code == 200:

            if len(self.__contain_text.findall(self.body)) > 0:
                if  self.__last_result['prev_response_time']:
                    diff = int(self.__last_result['prev_response_time']) - \
                           int(self.__last_result['response_time'])

                    if diff < 0:
                        diff = -diff
                        threshold = diff * 100 / int(self.__last_result[
                            'prev_response_time'])
                        if threshold > 10:
                            return 'ORANGE'

                    return 'GREEN'
                else:
                    return 'GREEN'
            else:
                return '200'
        else:
            # Network issue
            if self.response_code is False:
                return "%s" % self.response_code_msg
            else:
                return "%i" % self.response_code

    @property
    def retry_count(self):
        return self.__last_result['retry_count']

    @retry_count.setter
    def retry_count(self, retry_count):
        self.__last_result['retry_count'] = retry_count

    @property
    def response_time(self):
        return self.__last_result['response_time']

    @property
    def completed(self):
        return self.__last_result['completed']

    @response_time.setter
    def response_time(self, response_time):
        if self.__last_result['response_time']:
            prev =  self.__last_result['response_time']
            self.__last_result['prev_response_time'] = prev

        self.__last_result['response_time'] = response_time
        self.__last_result['completed'] = datetime.utcnow().strftime("%s")

    @property
    def response_code(self):
        return self.__last_result['response_code']

    @response_code.setter
    def response_code(self, response_code):
        self.__last_result['response_code'] = response_code

    @property
    def response_code_msg(self):
        return self.__last_result['response_code_msg']

    @response_code_msg.setter
    def response_code_msg(self, response_code_msg):
        self.__last_result['response_code_msg'] = response_code_msg

    @property
    def body(self):
        return self.__last_result['body']

    @body.setter
    def body(self, body):
        self.__last_result['body'] = body

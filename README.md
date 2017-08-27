# csmon [![Build Status](https://travis-ci.org/sa2018/csmon.svg?branch=master)](https://travis-ci.org/sa2018/csmon) [![Code Climate](https://codeclimate.com/github/sa2018/csmon/badges/gpa.svg)](https://codeclimate.com/github/sa2018/csmon) [![Test Coverage](https://codeclimate.com/github/sa2018/csmon/badges/coverage.svg)](https://codeclimate.com/github/sa2018/csmon/coverage) [![Issue Count](https://codeclimate.com/github/sa2018/csmon/badges/issue_count.svg)](https://codeclimate.com/github/sa2018/csmon) [![BCH compliance](https://bettercodehub.com/edge/badge/sa2018/csmon?branch=master)](https://bettercodehub.com/)

## Install

With [pip](https://pip.pypa.io/en/stable/installing/) installed, run

    $ pip install .

With setup.py

    $ python2.7 setup.py

## Usage
```
usage: cli.py [-h] [--urls [urls [urls ...]]] [--url-file filename]
              [--monitor-log FILE] [--system-log FILE] [--interval SECONDS]
              [--retry-count NUMBER] [--timeout SECONDS] [--back-off NUMBER]

CS Monitor Application

optional arguments:
  -h, --help            show this help message and exit

URL List:

      CSMon can load the URLs from arguments or from a file, either of
      them is *required*.

      URL format is : http(s)://domain.com[:Port]/!!!Regexp_or_String

      After http response received, it will check for the string or the regular
      expression inside the response content. Please escape the urls with quotes
      if you are providing URLs as arguments

  --urls [urls [urls ...]]
                        URLs to monitor
  --url-file filename
                        URLs from file to monitor

Connection options:
  --monitor-log FILE    [OPTIONAL] File to write monitor results.
                        [DEFAULT] ./csmon-monitor.log file
  --system-log FILE     [OPTIONAL] Output file to write system logs.
                        [DEFAULT] ./csmon-system.log file

Monitoring options:
  --interval SECONDS    [OPTIONAL] How many seconds to wait till
                        reschedule the next test for the each URL
                        [DEFAULT] 10 secs

Connection options:
  --retry-count NUMBER  [OPTIONAL] Max retry if service is unavailable
                        [DEFAULT] 3 times
  --timeout SECONDS     [OPTIONAL] Timeout for the connection
                        [DEFAULT] 5 seconds
  --back-off NUMBER     [OPTIONAL] A backoff factor to apply between
                        attempts after the second try.
                        {back-off} * (2 ^ ({num of total retries}-1))
                        If the number is 0.1, then it will sleep for
                        [0.0s,0.2s, 0.4s, ...] between retries
                        [DEFAULT] 0.10

```
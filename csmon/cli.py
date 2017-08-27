from argparse import ArgumentParser, RawTextHelpFormatter
from utils.validation import Validation
from utils.config import Config


def run():

    parser = ArgumentParser(description="CS Monitor Application",
                            formatter_class=RawTextHelpFormatter)

    # URL Input params
    arg_grp = parser.add_argument_group

    input_grp = arg_grp("URL List",
                        description="""
CSMon can load the URLs from arguments or from a file, either of
them is *required*.

URL format is : http(s)://domain.com[:Port]/!!!Regexp_or_String

After http response received, it will check for the string or the regular
expression inside the response content. Please escape the urls with quotes
if you are providing URLs as arguments""")

    input_grp_arg = input_grp.add_argument
    input_grp_arg("--urls",
                  metavar="urls",
                  type=str,
                  nargs="*",
                  help="\nURLs to monitor")

    input_grp_arg("--url-file",
                  metavar="filename",
                  type=Validation.argtype_file_exists_and_not_empty,
                  help="\nURLs from file to monitor")

    args = parser.parse_args()

    # Output params
    output_grp = arg_grp("Connection options")
    output_grp_arg = output_grp.add_argument

    output_grp_arg("--monitor-log",
                   metavar='FILE',
                   required=False,
                   default=Config.get('LOG_MON_FILE'),
                   type=str,
                   help="[OPTIONAL] Output file to write monitor results.\n"
                        "[DEFAULT] %s file\n" % Config.get('LOG_MON_FILE'))

    output_grp_arg("--system-log",
                   metavar='FILE',
                   required=False,
                   type=str,
                   default=Config.get('LOG_SYS_FILE'),
                   help="[OPTIONAL] Output file to write system logs.\n"
                        "[DEFAULT] %s file\n" % Config.get('LOG_SYS_FILE'))

    # Monitoring params
    mon_grp = arg_grp("Monitoring options")
    mon_grp_arg = mon_grp.add_argument
    mon_grp_arg("--interval",
                metavar='SECONDS',
                type=Validation.argtype_positive_integer,
                default=Config.get('CHECK_INTERVAL'),
                help="[OPTIONAL] How many seconds to wait till reschedule the "
                     "next test for the each URL\n"
                     "DEFAULT] %i seconds\n" % Config.get('CHECK_INTERVAL'))

    # HTTP Connection params
    http_grp = arg_grp("Connection options")
    http_grp_arg = http_grp.add_argument
    http_grp_arg("--retry-count",
                 metavar='NUMBER',
                 type=Validation.argtype_unsigned_integer,
                 default=Config.get('CHECK_CONN_MAX_RETRY'),
                 help="[OPTIONAL] Max retry count if service is unavailable"
                      "[DEFAULT] %i times" % Config.get(
                     'CHECK_CONN_MAX_RETRY'))

    http_grp_arg("--timeout",
                 metavar='SECONDS',
                 type=Validation.argtype_positive_float,
                 default=Config.get('CHECK_CONN_TIMEOUT'),
                 help="[OPTIONAL] Timeout for the connection\n"
                      "[DEFAULT] %i seconds" %
                      Config.get('CHECK_CONN_TIMEOUT'))

    http_grp_arg("--back-off",
                 metavar='NUMBER',
                 type=Validation.argtype_unsigned_float,
                 default=Config.get('CHECK_BACK_OFF_FACTOR'),
                 help="[OPTIONAL] A backoff factor to apply between attempts "
                      "after the second try.\n"
                      "{backoff factor}*(2 ^ ({number of total retries}-1))\n"
                      "If the number is 0.1, then it will sleep for "
                      "[0.0s,0.2s, 0.4s, ...] between retries\n"
                      "[DEFAULT] %.2f" % Config.get('CHECK_BACK_OFF_FACTOR'))

    # Extra validation
    urls = args.urls
    file_for_urls = args.url_file

    if (not urls and not file_for_urls) or (urls and file_for_urls):
        parser.error('--urls or --url-file required')

if __name__ == '__main__':
    run()

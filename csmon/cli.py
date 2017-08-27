from argparse import ArgumentParser, RawTextHelpFormatter
from utils.validation import Validation


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
                   default=None,
                   type=str,
                   help="[OPTIONAL] Output file to write monitor results.\n"
                        "[DEFAULT] %s file\n" % None)

    output_grp_arg("--system-log",
                   metavar='FILE',
                   required=False,
                   type=str,
                   default=None,
                   help="[OPTIONAL] Output file to write system logs.\n"
                        "[DEFAULT] %s file\n" % None)

    # Extra validation
    urls = args.urls
    file_for_urls = args.url_file

    if (not urls and not file_for_urls) or (urls and file_for_urls):
        parser.error('--urls or --url-file required')

if __name__ == '__main__':
    run()

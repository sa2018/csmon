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

    # Extra validation
    urls = args.urls
    file_for_urls = args.url_file

    if (not urls and not file_for_urls) or (urls and file_for_urls):
        parser.error('--urls or --url-file required')

if __name__ == '__main__':
    run()

#!/usr/bin/env python3
"""Script to parse through a sitemap and take screenshots of the pages."""

__author__ = "Javier Ayala"
__version__ = "0.1.0"
__license__ = "MIT"

from SiteCrawlerQuick import SiteCrawlerQuick
import argparse
import itertools
import os
from time import sleep

from jinja2 import Environment, FileSystemLoader
from logzero import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import url_utils
from SitemapReader import SitemapReader
from SiteCrawler import SiteCrawler

height_adjustment = 0
# Set num_urls_to_grab to a number if you want to limit the number of pages to parse
num_urls_to_grab = None
# sitemap_url = os.environ.get("SITEMAP_URL")


def main(args):
    """ Main entry point of the app """
    logger.info("Welcome!")
    # logger.info(args)

    sitemap = SitemapReader(args.sitemap_url)

    if args.num_urls_to_grab:
        urls_to_grab = dict(
            itertools.islice(sitemap.get_sitemap_data().items(), args.num_urls_to_grab)
        )
    else:
        urls_to_grab = sitemap.get_sitemap_data()

    if args.quick:
        import asyncio
        import aiohttp
        from SiteCrawlerQuick import SiteCrawlerQuick

        site_crawler = SiteCrawlerQuick(urls_to_grab)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(site_crawler.crawl_sites())
        print("Results:\n\n")
        for result in site_crawler.results:
            for url, status in result.items():
                print("%s : %s" % (url, status))
    else:
        site_crawler = SiteCrawler(
            urls=urls_to_grab,
            output_dir=args.output_dir,
            template_dir=args.template_dir,
            page_template=args.page_template,
            quick_mode=args.quick,
        )

    # # Get the page template for Jinja
    # page_template = jinja_env.get_template("page.html.j2")
    # for url, lastmod in urls_to_grab.items():
    #     # Dictionary containing the path of the resource separated into a parent/child
    #     res_path = url_utils.get_path_components(url_utils.get_path_from_url(url))
    #     # Set where to output data
    #     output_dir = "output%s" % res_path["parent"]
    #     # Create the output directory if needed
    #     url_utils.make_output_dir(output_dir)

    #     # Information about what we are doing
    #     # print(
    #     #     "URL: %s, Last Modified: %s, Parent: %s, Child: %s, OutputDir: %s"
    #     #     % (url, lastmod, res_path["parent"], res_path["child"], output_dir)
    #     # )

    #     try:
    #         # Setup Firefox as headless
    #         fireFoxOptions = Options()
    #         fireFoxOptions.headless = True
    #         # Create an actual Firefox instance, then get the url
    #         driver = webdriver.Firefox(options=fireFoxOptions)
    #         driver.get(url)
    #         scroll_height = driver.execute_script(
    #             "return document.documentElement.scrollHeight"
    #         )
    #         S = lambda X: driver.execute_script(
    #             "return document.body.parentNode.scroll" + X
    #         )
    #         # driver.set_window_size(S("Width"), S("Height") + height_adjustment)
    #         driver.set_window_size(S("Width"), scroll_height + height_adjustment)
    #         driver.find_element_by_tag_name("body").screenshot(
    #             "%s%s.png" % (output_dir, res_path["child"])
    #         )
    #     finally:
    #         try:
    #             driver.close()
    #         except:
    #             pass

    #     # Output to HTML
    #     output_html_path = "%s%s.html" % (output_dir, res_path["child"])
    #     page_template.stream(
    #         output_dir=res_path["parent"],
    #         child=res_path["child"],
    #         lastmod=lastmod,
    #         url=url,
    #     ).dump(output_html_path)
    #     print("Created %s" % output_html_path)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    description = (
        "Crawls a Sitemap and creates snapshots of each page.  Alternatively,\n"
        "if used with the 'quick' option will simply crawl without saving \n"
        "snapshots. This can be useful to warm the cache on a site.\n\n"
        "You can also set the Sitemap URL by setting the 'SITEMAP_URL'\n"
        "environment variable."
    )
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Required positional argument
    # parser.add_argument("sitemap_url", default=os.environ.get("SITEMAP_URL"), help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument(
        "-s",
        "--sitemap-url",
        action="store",
        default=os.environ.get("SITEMAP_URL"),
        help="URL to the Sitemap to parse",
    )

    parser.add_argument(
        "-n",
        "--num-urls-to-grab",
        action="store",
        default=None,
        type=int,
        help="Set this to a number that you want to use to limit the number of URLs to crawl",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        action="store",
        default=None,
        type=str,
        help="Path to the directory to store snapshots",
    )

    parser.add_argument(
        "-p",
        "--page-template",
        action="store",
        default=None,
        type=str,
        help="Name of the Jinja2 template for snapshots",
    )

    parser.add_argument(
        "-t",
        "--template-dir",
        action="store",
        default=None,
        type=str,
        help="Path to the directory where the Jinja2 templates are stored",
    )

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        "-q",
        "--quick",
        action="store_true",
        help="Perform a quick crawl, without saving snapshots",
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    logger.info(args)
    main(args)

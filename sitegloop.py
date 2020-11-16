#!/usr/bin/env python3
"""Script to parse through a sitemap and take screenshots of the pages.

.. code-block:: console

    usage: sitegloop.py [-h] [-m {quick,screenshot}] [-s SITEMAP_URL] [-tl TARGET_LOC] [-ts TARGET_SCHEME] [-n NUM_URLS_TO_GRAB] [-v] [--version] [-o OUTPUT_DIR] [-p PAGE_TEMPLATE] [-t TEMPLATE_DIR]
                        [-ql QUICK_LIMIT]

    Crawls a Sitemap and performs a quick asynchronous crawl of the resources contained
    within the sitemap.  This can be useful for warming the site's cache.  Alternatively,
    if used with the 'screenshot' option will simply crawl synchronously, saving
    snapshots of each page.

    You can also set the Sitemap URL by setting the 'SITEMAP_URL'
    environment variable.

    optional arguments:
    -h, --help            show this help message and exit

    Universal Options:
    These are universal options that can be used whether doing a normal/screenshot crawl or a quick crawl.

    -m {quick,screenshot}, --mode {quick,screenshot}
                            Which mode you want to invoke, a 'quick' async crawl or a synchronous 'screenshot' capture
    -s SITEMAP_URL, --sitemap-url SITEMAP_URL
                            URL to the Sitemap to parse
    -tl TARGET_LOC, --target-loc TARGET_LOC
                            Target Location to use when crawling, if you want to crawl a different host from that defined within the sitemap.
    -ts TARGET_SCHEME, --target-scheme TARGET_SCHEME
                            Target Scheme (http or https) to use when crawling, if you want to use a different scheme when crawling then what is defined within the sitemap.
    -n NUM_URLS_TO_GRAB, --num-urls-to-grab NUM_URLS_TO_GRAB
                            Set this to a number that you want to use to limit the number of URLs to crawl
    -v, --verbose         Verbosity (-v, -vv, etc)
    --version             show program's version number and exit

    Crawl w/ Screenshots:
    These options pertain to crawls in which each page is loaded, then a screenshot is created from a headless browser.

    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                            Path to the directory to store snapshots
    -p PAGE_TEMPLATE, --page-template PAGE_TEMPLATE
                            Name of the Jinja2 template for snapshots
    -t TEMPLATE_DIR, --template-dir TEMPLATE_DIR
                            Path to the directory where the Jinja2 templates are stored

    Quick Crawl w/o Screenshots:
    These options pertain to quick crawls in which screenshots are not created, and the links are visited asynchronously.

    -ql QUICK_LIMIT, --quick-limit QUICK_LIMIT
                            Maximum number of connections to allow at once (requires '-q') Default is 100.

"""

__author__ = "Javier Ayala"
__version__ = "0.2.3"
__license__ = "MIT"

import argparse
import asyncio
import itertools
import os
import sys
from time import sleep

from colored import attr, bg, fg
from logzero import logger

import url_utils
from SiteCrawler import SiteCrawler
from SiteCrawlerQuick import SiteCrawlerQuick
from SitemapReaderQuick import SitemapReaderQuick

height_adjustment = 0
# Set num_urls_to_grab to a number if you want to limit the number of pages to parse
num_urls_to_grab = None


def find_log_level(lvl=0):
    """Parse and return a valid logging level from the verbose setting.

    Parameters
    ----------
    lvl : int, optional
        verbose level, by default 0

    Returns
    -------
    int
        Python Logging Level (see: https://docs.python.org/3/library/logging.html#logging-levels)
    """
    if lvl == 0:
        return 50
    elif lvl == 1:
        return 40
    elif lvl == 2:
        return 30
    elif lvl == 3:
        return 20
    else:
        return 10


def main(args):
    """Run Sitegloop on behalf of the user.

    Parameters
    ----------
    args : ArgumentParser Namespace
        object containing the attributes passed via the command line
    """
    if args.sitemap_url is None:
        logger.error(
            "NO SITEMAP DEFINED! Must use '-s' option or SITEMAP_URL Environment Variable."
        )
        sys.exit(1)
    sitemaploop = asyncio.get_event_loop()
    sitemap = SitemapReaderQuick(
        args.sitemap_url,
        conn_limit=args.quick_limit,
        verbosity=find_log_level(args.verbose),
    )
    sitemaploop.run_until_complete(sitemap.parse_sitemap())

    if args.num_urls_to_grab:
        urls_to_grab = dict(
            itertools.islice(sitemap.get_sitemap_data().items(), args.num_urls_to_grab)
        )
    else:
        urls_to_grab = sitemap.get_sitemap_data()

    if args.mode == "quick":
        import aiohttp

        from SiteCrawlerQuick import SiteCrawlerQuick

        site_crawler = SiteCrawlerQuick(
            urls=urls_to_grab,
            target_loc=args.target_loc,
            target_scheme=args.target_scheme,
            conn_limit=args.quick_limit,
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(site_crawler.crawl_sites())

        print(
            "\n\n%s%s%s Results of Site Crawl: %s\n"
            % (attr("bold"), fg("white"), bg("green"), attr("reset"))
        )
        for result in site_crawler.results:
            for url, status in result.items():
                if int(status) < 300:
                    status_color = fg("green")
                elif int(status) < 400:
                    status_color = fg("yellow")
                else:
                    status_color = "%s%s" % (attr("bold"), fg("red"))
                print("%s : %s%s%s" % (url, status_color, status, attr("reset")))
    else:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options

        site_crawler = SiteCrawler(
            urls=urls_to_grab,
            output_dir=args.output_dir,
            template_dir=args.template_dir,
            page_template=args.page_template,
            mode=args.mode,
        )


if __name__ == "__main__":
    """ This is executed when run from the command line """
    description = (
        "Crawls a Sitemap and performs a quick asynchronous crawl of the resources contained \n"
        "within the sitemap.  This can be useful for warming the site's cache.  Alternatively,\n"
        "if used with the 'screenshot' option will simply crawl synchronously, saving \n"
        "snapshots of each page.\n\n"
        "You can also set the Sitemap URL by setting the 'SITEMAP_URL'\n"
        "environment variable."
    )
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    universal_group = parser.add_argument_group(
        "Universal Options",
        "These are universal options that can be used whether doing a normal/screenshot crawl or a quick crawl.",
    )

    universal_group.add_argument(
        "-m",
        "--mode",
        action="store",
        choices=["quick", "screenshot"],
        default="quick",
        help="Which mode you want to invoke, a 'quick' async crawl or a synchronous 'screenshot' capture",
    )

    # Optional argument flag which defaults to False
    universal_group.add_argument(
        "-s",
        "--sitemap-url",
        action="store",
        default=os.environ.get("SITEMAP_URL"),
        help="URL to the Sitemap to parse",
    )

    universal_group.add_argument(
        "-tl",
        "--target-loc",
        action="store",
        default=None,
        help=(
            "Target Location to use when crawling, if you want to crawl a different \n"
            "host from that defined within the sitemap."
        ),
    )

    universal_group.add_argument(
        "-ts",
        "--target-scheme",
        action="store",
        default=None,
        help=(
            "Target Scheme (http or https) to use when crawling, if you want to use a \n"
            "different scheme when crawling then what is defined within the sitemap."
        ),
    )

    universal_group.add_argument(
        "-n",
        "--num-urls-to-grab",
        action="store",
        default=None,
        type=int,
        help="Set this to a number that you want to use to limit the number of URLs to crawl",
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    universal_group.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)",
    )

    # Specify output of "--version"
    universal_group.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    screenshot_group = parser.add_argument_group(
        "Crawl w/ Screenshots",
        "These options pertain to crawls in which each page is loaded, then a screenshot is created from a headless browser.",
    )

    screenshot_group.add_argument(
        "-o",
        "--output-dir",
        action="store",
        default=None,
        type=str,
        help="Path to the directory to store snapshots",
    )

    screenshot_group.add_argument(
        "-p",
        "--page-template",
        action="store",
        default=None,
        type=str,
        help="Name of the Jinja2 template for snapshots",
    )

    screenshot_group.add_argument(
        "-t",
        "--template-dir",
        action="store",
        default=None,
        type=str,
        help="Path to the directory where the Jinja2 templates are stored",
    )

    quick_group = parser.add_argument_group(
        "Quick Crawl w/o Screenshots",
        "These options pertain to quick crawls in which screenshots are not created, and the links are visited asynchronously.",
    )

    quick_group.add_argument(
        "-ql",
        "--quick-limit",
        type=int,
        action="store",
        default=100,
        help="Maximum number of connections to allow at once (requires '-q') Default is 100.",
    )

    args = parser.parse_args()
    main(args)

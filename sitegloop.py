#!/usr/bin/env python3
"""Script to parse through a sitemap and take screenshots of the pages."""

__author__ = "Javier Ayala"
__version__ = "0.1.1"
__license__ = "MIT"

import argparse
import itertools
import os
import sys
from time import sleep

from logzero import logger

import url_utils
from SiteCrawler import SiteCrawler
from SiteCrawlerQuick import SiteCrawlerQuick
from SitemapReader import SitemapReader

height_adjustment = 0
# Set num_urls_to_grab to a number if you want to limit the number of pages to parse
num_urls_to_grab = None


def main(args):
    """Entry point of the app."""
    if args.sitemap_url is None:
        logger.error(
            "NO SITEMAP DEFINED! Must use '-s' option or SITEMAP_URL Environment Variable."
        )
        sys.exit(1)
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

        site_crawler = SiteCrawlerQuick(urls=urls_to_grab, conn_limit=args.quick_limit)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(site_crawler.crawl_sites())
        logger.info("Results:\n\n")
        for result in site_crawler.results:
            for url, status in result.items():
                logger.info("%s : %s" % (url, status))
    else:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options

        site_crawler = SiteCrawler(
            urls=urls_to_grab,
            output_dir=args.output_dir,
            template_dir=args.template_dir,
            page_template=args.page_template,
            quick_mode=args.quick,
        )


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

    universal_group = parser.add_argument_group(
        "Universal Options",
        "These are universal options that can be used whether doing a normal/screenshot crawl or a quick crawl.",
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
        "-n",
        "--num-urls-to-grab",
        action="store",
        default=None,
        type=int,
        help="Set this to a number that you want to use to limit the number of URLs to crawl",
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    universal_group.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
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
        "-q",
        "--quick",
        action="store_true",
        help="Perform a quick crawl, without saving snapshots",
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

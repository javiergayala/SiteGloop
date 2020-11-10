"""Crawl a list of URLs asynchronously."""
import asyncio

import aiohttp
from logzero import logger
from progress.spinner import Spinner


class SiteCrawlerQuick:
    def __init__(self, urls=None, conn_limit=None, verbosity=50):
        """Initialize the Quick Site Crawler.

        Parameters
        ----------
        urls : list
            list of URLs to crawl
        conn_limit : int
            maximum number of connections to use (default: 100)
        verbosity : int, optional
            verbosity setting, by default 50 (see: https://docs.python.org/3/library/logging.html#logging-levels)
        """
        self.verbosity = verbosity
        self.urls = [] if urls is None else urls
        self.conn_limit = 100 if conn_limit is None else conn_limit
        self.results = None
        self.spinner = None

    def _logger(self, level=None, msg=None, spin=False):
        """Log message or iterate the spinner.

        Parameters
        ----------
        level : str, optional
            log level to use, by default None (choices: debug, info, warning, error, critical)
        msg : str, optional
            message to log, by default None
        spin : bool, optional
            True to spin the spinner, by default False
        """
        if level is None and spin and self.verbosity >= 30:
            self.spinner.next()
        elif level == "debug" and msg is not None:
            logger.debug("%s" % msg)
        elif level == "info" and msg is not None:
            logger.info("%s" % msg)
        elif level == "warning" and msg is not None:
            logger.warning("%s" % msg)
        elif level == "error" and msg is not None:
            logger.error("%s" % msg)
        elif level == "critical" and msg is not None:
            logger.critical("%s" % msg)
        return

    def get_urls(self):
        """Getter for the provided URLs.

        Returns
        -------
        list
            list of urls provided to crawl
        """
        return self.urls

    async def request(self, url):
        """Asynchronously request a URL from a web server.

        Parameters
        ----------
        url : str
            URL to be requested

        Returns
        -------
        dict
            URL and it's response code from the crawler
        """
        connector = aiohttp.TCPConnector(limit=self.conn_limit)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as resp:
                self._logger(level="debug", msg="Starting session for %s" % url)
                self._logger(spin=True)
                await resp.text(encoding="utf-8")
                return {url: resp.status}

    async def crawl_sites(self):
        """Asynchronously crawl a list of URLs.

        Returns
        -------
        list
            list of dictionaries containing URLs crawled and their response codes
        """
        if self.verbosity >= 30:
            self.spinner = Spinner(" Crawling ")
        self.results = await asyncio.gather(*[self.request(u) for u in self.urls])
        return self.results

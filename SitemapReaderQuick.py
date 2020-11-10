"""Read and parse through a sitemap and return the data."""
import asyncio
import logging
import xml

import aiohttp
import logzero
from bs4 import BeautifulSoup
from colored import attr, bg, fg
from logzero import logger
from progress.spinner import Spinner

from SitegloopErrors import NoConnectorError, SitemapUrlError


class SitemapReaderQuick:
    """Quick Sitemap reader class."""

    def __init__(self, sitemap_url, sitemap_data={}, conn_limit=None, verbosity=50):
        """Initialize the Sitemap reader.

        Parameters
        ----------
        sitemap_url : str
            URL to the sitemap
        sitemap_data : dict, optional
            data from a parsed sitemap, by default {}
        conn_limit : int, optional
            maximum number of connections to use (default: 100)
        verbosity : int, optional
            verbosity setting, by default 50 (see: https://docs.python.org/3/library/logging.html#logging-levels)
        """
        self.verbosity = verbosity
        logzero.loglevel(self.verbosity)
        self.sitemap_url = sitemap_url
        self.sitemap_data = sitemap_data
        self.conn_limit = 100 if conn_limit is None else conn_limit
        self.connector = None
        self.queue = asyncio.Queue()
        self.queue.put_nowait(self.sitemap_url)
        self.spinner = None
        self.found_sitemap_urls = [self.sitemap_url]

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

    def get_sitemap_url(self):
        """Getter for the sitemap_url.

        Returns
        -------
        str
            URL to the sitemap
        """
        return self.sitemap_url

    def get_sitemap_data(self):
        """Getter for the parsed sitemap data.

        Returns
        -------
        dict
            provides the "url" and "lastmod" data from the sitemap
        """
        return self.sitemap_data

    async def _retrieve_sitemap(self, session=None, sitemap_url=None, parser="xml"):
        if session is None:
            raise NoConnectorError
        if sitemap_url is None:
            raise SitemapUrlError
        async with session.get(sitemap_url) as resp:
            self._logger(level="debug", msg="Starting session for %s" % sitemap_url)
            self._logger(spin=True)
            return await resp.text(encoding="utf-8")

    async def parse_sitemap(self):
        """Process the data within the sitemap."""
        print(
            "\n%s Beginning to parse sitemap(s)... %s\n" % (attr("bold"), attr("reset"))
        )
        if self.verbosity >= 30:
            self.spinner = Spinner(" Loading ")
        self.connector = aiohttp.TCPConnector(limit=self.conn_limit)
        async with aiohttp.ClientSession(connector=self.connector) as session:
            self.sitemap_data = {}
            _soups = None
            while not self.queue.empty():
                _soups = await asyncio.gather(
                    *[
                        self._retrieve_sitemap(session, self.queue.get_nowait(), "xml")
                        # for u in self.found_sitemap_urls
                    ]
                )

                for _soupraw in _soups:
                    _soup = BeautifulSoup(_soupraw, "xml")
                    if _soup.sitemapindex is not None:
                        for _sitemap in _soup.sitemapindex.find_all("sitemap"):
                            _sitemap_url = _sitemap.loc.text
                            if _sitemap_url not in self.found_sitemap_urls:
                                self.found_sitemap_urls.append(_sitemap_url)
                                self.queue.put_nowait(_sitemap_url)
                                self._logger(
                                    level="debug",
                                    msg="New Sitemap Found: %s" % _sitemap_url,
                                )
                                self._logger(spin=True)
                            self._logger(
                                level="debug",
                                msg="Found sitemaps: %s" % self.queue.qsize(),
                            )
                            self._logger(spin=True)
                    if _soup.urlset is not None:
                        self._logger(
                            level="debug",
                            msg="Sitemap Data Entries: %s" % len(self.sitemap_data),
                        )
                        self._logger(spin=True)
                        _urlset = _soup.urlset.find_all("url")
                        for _url in _urlset:
                            _url_text = _url.findNext("loc").text
                            if _url_text not in self.sitemap_data:
                                _lastmod = (
                                    _url.lastmod.text if _url.lastmod else "UNKNOWN"
                                )
                                self.sitemap_data[_url.findNext("loc").text] = _lastmod
                                self._logger(level="debug", msg="Added %s" % _url_text)
                                self._logger(spin=True)
                            elif _url_text in self.sitemap_data:
                                self._logger(
                                    level="debug",
                                    msg="Duplicate found. Sitemaps found: %s"
                                    % self.queue.qsize(),
                                )
                                self._logger(spin=True)
                self.queue.task_done()
        self._logger(level="info", msg="Sitemap Reading Complete!")
        print(
            "\n\n%s%s%s Sitemap Reading Complete! %s\n"
            % (attr("bold"), fg("white"), bg("green"), attr("reset"))
        )
        return

    def print_stats(self):
        """Print out the number of URLs found in the sitemaps."""
        self._logger(
            level="info",
            msg="Number of URLs found in sitemaps: %s" % len(self.sitemap_data),
        )
        return

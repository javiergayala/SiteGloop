"""Crawl a list of URLs asynchronously."""
import asyncio

import aiohttp
from logzero import logger


class SiteCrawlerQuick:
    def __init__(self, urls=None, conn_limit=None):
        """Initialize the Quick Site Crawler.

        Parameters
        ----------
        urls : list
            list of URLs to crawl
        conn_limit : int
            maximum number of connections to use (default: 100)
        """
        self.urls = [] if urls is None else urls
        self.conn_limit = 100 if conn_limit is None else conn_limit
        self.results = None

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
                logger.debug("Starting session for %s" % url)
                await resp.text(encoding="utf-8")
                return {url: resp.status}

    async def crawl_sites(self):
        """Asynchronously crawl a list of URLs.

        Returns
        -------
        list
            list of dictionaries containing URLs crawled and their response codes
        """
        self.results = await asyncio.gather(*[self.request(u) for u in self.urls])
        return self.results

    def __str__():
        return "urls: " + urls

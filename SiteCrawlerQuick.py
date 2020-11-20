"""Crawl a list of URLs asynchronously."""
import asyncio
import urllib.parse

import aiohttp
from logzero import logger
from progress.spinner import Spinner

from SiteGloopUtils import SiteGloopLogger as GloopLog
from SiteGloopUtils import is_fqdn
from SiteGloopErrors import InvalidHostname


class SiteCrawlerQuick:
    """Crawl the site in an asynchronous fashion.

    Args:
        urls (list): A list of URLs to crawl.
        target_loc (:obj:`str`, *optional*): The location (hostname) to target if different from
            that defined in the sitemap.
        target_scheme (:obj:`str`, *optional*): The scheme (http/https) to use if different from that defined in
            the sitemap.
        conn_limit (:obj:`int`, *optional*): The maximum number of connections to use.
        verbosity (:obj:`int`, *optional*): The verbosity setting for output.
            (see: https://docs.python.org/3/library/logging.html#logging-levels)

    Attributes:
        urls (list): A list of URLs to crawl.
        target_loc (str): The location (hostname) to target if different from
            that defined in the sitemap.
        target_scheme (str): The scheme (http/https) to use if different from that defined in
            the sitemap.
        conn_limit (int): The maximum number of connections to use.
        verbosity (int): The verbosity setting for output.
            (see: https://docs.python.org/3/library/logging.html#logging-levels)

    """

    def __init__(
        self,
        urls=None,
        target_loc=None,
        target_scheme=None,
        conn_limit=None,
        verbosity=50,
    ):
        """Initialize the Quick Site Crawler.

        Args:
            urls (list):
                list of URLs to crawl
            target_loc (str, *optional):
                location (hostname) to target if different (default: None)
            target_scheme (str, *optional*):
                scheme to use on target if different from source (default: same as resource within the sitemap)
            conn_limit (int, *optional*):
                maximum number of connections to use (default: 100)
            verbosity (int, *optional*):
                verbosity setting, by default 50 (see: https://docs.python.org/3/library/logging.html#logging-levels)
        """
        self.verbosity = verbosity
        self.glooplog = GloopLog(verbosity=self.verbosity)
        self.glooplog.logit(
            level="debug",
            msg=(
                "target_loc    : %s\ntarget_scheme : %s\n" % (target_scheme, target_loc)
            ),
        )
        if target_loc is not None and not is_fqdn(target_loc):
            raise InvalidHostname(
                "Value of 'target_loc' (%s) is not a valid FQDN!" % target_loc
            )
        else:
            self.target_loc = target_loc
        self.target_scheme = target_scheme
        if self.target_loc and isinstance(urls, dict):
            self.urls = self.change_url_location(urls)
        else:
            self.urls = urls
        self.conn_limit = 100 if conn_limit is None else conn_limit
        self.results = None
        if self.verbosity >= 30:
            self.glooplog.spinner = Spinner("\n Crawling ")

    def change_url_location(self, urls=[]) -> list:
        """Change the netloc in the URL to something user-defined.

        Args:
            urls (list, *optional*):
                URLs that we want to change, by default []

        Returns:
            list: A list of dictionaries containing modified URLs as their keys.

        """
        changed_urls = {}
        self.glooplog.spinner = Spinner("Replacing URLs with %s : " % self.target_loc)
        for url, lastmod in urls.items():
            _parsed = urllib.parse.urlparse(url)
            if self.target_scheme:
                _scheme = self.target_scheme
            else:
                _scheme = _parsed.scheme
            _path = _parsed.path
            _params = _parsed.params
            _query = _parsed.query
            _fragment = _parsed.fragment
            _new_url = "%s://%s%s%s%s%s" % (
                _scheme,
                self.target_loc,
                _path,
                _params,
                _query,
                _fragment,
            )
            changed_urls[_new_url] = lastmod
            self.glooplog.logit(spin=True)
        return changed_urls

    def get_urls(self) -> list:
        """Getter for the provided URLs.

        Returns
            list: a list of dictionaries with URLs to crawl as their keys.

        """
        return self.urls

    async def request(self, url, session) -> dict:
        """Asynchronously request a URL from a web server.

        Args:
            url (str): the URL to be requested by the crawler.
            session (obj): an aiohttp Client Session

        Returns:
            dict: The URL as the key, and it's response code as the value from the crawler.

        """
        async with session.get(url) as resp:
            self.glooplog.logit(level="debug", msg="Starting session for %s" % url)
            self.glooplog.logit(spin=True)
            await resp.text(encoding="utf-8")
            return {url: resp.status}

    async def bound_request(self, sem, url, session):
        """Bind the request to the semaphore pool.

        Args:
            sem (obj): a sempahore object to manage an internal counter for the connection limit
            url (str): the URL to be requested by the crawler
            session (obj): an aiohttp Client Session
        """
        async with sem:
            await self.request(url, session)

    async def crawl_sites(self) -> list:
        """Asynchronously crawl a list of URLs.

        Return:
            list: A list of dictionaries containing URLs crawled as their key and their response codes
                as the value:

            Example::

                [
                    {
                        'https://www.javierayala.com/page1': 200
                    },
                    {
                        'https://www.javierayala.com/page2': 200
                    }
                ]

        """
        self.results = []
        sem = asyncio.Semaphore(self.conn_limit)
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                self.results.append(
                    asyncio.create_task(self.bound_request(sem, url, session))
                )
            await asyncio.gather(*self.results)
        return self.results

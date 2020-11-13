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
    def __init__(
        self,
        urls=None,
        target_loc=None,
        target_scheme=None,
        conn_limit=None,
        verbosity=50,
    ):
        """Initialize the Quick Site Crawler.

        Parameters
        ----------
        urls : list
            list of URLs to crawl
        target_loc : str, optional
            location (hostname) to target if different (default: None)
        target_scheme : str, optional
            scheme to use on target if different from source (default: same as resource within the sitemap)
        conn_limit : int
            maximum number of connections to use (default: 100)
        verbosity : int, optional
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

        Parameters
        ----------
        urls : list, optional
            URLs that we want to change, by default []

        Returns
        -------
        list
            modified URLs
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
        -------
        list
            list of urls provided to crawl
        """
        return self.urls

    async def request(self, url) -> dict:
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
                self.glooplog.logit(level="debug", msg="Starting session for %s" % url)
                self.glooplog.logit(spin=True)
                await resp.text(encoding="utf-8")
                return {url: resp.status}

    async def crawl_sites(self) -> list:
        """Asynchronously crawl a list of URLs.

        Returns
        -------
        list
            list of dictionaries containing URLs crawled and their response codes
        """
        self.results = await asyncio.gather(*[self.request(u) for u in self.urls])
        return self.results

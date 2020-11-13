"""Read and parse through a sitemap and return the data."""
import requests
import xml
from bs4 import BeautifulSoup
from logzero import logger
from SiteGloopErrors import SitemapUrlError


class SitemapReader:
    """Sitemap reader class.

    Args:
        sitemap_url (str): URL to the primary sitemap
        sitemap_data (:obj:`dict`, optional): Data from a parsed sitemap, by default ``{}``

    Attributes:
        sitemap_url (str): URL to the primary sitemap
        sitemap_data (dict): Data from a parsed sitemap, by default ``{}``

    """

    def __init__(self, sitemap_url, sitemap_data={}) -> None:
        """Initialize the Sitemap reader.

        Args:
            sitemap_url (str):
                URL to the sitemap
            sitemap_data (:obj:`dict`, optional):
                data from a parsed sitemap, by default ``{}``

        """
        self.sitemap_url = sitemap_url
        self.sitemap_data = sitemap_data
        self.found_sitemap_urls = [self.sitemap_url]
        self.parse_sitemap()

    def get_sitemap_url(self) -> str:
        """Getter for the sitemap_url.

        Returns:
            str: URL to the sitemap

        """
        return self.sitemap_url

    def get_sitemap_data(self) -> dict:
        """Getter for the parsed sitemap data.

        Returns:
            dict: The URL crawled is the key, and the "lastmod" data taken
                from the sitemap is the value
        """
        return self.sitemap_data

    def _retrieve_sitemap(self, sitemap_url=None, parser="xml"):
        if sitemap_url is None:
            raise SitemapUrlError
        r = requests.get(sitemap_url, parser)
        return r.text

    def parse_sitemap(self) -> bool:
        """Process the data within the sitemap.

        Returns:
            bool: True if sitemap was successfully parsed

        """
        self.sitemap_data = {}
        while len(self.found_sitemap_urls) > 0:
            _soup = None
            _current_url = self.found_sitemap_urls.pop()
            logger.debug("Current URL: %s" % _current_url)
            _soup = BeautifulSoup(self._retrieve_sitemap(_current_url, "xml"))

            if _soup.sitemapindex is not None:
                for _sitemap in _soup.sitemapindex.find_all("sitemap"):
                    _sitemap_url = _sitemap.loc.text
                    if _sitemap_url not in self.found_sitemap_urls:
                        self.found_sitemap_urls.append(_sitemap.loc.text)
                        logger.debug("New Sitemap Found: %s" % _sitemap.loc.text)
                    logger.debug("Found sitemaps: %s" % len(self.found_sitemap_urls))
            if _soup.urlset is not None:
                _urlset = _soup.urlset.find_all("url")
                for _url in _urlset:
                    _lastmod = _url.lastmod.text if _url.lastmod else "UNKNOWN"
                    self.sitemap_data[_url.findNext("loc").text] = _lastmod
        return True

    def print_stats(self) -> None:
        """Print the number of URLs found in the sitemaps."""
        logger.debug("Number of URLs found in sitemaps: %s" % len(self.sitemap_data))
        return

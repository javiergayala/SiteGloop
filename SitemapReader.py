"""Read and parse through a sitemap and return the data."""
import requests
from bs4 import BeautifulSoup


class SitemapReader:
    """Sitemap reader class."""

    def __init__(self, sitemap_url, sitemap_data={}):
        """Initialize the Sitemap reader.

        Parameters
        ----------
        sitemap_url : str
            URL to the sitemap
        sitemap_data : dict, optional
            data from a parsed sitemap, by default {}
        """
        self.sitemap_url = sitemap_url
        self.sitemap_data = sitemap_data
        self.parse_sitemap()

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

    def _retrieve_sitemap(self):
        r = requests.get(self.sitemap_url)
        return r.text

    def parse_sitemap(self):
        """Process the data within the sitemap."""
        self.sitemap_data = {}
        soup = BeautifulSoup(self._retrieve_sitemap(), features="html.parser")
        sitemapTags = soup.find_all("url")
        for sitemap in sitemapTags:
            self.sitemap_data[sitemap.findNext("loc").text] = sitemap.findNext(
                "lastmod"
            ).text
        return

    def __str__(self):
        """Representation of the class data."""
        return (
            "sitemap_url: "
            + self.sitemap_url
            + " , "
            + "sitemap_data: "
            + self.sitemap_data
        )

"""Error Exceptions for Sitegloop."""


class SitemapUrlError(Exception):
    """Exception raised when an error is encountered with the Sitemap URL."""

    def __init__(self, message="Error with Sitemap URL"):
        """Create the exception."""
        self.message = message


class NoConnectorError(Exception):
    """Exception raised when there is no aiohttp connector."""

    def __init__(self, message="No aiohttp Connector Established"):
        """Create the exception."""
        self.message = message

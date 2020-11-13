"""Error Exceptions for SiteGloop."""


class SitemapUrlError(Exception):
    """Exception raised when an error is encountered with the Sitemap URL.

    Args:
        message (str): Human readable string describing the exception

    Attributes:
        message (str): Human readable string describing the exception

    """

    def __init__(self, message="Error with Sitemap URL"):
        """Create the exception."""
        self.message = message


class NoConnectorError(Exception):
    """Exception raised when there is no aiohttp connector.

    Args:
        message (str): Human readable string describing the exception

    Attributes:
        message (str): Human readable string describing the exception

    """

    def __init__(self, message="No aiohttp Connector Established"):
        """Create the exception."""
        self.message = message


class InvalidHostname(Exception):
    """Exception raised when a provided hostname is not a FQDN.

    Args:
        message (str): Human readable string describing the exception

    Attributes:
        message (str): Human readable string describing the exception

    """

    def __init__(self, message="Provided hostname is not a FQDN."):
        """Create the exception."""
        self.message = message

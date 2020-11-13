"""Various utilities for use by SiteGloop."""
import re
import logzero
from logzero import logger


def is_fqdn(hostname: str) -> bool:
    """Check for a valid hostname.

    Parameters
    ----------
    hostname : str
        hostname to validate

    Returns
    -------
    bool
        True if it's a valid hostname
    """
    if not 1 < len(hostname) < 253:
        return False

    # Remove trailing dot
    if hostname[-1] == ".":
        hostname = hostname[0:-1]

    #  Split hostname into list of DNS labels
    labels = hostname.split(".")

    #  Define pattern of DNS label
    #  Can begin and end with a number or letter only
    #  Can contain hyphens, a-z, A-Z, 0-9
    #  1 - 63 chars allowed
    fqdn = re.compile(r"^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$", re.IGNORECASE)

    # Check that all labels match that pattern.
    return all(fqdn.match(label) for label in labels)


class SiteGloopLogger:
    """Logger for SiteGloop."""

    def __init__(self, verbosity=50, spinner=None):
        """Create the logger.

        Parameters
        ----------
        verbosity : int, optional
            logging level, by default 50
        spinner : [type], optional
            progress spinner to spin, by default None
        """
        self.verbosity = verbosity
        logzero.loglevel(self.verbosity)
        self.spinner = spinner

    def logit(self, level=None, msg=None, spin=False):
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
        if level is None and self.spinner and spin and self.verbosity >= 30:
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

"""Various utilities needed for sitemap parsing."""
import os.path
from urllib.parse import urlparse


def get_path_from_url(url):
    """Extract the path from a URL.

    Parameters
    ----------
    url : str
        URL for a resource

    Returns
    -------
    str
        path extracted from the URL
    """
    return urlparse(url).path


def get_path_components(path):
    """Separate the parent/child components from a path.

    Parameters
    ----------
    path : str
        path to process

    Returns
    -------
    dict
        dictionary containing the parent and child of the path
    """
    if len(path) > 1:
        c = os.path.split(path)[1]
        if len(c) == 0:
            c = "INDEX"
        return {
            "parent": os.path.join(os.path.split(path)[0], ""),
            "child": c,
        }
    else:
        p = os.path.split(path)[0]
        if len(p) == 0:
            p = "/"
        return {"parent": p, "child": "INDEX"}


def make_output_dir(path):
    """Create an output directory if none exists.

    Parameters
    ----------
    path : str
        path of the output directory to create
    """
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

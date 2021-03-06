# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from better import better_theme_path

sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------

project = "SiteGloop"
copyright = "2020, Javier Ayala"
author = "Javier Ayala"

# The full version, including alpha/beta/rc tags
release = "v0.2.4"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "recommonmark",
    "sphinxcontrib.programoutput",
    "sphinxcontrib.srclinks",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- srclink settings --------------------------------------------------------
srclink_project = "https://github.com/javiergayala/SiteGloop"
srclink_src_path = "docsrc/"
srclink_branch = "main"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# html_theme_path = [better_theme_path]
#
html_theme = "alabaster"
# html_theme = "better"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_logo = "../SiteGloop_25.png"

html_theme_options = {
    "logo": "../SiteGloop_25.png",
    "github_user": "javiergayala",
    "github_repo": "SiteGloop",
    "github_banner": True,
    "github_button": True,
    "show_related": True,
    "show_relbars": True,
}

# html_sidebars = {
#     "**": ["globaltoc.html", "relations.html", "searchbox.html", "srclinks.html"],
# }

html_sidebars = {
    "**": ["localtoc.html", "relations.html", "searchbox.html", "srclinks.html"],
    "index": ["globaltoc.html", "relations.html", "searchbox.html", "srclinks.html"],
}

# html_theme_options = {"inlinecss": "img.logo { width: 100%; }"}

html_short_title = "Home"


# -- Extension configuration -------------------------------------------------

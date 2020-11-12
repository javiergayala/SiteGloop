"""Crawl a site and optionally perform snapshots of the pages."""
import os

from jinja2 import Environment, FileSystemLoader
from logzero import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import url_utils


class SiteCrawler:
    """Crawl the site and save snapshots if instructed to."""

    def __init__(
        self,
        urls=None,
        output_dir=None,
        template_dir=None,
        page_template=None,
        mode=None,
    ):
        """Initialize the SiteCrawler class.

        Parameters
        ----------
        urls : list, optional
            list of URLs to crawl, by default []
        output_dir : str, optional
            directory to output snapshots, by default "output"
        template_dir : str, optional
            directory containing Jinja2 templates, by default "templates"
        page_template : str, optional
            name of the Jinja2 template to use for snapshots, by default "page.html.j2"
        mode : str, optional
            set to "quick" to use quick mode (no snapshots saved)
        """
        self.urls = [] if urls is None else urls
        self.output_dir = (
            "output/" if output_dir is None else os.path.join(output_dir, "")
        )
        logger.debug("self.output_dir: %s" % self.output_dir)
        self.template_dir = "templates" if template_dir is None else template_dir
        self.page_template = "page.html.j2" if page_template is None else page_template
        self.mode = "quick" if mode is None else mode
        # logger.debug("template_dir: %s" % self.template_dir)
        self.jinja_file_loader = FileSystemLoader(self.template_dir)
        # logger.debug("jinja_file_loader: %s" % self.jinja_file_loader)
        self.jinja_env = Environment(loader=self.jinja_file_loader)
        # logger.debug("jinja_env: %s" % self.jinja_env)
        self.jinja_template = self.jinja_env.get_template(self.page_template)
        if len(self.urls) > 0:
            self.crawl_site()

    def crawl_site(self):
        """Crawl the site and perform a snapshot."""
        for url, lastmod in self.urls.items():
            # Dictionary containing the path of the resource separated into a parent/child
            res_path = url_utils.get_path_components(url_utils.get_path_from_url(url))
            # Set where to output data
            _output_dir = os.path.normpath(
                "%s%s" % (self.output_dir, res_path["parent"])
            )
            logger.debug("_output_dir: %s" % _output_dir)
            # Create the output directory if needed
            url_utils.make_output_dir(_output_dir)

            try:
                # Setup Firefox as headless
                fireFoxOptions = Options()
                fireFoxOptions.headless = True
                # Create an actual Firefox instance, then get the url
                driver = webdriver.Firefox(options=fireFoxOptions)
                driver.get(url)
                scroll_height = driver.execute_script(
                    "return document.documentElement.scrollHeight"
                )
                S = lambda X: driver.execute_script(
                    "return document.body.parentNode.scroll" + X
                )
                driver.set_window_size(S("Width"), scroll_height)
                driver.find_element_by_tag_name("body").screenshot(
                    "%s%s.png" % (self.output_dir, res_path["child"])
                )
            finally:
                try:
                    driver.close()
                except Exception:
                    pass

            # Output to HTML
            output_html_path = "%s/%s.html" % (_output_dir, res_path["child"])
            self.jinja_template.stream(
                output_dir=res_path["parent"],
                child=res_path["child"],
                lastmod=lastmod,
                url=url,
            ).dump(output_html_path)
            logger.info("Created %s" % output_html_path)

    def get_urls(self) -> list:
        """Get URLs contained in the class.

        Returns
        -------
        list
            list of URLs
        """
        return self.urls

    def get_output_dir(self) -> str:
        """Get the name of the output directory.

        Returns
        -------
        str
            name of the output directory
        """
        return self.output_dir

    def get_template_dir(self) -> str:
        """Get the name of the directory containing the Jinja2 templates.

        Returns
        -------
        str
            name of the templates directory
        """
        return self.template_dir

    def get_page_template(self) -> str:
        """Get the name of the Jinja2 page template for snapshots

        Returns
        -------
        str
            name of the Jinja2 page template
        """
        return self.page_template

    def get_mode(self) -> str:
        """Get the setting of quick mode.

        Returns
        -------
        str
            whether quick mode is enabled
        """
        return self.mode

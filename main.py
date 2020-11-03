"""Script to parse through a sitemap and take screenshots of the pages."""
import itertools
import os
from time import sleep

from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import url_utils
from SitemapReader import SitemapReader

height_adjustment = 0
# Set num_urls_to_grab to a number if you want to limit the number of pages to parse
num_urls_to_grab = None
sitemap_url = os.environ.get("SITEMAP_URL")

# Setup Jinja2
jinja_file_loader = FileSystemLoader("templates")
jinja_env = Environment(loader=jinja_file_loader)

sitemap = SitemapReader(sitemap_url)

if num_urls_to_grab:
    urls_to_grab = dict(
        itertools.islice(sitemap.get_sitemap_data().items(), num_urls_to_grab)
    )
else:
    urls_to_grab = sitemap.get_sitemap_data()

# Get the page template for Jinja
page_template = jinja_env.get_template("page.html.j2")
for url, lastmod in urls_to_grab.items():
    # Dictionary containing the path of the resource separated into a parent/child
    res_path = url_utils.get_path_components(url_utils.get_path_from_url(url))
    # Set where to output data
    output_dir = "output%s" % res_path["parent"]
    # Create the output directory if needed
    url_utils.make_output_dir(output_dir)

    # Information about what we are doing
    # print(
    #     "URL: %s, Last Modified: %s, Parent: %s, Child: %s, OutputDir: %s"
    #     % (url, lastmod, res_path["parent"], res_path["child"], output_dir)
    # )

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
        # driver.set_window_size(S("Width"), S("Height") + height_adjustment)
        driver.set_window_size(S("Width"), scroll_height + height_adjustment)
        driver.find_element_by_tag_name("body").screenshot(
            "%s%s.png" % (output_dir, res_path["child"])
        )
    finally:
        try:
            driver.close()
        except:
            pass

    # Output to HTML
    output_html_path = "%s%s.html" % (output_dir, res_path["child"])
    page_template.stream(
        output_dir=res_path["parent"], child=res_path["child"], lastmod=lastmod, url=url
    ).dump(output_html_path)
    print("Created %s" % output_html_path)

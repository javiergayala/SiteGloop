<div style="text-align:center"><img src="SiteGloop_25.png" /></div>

# Site Gloop

## Description

Site Gloop is a script that I created to solve a couple of needs that I have pertaining to crawling websites:

- Crawl with a Snapshot
- Quick Crawl

### Crawl with a Snapshot

This allows you to crawl a list of URLs (taken from a `sitemap.xml` file), and it uses Selenium to take a screenshot of the loaded page. It then produces HTML files within the `output` directory by default containing the embedded image of the screenshot. Useful for seeing how a page looks at the time that it was crawled, though could still use some work/optimization.

### Quick Crawl

This allows you to asynchronously crawl a list of URLs (also taken from a `sitemap.xml` file), and returns the status codes that were returned. You may need to increase your `ulimit` setting if you encounter an error similar to `OSError: [Errno 24] Too many open files`. This method allows you to quickly request a list of URLs to pre-warm a cache, for example. Since the resulting page is not rendered or saved, it completes in a much faster timeframe.

### Name Inspiration

Since this script consumes a list of URLs with ravenous hunger, it brought to mind a character from a [Roald Dahl](https://en.wikipedia.org/wiki/Roald_Dahl) book that my son is currently reading: [Charlie and the Chocolate Factory](https://en.wikipedia.org/wiki/Charlie_and_the_Chocolate_Factory). The character of [Augustus Gloop](https://en.wikipedia.org/wiki/List_of_Charlie_and_the_Chocolate_Factory_characters#Augustus_Gloop) inspires visions of unadulterated consumption in my mind. What better namesake for a script, that left to it's own devices, would consume in a similar fashion?

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

### Help

```text
python sitegloop.py -h

usage: sitegloop.py [-h] [-m {quick,screenshot}] [-s SITEMAP_URL] [-tl TARGET_LOC]
                    [-ts TARGET_SCHEME] [-n NUM_URLS_TO_GRAB] [-v] [--version] [-o OUTPUT_DIR]
                    [-p PAGE_TEMPLATE] [-t TEMPLATE_DIR] [-ql QUICK_LIMIT]

Crawls a Sitemap and performs a quick asynchronous crawl of the resources contained
within the sitemap.  This can be useful for warming the site's cache.  Alternatively,
if used with the 'screenshot' option will simply crawl synchronously, saving
snapshots of each page.

You can also set the Sitemap URL by setting the 'SITEMAP_URL'
environment variable.

optional arguments:
  -h, --help            show this help message and exit

Universal Options:
  These are universal options that can be used whether doing a normal/screenshot crawl or a quick crawl.

  -m {quick,screenshot}, --mode {quick,screenshot}
                        Which mode you want to invoke, a 'quick' async crawl or a synchronous
                        'screenshot' capture
  -s SITEMAP_URL, --sitemap-url SITEMAP_URL
                        URL to the Sitemap to parse
  -tl TARGET_LOC, --target-loc TARGET_LOC
                        Target Location to use when crawling, if you want to crawl a different
                        host from that defined within the sitemap.
  -ts TARGET_SCHEME, --target-scheme TARGET_SCHEME
                        Target Scheme (http or https) to use when crawling, if you want to use
                        a different scheme when crawling then what is defined within the
                        sitemap.
  -n NUM_URLS_TO_GRAB, --num-urls-to-grab NUM_URLS_TO_GRAB
                        Set this to a number that you want to use to limit the number of URLs
                        to crawl
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show program's version number and exit

Crawl w/ Screenshots:
  These options pertain to crawls in which each page is loaded, then a screenshot is created from a headless browser.

  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Path to the directory to store snapshots
  -p PAGE_TEMPLATE, --page-template PAGE_TEMPLATE
                        Name of the Jinja2 template for snapshots
  -t TEMPLATE_DIR, --template-dir TEMPLATE_DIR
                        Path to the directory where the Jinja2 templates are stored

Quick Crawl w/o Screenshots:
  These options pertain to quick crawls in which screenshots are not created, and the links are visited asynchronously.

  -ql QUICK_LIMIT, --quick-limit QUICK_LIMIT
                        Maximum number of connections to allow at once (requires '-q') Default is 100.
```

### Normal Usage

```bash
python sitegloop.py -s https://www.javierayala.com/sitemap.xml
```

### Usage w/ Environment Variables

```bash
SITEMAP_URL=https://www.javierayala.com/sitemap.xml python sitegloop.py
```

### Usage w/ Screenshot Option

```bash
python sitegloop.py -m screenshot -s https://www.javierayala.com/sitemap.xml
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

Javier Ayala (javier dot g dot ayala at gmail dot com)

## License

[MIT](https://choosealicense.com/licenses/mit/)

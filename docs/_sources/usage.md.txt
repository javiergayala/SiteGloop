# Usage

## CLI

### Help

```
> python sitegloop.py -h

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

## CLI Examples

### Normal Usage

```bash
> python sitegloop.py -s https://www.javierayala.com/sitemap.xml
```

### Usage w/ Environment Variables

```bash
> SITEMAP_URL=https://www.javierayala.com/sitemap.xml python sitegloop.py
```

### Usage w/ Screenshot Option

```bash
> python sitegloop.py -m screenshot -s https://www.javierayala.com/sitemap.xml
```

## API

See [API](API/index)

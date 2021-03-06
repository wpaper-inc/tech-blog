#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Whitepaper Inc.'
SITENAME = 'Whitepaper Tech Blog'
SITEURL = 'https://www.wpaper-inc.com'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'Japanese'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('企業サイト', 'https://www.wpaper-inc.com'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

RELATIVE_URLS = True
PATH = 'content'
STATIC_PATHS  = ['site_images', 'images', 'extra/CNAME', 'extra/favicon.ico', 'extra/.gitignore']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}, 'extra/favicon.ico': {'path': 'favicon.ico'}, 'extra/.gitignore': {'path': 'extra/.gitignore'}}

THEME = "theme/pelican-clean-blog"
GOOGLE_ANALYTICS = "UA-122761088-2"
HEADER_COLOR = 'white'
HEADER_COVER = 'site_images/osaka-castle.jpg'
FAVICON = 'favicon.ico'
DISQUS_SITENAME = 'whitepaper-tech-blog'

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['render_math', 'sitemap']
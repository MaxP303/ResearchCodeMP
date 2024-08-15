# -*- coding: utf-8 -*-

# Scrapy settings for ARGUS project

BOT_NAME = 'ARGUS'

SPIDER_MODULES = ['ARGUS.spiders']
NEWSPIDER_MODULE = 'ARGUS.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency settings
CONCURRENT_REQUESTS = 48
REACTOR_THREADPOOL_MAXSIZE = 35

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 4
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# DNS settings
DNS_RESOLVER = 'scrapy.resolver.CachingThreadedResolver'
DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 1000
DNS_TIMEOUT = 30

# Access settings from external file
import configparser
config = configparser.RawConfigParser()
config.read(r".\bin\settings.txt")

maxsize_number = config.get('spider-settings', 'maxsize')
DOWNLOAD_MAXSIZE = int(maxsize_number) if int(maxsize_number) > 0 else 10000000

timeout_secs = config.get('spider-settings', 'timeout')
DOWNLOAD_TIMEOUT = int(timeout_secs)

CONCURRENT_ITEMS = 72
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 5

MEMUSAGE_ENABLE = True

LOG_STDOUT = False
LOG_LEVEL = "INFO"

# Default request headers
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
}

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    #'scrapy_proxies.RandomProxy': 100,
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Extensions
EXTENSIONS = {'scrapy.contrib.feedexport.FeedExporter': None}

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 120
AUTOTHROTTLE_TARGET_CONCURRENCY = 2
AUTOTHROTTLE_DEBUG = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

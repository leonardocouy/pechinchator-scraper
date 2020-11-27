# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from base64 import b64decode

load_dotenv()

BOT_NAME = 'pechinchator_scraper'

SPIDER_MODULES = ['pechinchator_scraper.spiders']
NEWSPIDER_MODULE = 'pechinchator_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 6

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_twitter.TwitterDownloaderMiddleware': 10,
}

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True

ITEM_PIPELINES = {
    'pechinchator_scraper.pipelines.thread_pipelines.SanitizeContentHTMLPipeline': 300,
    'pechinchator_scraper.pipelines.thread_pipelines.NormalizeThreadDatePipeline': 310,
    'pechinchator_scraper.pipelines.db_pipelines.FirestorePipeline': 500,
}

# Firestore Settings

GCS_PROJECT_ID = os.getenv("GCS_PROJECT_ID")
GCS_CREDENTIALS = b64decode(os.getenv("GCS_CREDENTIALS_BASE64"))
GCS_COLLECTION_NAME = os.getenv("GCS_COLLECTION_NAME")
ADRENALINE_LOGIN = os.getenv("ADRENALINE_LOGIN")
ADRENALINE_PASSWORD = os.getenv("ADRENALINE_PASSWORD")
SENTRY_DSN = os.getenv("SENTRY_DSN")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN_KEY = os.getenv("TWITTER_ACCESS_TOKEN_KEY")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

EXTENSIONS = {
    "scrapy_sentry.extensions.Errors":10,
}
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DawsonCollegeWebsite:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com'
    }



# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
import os.path
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'videos'])

#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: run_crawler.py
@time: 16/8/3  下午10:41
@desc: 
"""
import os
import sys
sys.path.append(os.getcwd())


os.system("scrapy crawl jediSpider")

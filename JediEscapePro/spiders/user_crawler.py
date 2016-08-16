#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: user_crawler.py
@time: 16/8/11  下午4:10
@desc: catch user information
"""
import time
import re
import random
import urllib2
import sys
sys.path.append("/Users/pattywgm/SelfProject/DouBanMovieProVenv/JediEscapePro")
from bs4 import BeautifulSoup
from JediEscapePro.pipelines import JediEscapeProPipeline
from JediEscapePro.settings import COOKIES, USER_AGENT_LIST

cookie = COOKIES[0]
str_ = ""
for key, value in cookie.iteritems():
    str_ += key + "=" + value + ";"
print str_.strip()


class UserInfoCrawler(object):

    def __init__(self, cql):
        self.cql = cql

    def get_user_info(self):
        for _ in self.cql.conn.find(skip=10662):
            url = _['cmt_user']
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', str_))
            opener.addheaders.append(('User-Agent', random.choice(USER_AGENT_LIST)))
            html = opener.open(url).read()
            time.sleep(random.choice([1, 2, 3]))
            soup = BeautifulSoup(html)
            try:
                div = soup.find("div", attrs={"class": 'user-info'})
                area = div.find("a")
                if area is not None:
                    area = area.text.strip()
                join_time = re.findall("(\d{4}-\d{2}-\d{2})", div.find("div", attrs={"class": 'pl'}).text)[0]
                nick_name = soup.find("title").text.strip()
                self.cql.insert_user({"url": url, "area": area, "join_time": join_time, "nick_name": nick_name})
            except Exception, e:
                print url
                print e.message, e.args
                print "=================================================="


if __name__ == "__main__":
    jd = JediEscapeProPipeline()
    user_crawl = UserInfoCrawler(jd)
    user_crawl.get_user_info()
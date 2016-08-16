#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: middlewares.py
@time: 16/8/4  下午5:19
@desc:
"""
import random
from JediEscapePro.settings import USER_AGENT_LIST
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        # random choice one user-agent
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
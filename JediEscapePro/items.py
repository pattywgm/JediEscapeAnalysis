# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JediEscapeProItem(scrapy.Item):
    cmt_id = scrapy.Field()       # id of movie comment, used as a primary key in database
    cmt_cont = scrapy.Field()     # comment content
    cmt_star = scrapy.Field()     # comment stars
    cmt_time = scrapy.Field()     # comment publish time
    cmt_user = scrapy.Field()     # comment poster url
    cmt_thumbs = scrapy.Field()   # comment thumbs up count


class UserItem(scrapy.Item):
    url = scrapy.Field()
    area = scrapy.Field()
    join_time = scrapy.Field()
    nick_name = scrapy.Field()

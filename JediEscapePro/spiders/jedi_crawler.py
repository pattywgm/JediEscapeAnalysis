#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: jedi_crawler.py
@time: 16/8/3  下午9:54
@desc: The crawler of jediEscapePro
"""
import random
from scrapy import Request, FormRequest
from scrapy.spiders import Spider
from JediEscapePro.items import JediEscapeProItem, UserItem
from JediEscapePro.pipelines import JediEscapeProPipeline
from JediEscapePro.settings import COOKIES

star_map = {
    "很差".decode("utf-8"): 1,
    "较差".decode("utf-8"): 2,
    "还行".decode("utf-8"): 3,
    "推荐".decode("utf-8"): 4,
    "力荐".decode("utf-8"): 5,
}

jd_ql = JediEscapeProPipeline()


class JediCrawler(Spider):
    name = "jediSpider"
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/24529353/comments?sort=new_score']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Content-Type": " application/x-www-form-urlencoded",
        "Referer": "http://www.zhihu.com/"
    }

    def start_requests(self):
        return [Request('https://www.douban.com/accounts/login',
                        cookies=random.choice(COOKIES),
                        callback=self.after_login,
                        headers=self.headers)]

    def post_login(self, response):
        # login in with form data
        self.log('Preparing login...')
        form_data = {
            'source': 'movie',
            'redir': "https://movie.douban.com/subject/24529353/comments?start=20",
            'form_email': '416131549@qq.com',
            'form_password': '1847815zjm',
            'remember': "on",
            'login': "登录".decode("utf-8")
        }
        try:
            captcha_id = response.xpath("//input[@name='captcha-id']/@value").extract()[0]
            form_data.setdefault("captcha-id", captcha_id)
            form_data.setdefault("captcha-solution", "basin")
        except Exception, e:
            self.log("None captcha img")
        return [FormRequest.from_response(response,
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.headers,
                                          formdata=form_data,
                                          callback=self.after_login,
                                          dont_filter=True)]

    def after_login(self, response):
        self.log('Already login')
        with open("1.html", 'w') as f:
            f.write(response.body)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        # parse the html and get item field
        self.log('A response from %s just arrived!' % response.url)
        users = list()
        for comment in response.xpath("//div[@class='comment-item']"):
            item = JediEscapeProItem()
            item['cmt_id'] = comment.xpath("./@data-cid").extract()[0]
            item['cmt_thumbs'] = comment.xpath(".//span[@class='comment-vote']/span/text()").extract()[0]
            if jd_ql.duplicate_filter(item['cmt_id'], item['cmt_thumbs']) is False:
                self.log("The comment of id: %s has been crawled, drop it or update it's thumbs up counts!" % item['cmt_id'])
                continue
            item['cmt_cont'] = comment.xpath(".//p/text()").extract()[0].strip()
            item['cmt_time'] = comment.re("\d{4}-\d{2}-\d{2}")[0]
            stars = comment.xpath(".//span[@class='comment-info']/span/@title").extract()
            if len(stars) == 0:
                item['cmt_star'] = 0
            else:
                item['cmt_star'] = star_map.get(stars[0])
            item['cmt_user'] = comment.xpath(".//span[@class='comment-info']/a/@href").extract()[0]
            users.append(item['cmt_user'])
            yield item

        for user_url in users:
            yield Request(user_url, headers=self.headers, callback=self.get_user_infos)

        self.log("Get next page...")
        for url in response.xpath("//a[@class='next']/@href").extract():
            yield Request('https://movie.douban.com/subject/24529353/comments'+url,
                          callback=self.parse, cookies=random.choice(COOKIES))

    def get_user_infos(self, response):
        self.log("Now get user information of %s"% response.url)
        user_item = UserItem()
        info = response.xpath("//div[@class='user-info']").extract()[0]
        user_item["area"] = info.xpath(".//a/text()").extract()[0]
        user_item["join_time"] = info.re("\d{4}-\d{2}-\d{2}")[0]
        nick_name = response.xpath("//div[@class='info']/h1/text()").extract()[0]
        nick_name = nick_name[nick_name.index('"')+1: nick_name.rindex('"')].strip()
        user_item["nick_name"] = nick_name
        user_item["url"] = response.url
        yield user_item

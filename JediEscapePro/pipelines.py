# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from pymongo import MongoClient


class JediEscapeProPipeline(object):
    """
    The database of jediescape(named jediDB) only contains one table (named comments).
    """

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.jediDB
        self.conn = self.db.comments
        self.conn_user = self.db.coral_users

    def insert(self, comment):
        try:
            if self.conn.find_one({"cmt_id": comment.get('cmt_id')}) is None:
                self.conn.insert(comment)
        except Exception, e:
            logging.debug("Insert comment error: %s", e.message)

    def insert_user(self, user):
        """
        user information
        :param user:
        :return:
        """
        try:
            if self.conn_user.find_one({"url": user.get("url")}) is None:
                self.conn_user.insert(user)
        except Exception, e:
            logging.debug("Insert user error: %s", e.message)

    def duplicate_filter(self, cmt_id, thumbs_up):
        """
        Filter duplicate entries
        :param cmt_id: comment id
        :param thumbs_up: comment thumbs counts
        :return:
        """
        if self.conn.find_one({"cmt_id": cmt_id}) is None:
            return True
        else:
            self.conn.update({"cmt_id": cmt_id}, {"$set": {"cmt_thumbs": thumbs_up}})
            return False

    def process_item(self, item, spider):
        item_obj = dict(item)
        if item_obj.get("nick_name") is None:
            self.insert(item_obj)
        else:
            self.insert_user(item_obj)
        return item
#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: stats_analysis.py
@time: 16/8/15  下午4:56
@desc: static data analysis
"""

import sys
import random
import numpy as np
from matplotlib import pyplot as plt
sys.path.append("/Users/pattywgm/SelfProject/DouBanMovieProVenv/JediEscapePro")
from JediEscapePro.pipelines import JediEscapeProPipeline


jd = JediEscapeProPipeline()

comments = list()
users = list()


def get_comments():
    for comment in jd.conn.find():
        try:
            star = comment['cmt_star']
            thumbs = comment['cmt_thumbs']
            cmt_date = comment['cmt_time']
            comments.append((star, thumbs, cmt_date))
        except KeyError:
            print comment['cmt_id']
            continue


def get_users():
    for user in jd.conn_user.find():
        try:
            users.append((user['join_time'], user['area']))
        except KeyError:
            print user['_id']
            continue


# stars analysis
def plot_stars():
    star_list = [0, 0, 0, 0, 0]
    thumbs_list = [0, 0, 0, 0, 0]
    for star, thumbs, cmt_date in comments:
        if star == 0:
            continue
        else:
            star_list[star-1] += 1
            thumbs_list[star-1] += int(thumbs)
    star_arr = np.array(star_list)
    thumbs_arr = np.array(thumbs_list)
    plt.plot([1, 2, 3, 4, 5], star_arr, 'bo', linestyle="-")
    plt.plot([1, 2, 3, 4, 5], thumbs_arr, 'r^', linestyle="-.")
    plt.xlabel('Stars')
    plt.ylabel('Counts')
    plt.title('Histogram of Stars')
    for i in range(1, 6):
        plt.text(i+0.1, star_arr[i-1]+0.1, star_arr[i-1])
        plt.text(i+0.1, thumbs_arr[i-1]+0.1, thumbs_arr[i-1])
    plt.text(0.1, star_arr[0]-30, 'stars count')
    plt.text(0.1, thumbs_arr[0]+30, 'stars thumbs')
    plt.axis([0, 6, 200, 5000])
    plt.grid(True)
    plt.show()


def plot_users():
    user_dict = dict()
    for join_time, area in users:
        if user_dict.get(area) is None:
            user_dict.setdefault(area, 1)
        else:
            user_dict.update({area: user_dict.get(area)+1})
    user_sorted = sorted(user_dict.iteritems(), key=lambda x: x[1], reverse=True)
    print "total area is: ", len(user_dict.keys())
    areas = [k for k, v in user_sorted[:15]]
    counts = [v for k, v in user_sorted[:15]]
    for i in range(len(areas)):
        print "area -> counts: %s, %d"% (areas[i], counts[i])
        print

    colors = list()
    explore = list()
    for i in range(len(areas)):
        colors.append(random.choice(plt.cm.colors.cnames.keys()))
        explore.append(random.choice([0, 0.1, 0.2]))
    plt.pie(counts, labels=areas, colors=colors, explode=explore, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.show()

get_comments()
plot_stars()
get_users()
plot_users()
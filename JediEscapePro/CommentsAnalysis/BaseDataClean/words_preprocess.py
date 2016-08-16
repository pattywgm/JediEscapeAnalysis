#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: words_preprocess.py
@time: 16/8/12  上午9:52
@desc: words preprocessing of : words segmentation, frequency calculate
"""
import os
import jieba
import sys
sys.path.append("/Users/pattywgm/SelfProject/DouBanMovieProVenv/JediEscapePro")
print sys.path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from JediEscapePro.pipelines import JediEscapeProPipeline


STATIC_PATH = '/Users/pattywgm/SelfProject/DouBanMovieProVenv/JediEscapePro/JediEscapePro/CommentsAnalysis/statics/'
jd = JediEscapeProPipeline()


def get_stop_words():
    # get stop words set
    with open(STATIC_PATH + "stop_words") as f:
        stop_words = list()
        for line in f.readlines():
            stop_words.append(line.strip().decode('utf-8'))
        return set(stop_words)


def words_process():
    # cut words and calculate the words frequency
    stop_words = get_stop_words()
    words_freq = dict()
    with open(STATIC_PATH + "words_seg.txt", 'w') as f:
        for comment in jd.conn.find():
            words_cont = set(jieba.cut(comment['cmt_cont'].strip().encode("utf-8")))
            words_res = words_cont - stop_words
            for word in words_res:
                word = word.upper()
                if len(word) > 1 and word != ' ':
                    if words_freq.get(word) is None:
                        words_freq.setdefault(word, 1)
                    else:
                        words_freq.update({word: words_freq.get(word)+1})
            f.write(' '.join(words_res).encode("utf-8"))
            f.write(os.linesep)
    with open(STATIC_PATH + "words_freq.txt", 'w') as ff:
        for k, v in words_freq.iteritems():
            ff.write(k.encode("utf-8") + ' ' + str(v))
            ff.write(os.linesep)
    return words_freq


def words_cloud():
    words_freql = words_process()
    words_freq = list()
    for _ in sorted(words_freql.iteritems(), key=lambda x: x[1], reverse=True)[:100]:
        print _[0], ": ", _[1]
        print
    for k, v in words_freql.iteritems():
        words_freq.append((k, v))
    # read the mask / color image
    alice_coloring = imread(STATIC_PATH + 'alice_color.png')
    wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring, max_font_size=40,
                   random_state=42, font_path="/Library/Fonts/Kaiti.ttc")
    wc.generate_from_frequencies(words_freq)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()



words_cloud()



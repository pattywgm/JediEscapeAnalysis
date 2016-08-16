#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: words_cloud.py
@time: 16/8/12  上午9:52
@desc: 
"""
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)

# Read the whole text.
text = open('/Users/pattywgm/SelfProject/DouBanMovieProVenv/JediEscapePro/JediEscapePro/CommentsAnalysis/statics/words_freq.txt').readlines()

# read the mask / color image
alice_coloring = imread('/Users/pattywgm/SelfProject/DouBanMovieProVenv/JediEscapePro/JediEscapePro/CommentsAnalysis/statics/alice_color.png')

wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
               # stopwords=STOPWORDS.add("said"),
               max_font_size=40, random_state=42, font_path="/Library/Fonts/Kaiti.ttc")
# generate word cloud
word_freq = list()
for line in text:
    try:
        word_freq.append((int(line.split(" ")[0].strip()), line.split(" ")[1]))
    except IndexError, e:
        print line
        continue
wc.generate_from_frequencies(word_freq)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show
plt.imshow(wc)
plt.axis("off")
# plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
# plt.imshow(wc.recolor(color_func=image_colors))
# plt.axis("off")
# plt.figure()
# plt.imshow(alice_coloring, cmap=plt.cm.gray)
# plt.axis("off")
plt.show()
#!/usr/bin/env python2
"""
Masked wordcloud
================
Using a mask you can generate wordclouds in arbitrary shapes.
"""

from os import path
import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'reviews_list.txt')).read()

# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
alice_mask = np.array(Image.open(path.join(d, "batman.png")))

wc = WordCloud(background_color="transparent", max_words=2000, mask=alice_mask,
               stopwords=STOPWORDS.add("said"))
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "fiverr.gif"))

# show
plt.imshow(wc)
plt.axis("off")
plt.figure()
plt.imshow(alice_mask, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
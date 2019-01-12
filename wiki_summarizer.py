
# coding: utf-8

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet as wn
import bs4 as bs
from io import BytesIO
import urllib.request
import re
import heapq
import requests
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

stop_words = set(stopwords.words("english"))


search = input("enter search")
search = re.sub('\s+', '_', search.lower())
url_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + search)
page = url_data.read().decode('utf-8')
parse = bs.BeautifulSoup(page, 'lxml')
para = parse.find_all('p')
text = ''
for p in para:
    text += p.text


img_links = parse.find("a", {"class": "image"})
link = img_links.img['src']
link = 'http:' + link
img = requests.get(link)
show_image = Image.open(BytesIO(img.content))
print(link)
show_image.show()

   # removes references
pages = re.sub(r'\\.[0-9]*\\', ' ', text)
pages2 = re.sub(r'\s+', ' ', pages)

   # create weighted frequencies
format_text = re.sub(r'[^a-zA-Z]', ' ', pages2)
format_page = re.sub(r'\s+', ' ', format_text)

   # creates tokens
token_w = word_tokenize(format_page.lower())
token_s = sent_tokenize(pages2)


token_words = []
    for w in token_w:
     if wn.synsets(w):
         token_words.append(w)


 frequencies = {}


    for w in token_words:
        if w not in stop_words:
            if w not in frequencies.keys():
                frequencies[w] = 1
            else:
                frequencies[w] += 1 


# find most used words in article
# use tool to see if they are a synonym/plural of each other
for w in token_words:
    if w not in stop_words:
        if w not in frequencies.keys():
            frequencies[w] = 1
        else:
            frequencies[w] += 1      


words_sorted = {}
words_sorted = sorted( frequencies, key = frequencies.__getitem__, reverse = True)

# top 15 most frequently used words
# print(words_sorted[:25])

cloud_text = str(words_sorted[:30])


wordcloud = WordCloud(background_color= 'white', max_words = 30)
wordcloud.generate(cloud_text)
plt.imshow(wordcloud, interpolation= 'bilinear')



# find the weighted frequency of words to see
max_freq = max(frequencies.values())

for w in frequencies.keys():
    frequencies[w] = frequencies[w]/max_freq

# finding most important sentences
sentences = {}
for sent in token_s:
    for w in token_words:
        if w in frequencies.keys():
            if len(sent.split(' ')) < 15:
                if sent not in sentences.keys():
                    sentences[sent] = frequencies[w]
                else:
                    sentences[sent] += frequencies[w]

scoring = heapq.nlargest(10, sentences, key= sentences.get)
summary = ' '.join(scoring)
print(summary)

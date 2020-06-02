#!/usr/bin/env python

from __future__ import with_statement

import sys, itertools

import numpy as np
#import matplotlib.pyplot as plt

import nltk

"""
Frequency counts of keywords in in document.
Then produces histogram using matplotlib and d3.js

Requires at least: Python 2.7, matplotlib, numpy
Document must be utf-8 or ascii encoded TEXT document

To run:
$ python frequency_words.py frequency_words_doc0.txt   # small document 
$ python frequency_words.py frequency_words_doc1.txt   # larger document
$ python frequency_words.py                            # runs an internal test document 

Open frequency_d3.html to see d3 visualization
"""


SKIP_SEPARATORS = ['. ', ' .', ',', ';', ':', '"', "'", '`', '~', '*', '!', '?', '(', ')', '{', '}', '<', '>',
                   '+', '=', '|', '\\', '/', '-']
SKIP_SEPARATORS_UNI = SKIP_SEPARATORS + [u'\u2022', ]  # the bullet symbol, more can be added ...
SKIP_WORDS = SKIP_SEPARATORS_UNI + ['the', 'a', 'of', 'for', 'and']  # can choose to skip these words, not used here


def get_freq(words):
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
    
    
def get_freq_sorted(words):
    freq = get_freq(words)
    return sorted(freq.items(), key=lambda item: item[1], reverse=True)
  
  
def freq_defaultdict():
    from collections import Counter
    freq_counter = Counter(words.split())
    return dict(freq_counter)
    

def get_words(**kwargs):
    _doc = kwargs['doc']
    _skip_words = []
    if 'skip_words' in kwargs:
        _skip_words = kwargs['skip_words']
        
    doc_lower = _doc.lower()
    for s in SKIP_SEPARATORS_UNI:
        doc_lower = doc_lower.replace(s, ' ')
    doc_lower_split = doc_lower.split()
    
    if _skip_words:
        words = [w for w in doc_lower_split if w not in _skip_words]
    else:
        words = doc_lower_split
    return words
    
    
def get_words_nltk(**kwargs):
    """
    Different definition of 'word'; eg, framework.python is one word
    """
    _doc = kwargs['doc']
    _skip_words = []
    if 'skip_words' in kwargs:
        _skip_words = kwargs['skip_words']
    
    words = []
    for s in nltk.sent_tokenize(_doc.lower()):
        for t in nltk.word_tokenize(s):
            if t in SKIP_SEPARATORS_UNI:
                continue
            if t == '.':
                continue
            words.append(t)
                
    if _skip_words:
        words = [w for w in words if w not in _skip_words]
    
    return words


def render_histogram_matplot(freq_sorted, save=True, show=False):
    keys = [kv[0] for kv in freq_sorted]
    freqs = [kv[1] for kv in freq_sorted]
    
    N = len(keys)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.20
    
    p1 = plt.bar(ind, freqs, width, color='b')
    
    plt.ylabel('Word Frequency')
    plt.title('Word Frequency of Document')
    plt.xticks(ind+width/2, keys, rotation=55, fontsize=8)
    if show:
        plt.show()
    if save:
        pass
    

def output_tsv(freq_sorted, outfile_name):
    try:
        with open(outfile_name, "w") as f:
          f.write("word\tfrequency\n".encode('utf-8'))
          for kv in freq_sorted:
            f.write(kv[0].encode('utf-8') + "\t" + str(kv[1]).encode('utf-8') + "\n")
            
    except IOError:
        print 'Unable to write data file'
        

def output_csv(freq_sorted, outfile_name):
    try:
        with open(outfile_name, "w") as f:
          f.write("word,frequency\n".encode('utf-8'))
          for kv in freq_sorted:
            f.write(kv[0].encode('utf-8') + "," + str(kv[1]).encode('utf-8') + "\n")

    except IOError:
        print 'Unable to write data file'


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as f :
                docu = unicode(f.read(), "UTF-8")
        except IOError: 
            print 'Unable to read input file ' + sys.arg[1]
            sys.exit()
    else:
        docu = u'\u2022 Python, Django, Django AB\u0107, Python; django; scraping python. the Java framework'
        print "Using test document:"
        print docu
    
    """
    Two different ways to run this, custom parser or use nltk
    """
    words = get_words(doc=docu, skip_words=SKIP_WORDS)
    #words = get_words_nltk(doc=docu, skip_words=SKIP_WORDS)
    
    freq_sorted = get_freq_sorted(words)
    print "\nFrequency of words:"
    for freq in freq_sorted:
        print freq[0], freq[1]
        
    output_csv(freq_sorted, "frequency_words.csv")     # open frequency_d3.html to view
    render_histogram_matplot(freq_sorted)
    
    """
    Finally can put this into a trie if you wanted to search this
    """
    
    

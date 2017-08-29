import re
from collections import defaultdict
from tweet.generate import Generated
import nltk
import random


def is_noun(word):
    POS = nltk.pos_tag([word])[0][1]
    return POS.startswith('NN')


class readTweet():
    def __init__(self, db=None, tweet=None):
        self.generator = Generated(db)
        self.tweet = tweet
        self.topic = None
        self.words = re.findall(r"[\w']+|[.!?;,:]", self.tweet)
        self.nouns = []
        self.nounFreq = defaultdict(list)
        self.wordFreq = defaultdict(list)
        self.bigrams = zip(self.words, self.words[1:])
        self.bigramFreq = defaultdict(list)
        self.replyStart = ''

    def getFreq(self):
        for word in self.words:
            self.wordFreq[word] = self.generator.wordFreq[word]

        for bigram in self.bigrams:
            self.bigramFreq[bigram] = self.generator.bigramFreq[bigram]

        self.getNouns()

    def getNouns(self):
        self.nouns = [word for word in self.words if is_noun(word)]

        for noun in self.nouns:
            self.nounFreq[noun] = self.generator.wordFreq[noun]

    def bigramReplyStarter(self):
        best_count = 1000000
        for key in self.bigramFreq:
            if (self.bigramFreq[key] > 0) & (self.bigramFreq[key] < best_count):
                self.replyStart = key[0] + ' ' + key[1]
                best_count = self.bigramFreq[key]
        if best_count == 1000000:
            self.replyStart = "What are you talking about?"

    def nounReplyStarter(self):
        best_count = 1000000
        for key in self.nounFreq:
            if (self.nounFreq[key] > 0) & (self.nounFreq[key] < best_count):
                next_start = random.choice(self.generator.transitions[key])
                while (len(set(next_start).intersection(set(self.generator.enders))) > 0):
                    next_start = random.choice(self.generator.transitions[key])
                self.replyStart = key.capitalize() + ' ' + ' '.join(next_start)
                best_count = self.nounFreq[key]
        if best_count == 1000000:
            self.replyStart = "What are you talking about? "

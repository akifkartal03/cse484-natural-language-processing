import math
import re

# nltk libraries
from nltk import collections
from nltk import tokenize
from nltk.util import ngrams
# syllable helper library
from turkishnlp import detector


# I didn't want to bother with global variables therefore,
# I created a class to encapsulate whole homework.
class HW2:

    def __init__(self):
        # write class variables here.
        self.__nlp = detector.TurkishNLP()
        self.__ngr = 0
        self.__ngramTable = None
        self.__ngramTableSize = 0
        self.__wordCounts = None
        self.__countTable = None
        self.__GtTable = None
        self.__n1 = None

        self.__testFile1 = None
        self.__testFile2 = None
        self.__testFile3 = None
        self.__testFile4 = None

    def get_results(self):
        print("test")
        # self.__separate_syllables()
        # self.__findPerplexity()
        #"""
        self.__ngr = 2
        self.__calculateNgrams(self.__ngr)
        self.__createCountTable()
        f1 = open("outputs/countTable.txt", "w", encoding="utf8")
        f1.write(str(self.__countTable))
        self.__gtSmoothing()
        self.__findTestPerplexity()
        f1 = open("outputs/gtTable.txt", "w", encoding="utf8")
        f1.write(str(self.__GtTable))
        #"""

    def __separate_syllables(self):
        self.__testFile1 = open('inputs/corpus_out.txt', 'r', encoding='utf-8')
        self.__testFile2 = open('inputs/corpus_syl2.txt', 'w', encoding='utf-8')
        obj = detector.TurkishNLP()

        line = self.__testFile1.read()
        arr = obj.syllabicate_sentence(line)
        for element in arr:
            for innerelement in element:
                self.__testFile2.write(innerelement)
                self.__testFile2.write(" ")
            self.__testFile2.write(",")
        self.__testFile2.close()
        self.__testFile1.close()

    def __sentence_syllable(self, sentence):
        obj = detector.TurkishNLP()
        arr = obj.syllabicate_sentence(sentence)
        res = []
        for element in arr:
            for innerelement in element:
                res.append(innerelement)
            res.append(' ')
        return res

    def __calculateNgrams(self, size):
        name = "outputs/myGram" + str(size) + ".txt"
        print(name)
        f = open('inputs/corpus_syl2.txt', 'r', encoding='utf-8')
        of = open(name, 'w', encoding='utf-8')
        corpusSyl = f.read()
        cs = re.split(" ,", corpusSyl)
        cs2 = []
        for i in cs:
            cs2.extend(i.split(" "))
            cs2.append(" ")
        self.__ngramTable = list(ngrams(cs2, size))
        f1 = open("outputs/counters.txt", "w", encoding="utf8")
        self.__wordCounts = collections.Counter(self.__ngramTable)
        f1.write(str(dict(self.__wordCounts)))
        self.__ngramTableSize = len(self.__ngramTable)
        #print("size: " + str(self.__ngramTableSize))
        of.write(' '.join(cs))
        f.close()
        of.close()
        f1.close()

    def __lowerText(self):
        f = open('inputs/corpus_test.txt', 'r', encoding='utf-8')
        of = open('inputs/corpus_test3.txt', 'w', encoding='utf-8')
        corpusSyl = f.read()
        corpusSyl = corpusSyl.lower()
        of.write(corpusSyl)
        f.close()
        of.close()

    def __createCountTable(self):
        self.__countTable = dict()
        for i in self.__wordCounts:
            if self.__wordCounts[i] in self.__countTable:
                self.__countTable[self.__wordCounts[i]] += 1
            else:
                self.__countTable[self.__wordCounts[i]] = 1

    def __gtSmoothing(self):
        self.__GtTable = dict()
        if 1 in self.__countTable:
            self.__n1 = self.__countTable[1]
        else:
            self.__n1 = 1
        for i in self.__wordCounts:
            c = self.__wordCounts[i]

            if (c + 1) not in self.__countTable:
                nc1 = 1
            else:
                nc1 = self.__countTable[c + 1]

            if c not in self.__countTable:
                nc = 1
            else:
                nc = self.__countTable[c]

            res1 = (((c + 1) * nc1) / nc) - ((c * ((c + 1) * nc1)) / self.__n1)
            res2 = 1 - (((c + 1) * nc1) / self.__n1)

            self.__GtTable[i] = res1 / res2

        print(self.__n1)

    def __findTestPerplexity(self):
        f = open('inputs/corpus_test.txt', 'r', encoding='utf-8')
        allSentences = tokenize.sent_tokenize(f.read())
        for sent in allSentences:
            result = self.__calculateTestPerplexity(sent)
            if result > 0:
                print(sent, result)

    def __chainWithMarkovAssumption(self, sentence):
        sylArr = self.__sentence_syllable(sentence)
        if len(sylArr) < self.__ngr:
            return 0

        gramList = list(ngrams(sylArr, self.__ngr))
        logSum = 0
        for i in gramList:
            if i in self.__GtTable:

                if self.__GtTable[i] / self.__ngramTableSize <= 0:
                    logSum += 0
                else:
                    logSum += math.log10(self.__GtTable[i] / self.__ngramTableSize)

            else:

                if self.__countTable[1] / self.__ngramTableSize <= 0:
                    logSum += 0
                else:
                    logSum += math.log10(self.__countTable[1] / self.__ngramTableSize)
        return math.exp(logSum)

    def __calculateTestPerplexity(self, sentence):
        res = self.__chainWithMarkovAssumption(sentence)
        if res != 0:
            root = 1 / res
            return math.pow(root, 1 / self.__ngr)
        else:
            return 0


hw2 = HW2()
hw2.get_results()

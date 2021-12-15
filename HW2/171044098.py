#helper libs
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
        # class variables
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
        self.__corpusSylFile = None
        self.__corpusTestFile = None
        self.__perpFile = None
        self.__gramFile = None
        self.__countFile = None
        self.__counterFile = None
        self.__gtTableFile = None

    def get_results(self, ngr):
        print(str(ngr) + " Gram calculating...")

        self.__openFiles(ngr)
        self.__ngr = ngr
        self.__calculateNgrams(self.__ngr)
        self.__createCountTable()

        self.__countFile.write(str(self.__countTable))
        self.__gtSmoothing()
        self.__findTestPerplexity()
        self.__gtTableFile.write(str(self.__GtTable))
        print(str(ngr) + " Gram table size: " + str(self.__ngramTableSize))
        print("---------------------------------------------------")
        self.__closeFiles()

    def __openFiles(self, ngr):
        name1 = 'inputs/corpus_syl.txt'
        name2 = 'inputs/corpus_test.txt'
        name3 = "outputs/perpRes" + str(ngr) + ".txt"
        name4 = "outputs/nGrams" + str(ngr) + ".txt"
        name5 = "outputs/countTable" + str(ngr) + ".txt"
        name6 = "outputs/counter" + str(ngr) + ".txt"
        name7 = "outputs/GtTable" + str(ngr) + ".txt"
        self.__corpusSylFile = open(name1, 'r', encoding='utf-8')
        self.__corpusTestFile = open(name2, 'r', encoding='utf-8')
        self.__perpFile = open(name3, 'w', encoding='utf-8')
        self.__gramFile = open(name4, 'w', encoding='utf-8')
        self.__countFile = open(name5, 'w', encoding='utf-8')
        self.__counterFile = open(name6, 'w', encoding='utf-8')
        self.__gtTableFile = open(name7, 'w', encoding='utf-8')

    def __closeFiles(self):
        self.__corpusSylFile.close()
        self.__corpusTestFile.close()
        self.__perpFile.close()
        self.__gramFile.close()
        self.__countFile.close()
        self.__counterFile.close()
        self.__gtTableFile.close()

    def __separate_syllables(self):
        # this is one time used function
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
        corpusSyl = self.__corpusSylFile.read()
        cs = re.split(" ,", corpusSyl)
        cs2 = []
        for i in cs:
            cs2.extend(i.split(" "))
            cs2.append(" ")
        self.__ngramTable = list(ngrams(cs2, size))
        self.__wordCounts = collections.Counter(self.__ngramTable)
        self.__counterFile.write(str(dict(self.__wordCounts)))
        self.__ngramTableSize = len(self.__ngramTable)
        self.__gramFile.write(' '.join(cs))

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

            c0 = self.__n1 / self.__ngramTableSize
            if c not in self.__countTable or (c + 1) not in self.__countTable:
                self.__GtTable[i] = c0
            else:
                nc1 = self.__countTable[c + 1]
                nc = self.__countTable[c]

                res1 = (((c + 1) * nc1) / nc) - ((c * ((c + 1) * nc1)) / self.__n1)
                res2 = 1 - (((c + 1) * nc1) / self.__n1)

                self.__GtTable[i] = res1 / res2

    def __findTestPerplexity(self):

        allSentences = tokenize.sent_tokenize(self.__corpusTestFile.read())
        for sent in allSentences:
            result = self.__calculateTestPerplexity(sent)
            if result > 0:
                self.__writePerpToFile(sent, result)

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

    def __writePerpToFile(self, sentence, result):
        self.__perpFile.write(sentence + " " + str(result) + "\n")


hw2 = HW2()
hw2.get_results(1)
hw2.get_results(2)
hw2.get_results(3)
hw2.get_results(4)
hw2.get_results(5)
print("Calculation is done. Check output files..")

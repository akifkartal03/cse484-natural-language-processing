import math
import re
import numpy as np

# nltk libraries
from nltk import collections
from nltk.util import ngrams
# syllable helper library
from turkishnlp import detector

obj = detector.TurkishNLP()


# I didn't want to bother with global variables therefore,
# I created a class to encapsulate whole homework.
class HW3:

    def __init__(self):
        # class variables

        self.__in_testFile = None
        self.__out_testFile = None
        self.__english = ["i", "o", "u", "s", "c", "g"]
        self.__turkish = {"i": "ı", "o": "ö", "u": "ü",
                          "s": "ş", "c": "ç", "g": "ğ"}
        self.__resFile = None

    def get_results(self):
        self.__openFiles()
        self.__findBestSentence()
        self.__closeFiles()

    def __openFiles(self):
        name1 = 'inputs/test_sentences.txt'
        self.__in_testFile = open(name1, 'r', encoding='utf-8')


    def __closeFiles(self):
        self.__in_testFile.close()

    def __openResFile(self, ngr):
        name = "outputs/results_" + str(ngr) + "gram.txt"
        self.__resFile = open(name, 'a', encoding='utf-8')
    def __closeResFile(self):
        self.__resFile.close()

    def __findBestSentence(self):
        allSentences = self.__in_testFile.readlines()

        for sent in allSentences:
            possibles = self.____findPossibleSentences(sent)
            print("Test Sentence: " + sent + "Number of Possible Sentences: " + str(len(possibles)))
            print("------------------------------------------------")
            for i in range(1, 6):
                perp = HW2(i)
                res = possibles.pop()
                min = perp.get_results(res)
                self.__openResFile(i)
                for item in possibles:
                    temp = perp.get_results(item)
                    if temp < min:
                        min = temp
                        res = item
                self.__writePerpToFile(res)
                self.__closeResFile()
    def ____findPossibleSentences(self, sentence):

        occurenceDict = dict()
        resultSet = set()
        resultSet.add(sentence)
        size = 0
        for ele in self.__english:
            occurenceDict[ele] = [m.start() for m in re.finditer(ele, sentence)]
            size = size + len(occurenceDict[ele])

        for key1, value1 in occurenceDict.items():
            if len(value1) > 0:
                for index in value1:
                    tempList = []
                    for sent in resultSet:
                        liste = list(sent)
                        liste[index] = self.__turkish[key1]
                        tempList.append(''.join(liste))
                    for item in tempList:
                        resultSet.add(item)

        return resultSet

    def __writePerpToFile(self, sentence):
        self.__resFile.write(sentence + "\n")


# HW2 codes
class HW2:

    def __init__(self, ngr2):
        # class variables
        self.__nlp = detector.TurkishNLP()
        self.__ngr = 0
        self.__ngramTable = None
        self.__ngramTableSize = 0
        self.__wordCounts = None
        self.__countTable = None
        self.__GtTable = None
        self.__n1 = None
        self.__N = 0

        self.__testFile1 = None
        self.__testFile2 = None
        self.__corpusSylFile = None

        self.__openFiles(ngr2)
        self.__ngr = ngr2
        self.__calculateNgrams(self.__ngr)
        self.__createCountTable()
        self.__gtSmoothing()

    def get_results(self, sent):

        return self.__chainWithMarkovAssumption(sent)

    def __openFiles(self, ngr):
        name1 = 'inputs/corpus_syl2.txt'
        self.__corpusSylFile = open(name1, 'r', encoding='utf-8')

    def __closeFiles(self):
        self.__corpusSylFile.close()

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
        arr = obj.syllabicate_sentence(sentence)
        res = []
        for element in arr:
            for innerelement in element:
                res.append(innerelement)
        return res

    def __calculateNgrams(self, size):
        corpusSyl = self.__corpusSylFile.read()
        tokenized = corpusSyl.split()
        """
        cs = re.split(" ,", corpusSyl)
        cs2 = []
        for i in cs:
            cs2.extend(i.split(" "))
            cs2.append(" ")
        print(cs2)
         """
        self.__ngramTable = list(ngrams(tokenized, size))
        self.__wordCounts = collections.Counter(self.__ngramTable)
        self.__N = sum(self.__wordCounts.values())
        self.__counterGT = dict(self.__wordCounts)
        self.__ngramTableSize = len(self.__ngramTable)

    def __createCountTable(self):
        self.__countTable = dict()
        for i in self.__wordCounts:
            if self.__wordCounts[i] in self.__countTable:
                self.__countTable[self.__wordCounts[i]] += 1
            else:
                self.__countTable[self.__wordCounts[i]] = 1
            # self.__N = self.__N + 1
        # print(self.__N)

    def __gtSmoothing(self):
        self.__GtTable = dict()
        if 1 in self.__countTable:
            self.__n1 = self.__countTable[1]
        else:
            self.__n1 = 1
        for i in self.__wordCounts:
            c = self.__wordCounts[i]

            c0 = self.__n1 / self.__N
            if c not in self.__countTable:
                self.__GtTable[i] = c0
            elif (c + 1) not in self.__countTable:
                nc1 = c0
                nc = self.__countTable[c]

                res = (((c + 1) * nc1) / nc)
                self.__GtTable[i] = res
            else:
                nc1 = self.__countTable[c + 1]
                nc = self.__countTable[c]

                res = (((c + 1) * nc1) / nc)
                self.__GtTable[i] = res

    def __chainWithMarkovAssumption(self, sentence):
        # print(sentence)
        sylArr = self.__sentence_syllable(sentence)
        if len(sylArr) < self.__ngr:
            return 0

        gramList = list(ngrams(sylArr, self.__ngr))
        logSum = 0
        for i in gramList:

            if i in self.__GtTable:

                if self.__GtTable[i] <= 0:
                    logSum += 0
                else:
                    logSum += np.log(self.__GtTable[i])


            else:

                if self.__countTable[1] <= 0:
                    logSum += 0
                else:
                    logSum += np.log(self.__countTable[1])

        return np.exp(logSum)

    def __calculateTestPerplexity(self, sentence):
        res = self.__chainWithMarkovAssumption(sentence)
        return res



hw3 = HW3()
hw3.get_results()

print("Calculation is done. Check output files..")

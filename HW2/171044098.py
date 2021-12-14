from nltk import collections
from nltk.util import ngrams
from turkishnlp import detector


# I didn't want to bother with global variables therefore,
# I created a class to encapsulate whole homework.
class HW2:

    def __init__(self):
        # write class variables here.
        self.__nlp = detector.TurkishNLP()
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
        self.__calculateNgrams(2)
        self.__createCountTable()
        f1 = open("outputs/countTable.txt", "w", encoding="utf8")
        f1.write(str(self.__countTable))
        self.__gtSmoothing()
        f1 = open("outputs/gtTable.txt", "w", encoding="utf8")
        f1.write(str(self.__GtTable))

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
        self.__testFile2.close()
        self.__testFile1.close()

    def __calculateNgrams(self, size):
        name = "outputs/myGram" + str(size) + ".txt"
        print(name)
        f = open('inputs/corpus_syl.txt', 'r', encoding='utf-8')
        of = open(name, 'w', encoding='utf-8')
        corpusSyl = f.read()
        corpusSyl = corpusSyl.split(' ')
        self.__ngramTable = list(ngrams(corpusSyl, size))

        f1 = open("outputs/counters.txt", "w", encoding="utf8")
        self.__wordCounts = collections.Counter(self.__ngramTable)
        f1.write(str(dict(self.__wordCounts)))
        self.__ngramTableSize = len(self.__ngramTable)
        print("size: " + str(self.__ngramTableSize))
        of.write(' '.join(corpusSyl))
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


hw2 = HW2()
hw2.get_results()

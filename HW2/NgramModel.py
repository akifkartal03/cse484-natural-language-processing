from nltk import collections
from nltk.util import ngrams
from nltk import tokenize

import random
import math
import heceleme
import re


class NgramModel:
    tokens = []
    tokensWithoutSpace = []

    def __init__(self, corpusPath, testPath, n):

        self.n = n
        self.countMap = dict()  # countların kaç kere geçtiği
        self.smootedTable = dict()  # smooted table
        f = open(corpusPath, "r", encoding="utf8")
        fTest = open(testPath, "r", encoding="utf8")
        self.sentences = f.read()

        self.test = fTest.read()
        self.sentences = self.preProcessing(self.sentences)
        self.tokens = self.SpellingText(self.sentences)
        f1 = open("outputs/tokens.txt", "w", encoding="utf8")
        f1.write(' '.join(self.tokens))
        print("-------------------------------")
        self.tokensWithoutSpace = self.tokens
        self.setNgram(n)



    def Smoothing(self):

        k = 5
        kplus = 6
        if kplus not in self.countMap:  # number of c+1 count
            Nkplus1 = 1
        else:  # number of k+1 count
            Nkplus1 = self.countMap[kplus]

        if 1 in self.countMap:
            self.N1 = self.countMap[1]
        else:
            self.N1=1

        count = 0
        divider = 1 - (((k + 1) * Nkplus1) / self.N1)
        for i in self.nGramTable:
            c = self.nGramTable[i]  # count from ngramTable


            if c not in self.countMap:
                Nc=1
            else:
                Nc= self.countMap[c]

            if (c + 1) not in self.countMap:  # number of c+1 count
                Ncplus1 = 1
            else:
                Ncplus1 = self.countMap[c + 1]

            dividend = (((c + 1) * Ncplus1) / Nc) - ((c * (k + 1) * Nkplus1) / self.N1)

            self.smootedTable[i] = dividend / divider

            if (self.smootedTable[i] < 0):
                count += 1
                # print(i, c , Ncplus1, self.countMap[c],self.smootedTable[i],dividend,divider)
        # print(count)

    def MarkovChain(self, testSentence):

        testSentence = self.preProcessing(testSentence)
        tokens = self.SpellingText(testSentence)
        if len(tokens) < self.n:
            return 0

        gram = list(ngrams(tokens, self.n))

        sumOfLogs = 0

        for i in gram:
            if i in self.smootedTable:
                #print("if", i , self.smootedTable[i],self.nGramLen,self.smootedTable[i]/self.nGramLen)

                if self.smootedTable[i] / self.nGramLen<0:
                    sumOfLogs+=0
                else:
                    sumOfLogs += math.log10(self.smootedTable[i] / self.nGramLen)

            else:
                #print("else", i, self.countMap[1], self.nGramLen,self.countMap[1]/self.nGramLen)
                if self.countMap[1] / self.nGramLen < 0:
                    sumOfLogs+=0
                else:
                    sumOfLogs += math.log10(self.countMap[1] / self.nGramLen)

        # print(str(self.n) + "Gram""Markov chain:", math.exp(sumOfLogs))
        return math.exp(sumOfLogs)

    def calculatePerplexity(self):
        allSentences = tokenize.sent_tokenize(self.test)
        for sent in allSentences:
            perp = self.perplexity(sent)
            if perp > 0:
                print(sent, perp)

    def perplexity(self, testSentence):
        markov = self.MarkovChain(testSentence)
        if(markov!=0):
            p = 1 / markov
            return math.pow(p, 1 / self.n)
        else: return 0


    def randomSentenceGenerator(self):
        return self.generator("", "", 0)


    def countOfTable(self):
        # countların kaç kere geçtiğini hesapla
        for i in self.nGramTable:
            if self.nGramTable[i] in self.countMap:
                self.countMap[self.nGramTable[i]] += 1
            else:
                self.countMap[self.nGramTable[i]] = 1

    def setNgram(self, n):
        if n == 1:
            self.nGram = self.tokensWithoutSpace
        else:
            self.nGram = list((ngrams(self.tokens, n)))
        f1 = open("outputs/ngram.txt", "w", encoding="utf8")
        f1.write(str(self.nGram))
        print("nGram[5]:")
        print(self.nGram[5])
        print("---------------------------------------")
        self.setNgramLen()
        print("nGramLen:")
        print(self.nGramLen)
        print("---------------------------------------")
        self.setNGramTable()
        f1 = open("outputs/ngramTable.txt", "w", encoding="utf8")
        f1.write(str(dict(self.nGramTable)))
        self.countOfTable()
        f1 = open("outputs/countMap.txt", "w", encoding="utf8")
        f1.write(str(self.countMap))
        self.Smoothing()
        f1 = open("outputs/smothTable.txt", "w", encoding="utf8")
        f1.write(str(self.smootedTable))

    def setNgramLen(self):
        self.nGramLen = len(self.nGram)

    def setNGramTable(self):
        self.nGramTable = collections.Counter(self.nGram)

    def preProcessing(self, sentence):
        sentence = heceleme.lowerWithoutTurkish(sentence)  # make all letters lower accoding to turkish alphabet
        sentence = self.check_corpus(sentence)
        sentence = ''.join(i for i in sentence if not i.isdigit())
        sentence = re.sub(' +', ' ', sentence)
        return sentence

    def check_corpus(self, context):
        valid_harf = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k", "l"
            , "m", "n", "o", "ö", "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z", " "]
        ncontext = ""
        for i in range(len(context)):
            if context[i] in valid_harf:
                ncontext += context[i]
            else:
                ncontext += ' '
        return ncontext

    def SpellingText(self, sentence):
        verbs = sentence
        verbs = verbs.split(' ')
        hece_arr = []
        count = 0
        for i in verbs:
            heceli = str(heceleme.hypo(i))
            for t in heceli.split(" "):
                if t != '':
                    hece_arr.append(t)
                    count += 1
            if i != "":
                hece_arr.append(" ")
                count += 1
        if len(hece_arr)>0:
            hece_arr.pop()
        return hece_arr





    def generator(self, spell, sentence, call):
        if (call == 5):
            return sentence
        if (sentence == "" and self.n > 1):

            index = random.randrange(len(self.smootedTable) - 1)
            heceler = list(list(self.smootedTable.items())[index])[0]

            sentence = ''.join([str(elem) for elem in heceler])
            newSpell = []
            if self.n > 4:
                newSpell.append(heceler[len(heceler) - 4])
            if self.n > 3:
                newSpell.append(heceler[len(heceler) - 3])
            if self.n > 2:
                newSpell.append(heceler[len(heceler) - 2])
            newSpell.append(heceler[len(heceler) - 1])
            call += 1

            return self.generator(newSpell, sentence, call)
        elif self.n == 1:
            founded = collections.Counter(self.smootedTable).most_common(5)
            for i in founded:
                sentence += i[0]
            return sentence

        else:
            newSpell = []

            founded = dict()

            if self.n == 2:
                for key in self.smootedTable:
                    if key[0] == spell[0]:
                        founded[key] = self.smootedTable[key]
            elif self.n == 3:
                for key in self.smootedTable:
                    if key[0] == spell[0] and key[1] == spell[1]:
                        founded[key] = self.smootedTable[key]
            elif self.n == 4:
                for key in self.smootedTable:
                    if key[0] == spell[0] and key[1] == spell[1] and key[2] == spell[2]:
                        founded[key] = self.smootedTable[key]
            else:
                for key in self.smootedTable:
                    if key[0] == spell[0] and key[1] == spell[1] and key[2] == spell[2] and key[3] == spell[3]:
                        founded[key] = self.smootedTable[key]

            founded = collections.Counter(founded).most_common(1)

            if len(founded) == 0:
                return sentence

            found = founded[0]

            start = self.n - 1

            sentence += str(found[0][len(found[0]) - 1])
            if self.n > 4:
                newSpell.append(found[0][len(found[0]) - 4])
            if self.n > 3:
                newSpell.append(found[0][len(found[0]) - 3])
            if self.n > 2:
                newSpell.append(found[0][len(found[0]) - 2])
            newSpell.append(found[0][len(found[0]) - 1])

            call += 1
            return self.generator(newSpell, sentence, call)

test1 = NgramModel("inputs/corpus_out.txt", "inputs/corpus_test.txt",1)
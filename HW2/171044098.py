import math

import matplotlib.pyplot as plt
from turkishnlp import detector



# I didn't want to bother with global variables therefore,
# I created a class to encapsulate whole homework.
class HW2:

    def __init__(self):
        # write class variables here.
        self.__nlp = detector.TurkishNLP()
        self.__wordList1 = []
        self.__numberOfWord = 0
        self.__sum2 = 0
        self.__grp = []
        self.__sem_sim = []
        self.__firstLine = ""
        self.__testFile1 = None
        self.__testFile2 = None
        self.__testFile3 = None
        self.__testFile4 = None
        self.__syll_in = None
        self.__txt_in = None

    def get_results(self):
        self.__testFile1 = open('corpus_out.txt', 'r', encoding='utf-8')
        self.__testFile2 = open('corpus_syl.txt', 'w', encoding='utf-8')
        obj = detector.TurkishNLP()


        line = self.__testFile1.read()
        arr = obj.syllabicate_sentence(line)
        for element in arr:
            for innerelement in element:
                self.__testFile2.write(innerelement)
                self.__testFile2.write(" ")
        self.__testFile2.close()
        self.__testFile1.close()

    def __calculate_sem_sim_syl(self):

        acp = []
        self.__sum2 = 0
        for line in self.__wordList1:
            words = line.split()
            mainList = []

            for word in words[0:2]:
                arr = self.__nlp.syllabicate_sentence(word)
                listOfVectors = []

                for element in arr:
                    for inner_element in element:
                        alist = self.__searchFile(inner_element, self.__syll_in)
                        if alist is not None:
                            listOfVectors.append(alist)
                if len(listOfVectors) > 0:
                    mainList.append(listOfVectors)
            self.__addAndWrite(mainList, line, words[2])
            acp.append(float(words[2]))
        self.__sem_sim.append(100 - (self.__sum2 / len(self.__wordList1)))
        return 100 - (self.__sum2 / len(self.__wordList1))

    def __calculate_sem_sim_normal(self):
        self.__sum2 = 0
        counter = 0
        for line in self.__wordList1:
            words = line.split()
            mainList = []

            for word in words[0:2]:
                alist = self.__searchFile(word, self.__txt_in)
                if alist is not None:
                    mainList.append(alist)
                else:
                    print("ERRORRRR!!")
                    print(word)
            if len(mainList) > 1:
                acc = float(words[2])
                ecp = abs(self.__cosine_similarity(mainList[0], mainList[1]) - acc)
                self.__sum2 += (ecp / acc) * 100
            else:
                counter = counter + 1
        self.__sem_sim.append(100 - (self.__sum2 / (self.__numberOfWord - counter)))
        return 100 - (self.__sum2 / (self.__numberOfWord - counter))

    def __calculate_syn_sim_normal(self):
        self.__sum2 = 0
        counter = 0
        for line in self.__wordList1:
            words = line.split()
            mainList = []

            for word in words[0:4]:
                alist = self.__searchFile(word, self.__txt_in)
                if alist is not None:
                    mainList.append(alist)
                else:
                    print("ERRORRRR!!")
                    print(word)
            if len(mainList) > 3:
                acc = float(words[4])
                sum1_2 = [x + y for x, y in zip(mainList[1], mainList[2])]
                sub12_0 = [x - y for x, y in zip(sum1_2, mainList[0])]
                ecp = abs(self.__cosine_similarity(mainList[3], sub12_0) - acc)
                self.__sum2 += (ecp / acc) * 100
            else:
                counter = counter + 1
        self.__sem_sim.append(100 - (self.__sum2 / (self.__numberOfWord - counter)))
        return 100 - (self.__sum2 / (self.__numberOfWord - counter))

    def __calculate_syn_sim_syl(self):
        # self.__testFile.seek(0, 0)
        acp = []
        self.__sum2 = 0
        for line in self.__wordList1:
            words = line.split()
            mainList = []

            for word in words[0:4]:
                arr = self.__nlp.syllabicate_sentence(word)
                listOfVectors = []

                for element in arr:
                    for inner_element in element:
                        alist = self.__searchFile(inner_element, self.__syll_in)
                        if alist is not None:
                            listOfVectors.append(alist)
                if len(listOfVectors) > 0:
                    mainList.append(listOfVectors)
            self.__addAndWrite2(mainList, line, words[4])
            acp.append(float(words[4]))
        self.__sem_sim.append(100 - (self.__sum2 / len(self.__wordList1)))
        return 100 - (self.__sum2 / len(self.__wordList1))

    def __searchFile(self, syllable, name):
        name.seek(0, 0)
        for line in name:
            # print(line.split()[0])
            if line.split()[0] == syllable:
                str2 = syllable + " "
                vectorLine = line.replace(str2, '')
                # print(vectorLine)
                return [float(i) for i in vectorLine.split()]
                # return vectorLine.split()

    def __closeFiles(self):
        self.__testFile1.close()
        self.__testFile2.close()
        self.__testFile3.close()
        self.__testFile4.close()
        self.__syll_in.close()
        self.__txt_in.close()

    def __addAndWrite(self, vectorList, sylb, guess):
        if len(vectorList) > 1:
            vectList1 = [sum(elements) for elements in zip(*vectorList[0])]
            vectList2 = [sum(elements) for elements in zip(*vectorList[1])]
            result = self.__cosine_similarity(vectList1, vectList2)
            acc = float(guess)
            self.__sum2 += (abs(result - acc) / acc) * 100

        else:
            print(sylb + ": Not FOUND!!!")

    def __addAndWrite2(self, vectorList, sylb, guess):
        if len(vectorList) > 3:
            vectList0 = [sum(elements) for elements in zip(*vectorList[0])]
            vectList1 = [sum(elements) for elements in zip(*vectorList[1])]
            vectList2 = [sum(elements) for elements in zip(*vectorList[2])]
            vectList3 = [sum(elements) for elements in zip(*vectorList[3])]

            sum1_2 = [x + y for x, y in zip(vectList1, vectList2)]
            sub12_0 = [x - y for x, y in zip(sum1_2, vectList0)]
            result = self.__cosine_similarity(vectList3, sub12_0)
            acc = float(guess)
            self.__sum2 += (abs(result - acc) / acc) * 100

        else:
            print(sylb + ": Not FOUND!!!")

    def __initFields(self):
        self.__testFile1 = open('test_files/semantic_sim.txt', 'r', encoding='utf-8')
        self.__testFile2 = open('test_files/semantic_anlgy.txt', 'r', encoding='utf-8')
        self.__testFile3 = open('test_files/syntactic_sim.txt', 'r', encoding='utf-8')
        self.__testFile4 = open('test_files/syntactic_anlgy.txt', 'r', encoding='utf-8')
        self.__syll_in = open('test_files/heceVektors.txt', 'r', encoding='utf-8')
        self.__txt_in = open('test_files/word2vec2.txt', 'r', encoding="utf-8", errors='ignore')

    def __cosine_similarity(self, vect1, vect2):
        xx, xy, yy = 0, 0, 0
        for i in range(len(vect1)):
            x = vect1[i]
            y = vect2[i]
            xx += x * x
            yy += y * y
            xy += x * y
        return xy / math.sqrt(xx * yy)

    def __q9(self, syllable):
        self.__txt_in.seek(0, 0)
        for line in self.__txt_in:
            # print(line.split()[0])
            if line.split()[0] == syllable:
                str2 = syllable + " "
                vectorLine = line.replace(str2, '')
                # print(vectorLine)
                return [float(i) for i in vectorLine.split()]

    def __drawGraph(self, title):

        left = [2, 3]
        height = self.__grp
        tick_label = ['word2vec', 'syllable based']
        plt.bar(left, height, tick_label=tick_label,
                width=0.1, color=['blue', 'green'])

        plt.xlabel('Methods')
        plt.ylabel('accuracy(%)')
        plt.title(title)
        plt.show()


hw1 = HW2()
hw1.get_results()

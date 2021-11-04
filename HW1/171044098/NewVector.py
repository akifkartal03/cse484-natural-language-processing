from turkishnlp import detector
import math



# I didn't want to bother with global variables therefore,
# I created a class to encapsulate whole homework.
class HW1:

    def __init__(self):
        # write class variables here.
        self.__nlp = detector.TurkishNLP()
        self.__wordList = []
        self.__dimension = 200
        self.numberOfWord = 0
        self.__firstLine = ""
        self.__testFile = open('test_words.txt', 'r', encoding='utf-8')
        self.__syll_in = open('mybin34.txt', 'r', encoding='utf-8')
        self.__syll_out = open('syllabled_vectors.txt', 'w', encoding='utf-8')
        self.__txt_in = open('sample9.txt', 'r', encoding='utf-8')
        self.__vect_in = open('mybin28.txt', 'r', encoding='utf-8')

    def get_results(self):
        # this is only public method to calculate all results
        self.__initFields()
        self.__getVectorsOfWord()

    def __getVectorsOfWord(self):
        #self.__testFile.seek(0, 0)
        for line in self.__wordList:
            arr = self.__nlp.syllabicate_sentence(line)
            listOfVectors = []
            for element in arr:
                for inner_element in element:
                    alist= self.__searchFile(inner_element)
                    #if alist is None:
                        #print(inner_element)
                        #print(line)
                    listOfVectors.append(alist)
            if len(listOfVectors) > 0:
                self.__addAndWrite(listOfVectors,line)
            #print(listOfVectors)


    def __searchFile(self, syllable):
        self.__syll_in.seek(0, 0)
        for line in self.__syll_in:
            # print(line.split()[0])
            if line.split()[0] == syllable:
                str2 = syllable + " "
                vectorLine = line.replace(str2, '')
                # print(vectorLine)
                return [float(i) for i in vectorLine.split()]
                # return vectorLine.split()




    def __closeFiles(self):
        self.__testFile.close()
        self.__syll_in.close()
        self.__syll_out.close()


    def __addAndWrite(self,vectorList,sylb):
        self.__syll_out.write(sylb)
        self.__syll_out.write(" ")
        vectList = [sum(elements) for elements in zip(*vectorList)]
        self.__syll_out.write(" ".join(str(x) for x in vectList))
        self.__syll_out.write("\n")



    def __initFields(self):
        corpusText = self.__txt_in.read()
        self.__wordList = corpusText.split()
        self.__dimension = self.__vect_in.readline().split()[1]
        self.__firstLine = self.__vect_in.readline()
        self.__syll_out.write(self.__firstLine)
        self.__syll_out.write("\n")
        #print(self.__wordList)

    def __cosine_similarity(vect1, vect2):

        xx, xy, yy = 0, 0, 0
        for i in range(len(vect1)):
            x = vect1[i];
            y = vect2[i]
            xx += x * x
            yy += y * y
            xy += x * y
        return xy / math.sqrt(xx * yy)

    """
    def __q9(self):
        self.__common_5to13("X")

    def __q10(self):
        self.__common_5to13("Z")
 """


hw1 = HW1()
hw1.get_results()

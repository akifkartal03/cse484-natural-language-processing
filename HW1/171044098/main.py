# 171044098-Akif Kartal
# turkish nlp package must be installed

from turkishnlp import detector

obj = detector.TurkishNLP()

f = open('sample36.txt','r',encoding = 'utf-8')
file = open('heceler.txt','w',encoding = 'utf-8')

line = f.read()
arr = obj.syllabicate_sentence(line)
for element in arr:
    for innerelement in element:
        file.write(innerelement)
        file.write(" ")
file.close()
f.close()


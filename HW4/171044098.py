# -*- coding: utf-8 -*-
"""171044098.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ieeOK3oVarmn_3KL8JzOWyFuX5J7UdOx

Import libraries
"""

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense
from keras.models import Sequential
import numpy as np
import tensorflow as tf
import pickle
import re
from google.colab import drive
from keras.utils import np_utils

"""### Connect Google Drive Account
Please add files to the paths.
"""

#add corpus file to your google drive path is 'Colab Notebooks/data/corpus_out3.txt'
#add test_sentence file to your google drive path is 'Colab Notebooks/data/test_sentences.txt'

drive.mount('/content/drive')
path = '/content/drive/My Drive/Colab Notebooks/data/corpus_out3.txt'

"""Clean data and remove noisy"""

def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"", text)


def remove_html(text):
    html = re.compile(r"<.*?>")
    return html.sub(r"", text)


file = open(path, 'r', encoding='utf-8')
data1 = file.read()
data1 = remove_URL(data1)
data1 = remove_html(data1)
data1 = data1.lower()
data1 = data1.replace('\n', '').replace('\r', '')
data = data1.split(".")
data = np.array_split(data, 16)[0]

print(len(data))
print(data[:10])

"""Split data into word tokens"""

tokenizer = Tokenizer()
tokenizer.fit_on_texts(data)
vocab = tokenizer.word_index
seqs = tokenizer.texts_to_sequences(data)

"""Prepare train data"""

def prepare_sentence(seq, maxlen):
    
    x = []
    y = []
    for i, w in enumerate(seq):
        x_padded = pad_sequences([seq[:i]],
                                 maxlen=maxlen - 1,
                                 padding='pre')[0]  
        x.append(x_padded)
        y.append(w)
    return x, y


maxlen = max([len(seq) for seq in seqs])
x = []
y = []
for seq in seqs:
    x_windows, y_windows = prepare_sentence(seq, maxlen)
    x += x_windows
    y += y_windows
x = np.array(x)
y = np.array(y) - 1  
y = np.eye(len(vocab))[y]  
print(x.shape)

"""Tain model"""

model = Sequential()
model.add(Embedding(input_dim=len(vocab) + 1,                    
                    output_dim=5,  
                    input_length=maxlen - 1))  
model.add(LSTM(64))
model.add(Dense(len(vocab), activation='softmax'))
model.compile('rmsprop', 'categorical_crossentropy')

model.fit(x, y, epochs=1)


#path='/content/drive/MyDrive/Colab Notebooks/model2/'
#pickle.dump(model, open(path+'model30.pkl','wb'))

"""Try to Find best sentences"""

import sys
name1 = '/content/drive/My Drive/Colab Notebooks/data/test_sentences.txt'
in_testFile = open(name1, 'r', encoding='utf-8')

english = ["i", "o", "u", "s", "c", "g"]
turkish = {"i": "??", "o": "??", "u": "??",
                  "s": "??", "c": "??", "g": "??"}

maxlen = max([len(seq) for seq in seqs])

def prepare_sentence(seq, maxlen):
    
    x = []
    y = []
    for i, w in enumerate(seq):
        x_padded = pad_sequences([seq[:i]],
                                 maxlen=maxlen - 1,
                                 padding='pre')[0]  
        x.append(x_padded)
        y.append(w)
    return x, y

def findPossibleSentences(sentence):

    occurenceDict = dict()
    resultSet = set()
    resultSet.add(sentence)
    size = 0
    for ele in english:
        occurenceDict[ele] = [m.start() for m in re.finditer(ele, sentence)]
        size = size + len(occurenceDict[ele])

    for key1, value1 in occurenceDict.items():
        if len(value1) > 0:
            for index in value1:
                tempList = []
                for sent in resultSet:
                    liste = list(sent)
                    liste[index] = turkish[key1]
                    tempList.append(''.join(liste))
                for item in tempList:
                    resultSet.add(item)

    return resultSet

def writePerpToFile(sentence):
    print("Best Sentence: " + sentence)
    print("------------------------------------------------")
  
def findBestSentence():
    allSentences = in_testFile.readlines()

    for sent in allSentences:
        possibles = findPossibleSentences(sent)
        print("Test Sentence: " + sent + "Number of Possible Sentences: " + str(len(possibles)))
        
        res = sent
        min = get_results(res)
        for item in possibles:
            temp = get_results(item)
            if  temp > min:
                min = temp
                res = item
        writePerpToFile(res)
            
def get_results(sentence):
    tok = tokenizer.texts_to_sequences([sentence])[0]
    x_test, y_test = prepare_sentence(tok, maxlen)
    if len(x_test)== 0 :
      return -sys.maxsize - 1
    else:
      x_test = np.array(x_test)
      y_test = np.array(y_test) - 1  
      
      p_pred = model.predict(x_test)
      
      
      vocab_inv = {v: k for k, v in vocab.items()}
      log_p_sentence = 0
      for i, prob in enumerate(p_pred):
          word = vocab_inv[y_test[i]+1]  
          prob_word = prob[y_test[i]]
          log_p_sentence += np.log(prob_word)
      return np.exp(log_p_sentence)
    


findBestSentence()
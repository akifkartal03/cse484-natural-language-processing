# 171044098-Akif Kartal
# turkish nlp package must be installed

from turkishnlp import detector

obj = detector.TurkishNLP()
print(obj.syllabicate_sentence("Hiç unutmadım, doğudan esen hafif bir yel saçlarını dalgalandırıyordu"))

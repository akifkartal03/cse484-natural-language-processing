time ./word2vec -train sample36.txt -output word2vec2.txt -cbow 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -binary 0
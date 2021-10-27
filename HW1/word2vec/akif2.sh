time ./word2vec -train mytext.txt -output mybin26.bin -cbow 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -binary 1
./distance mybin26.bin


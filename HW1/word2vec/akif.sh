time ./word2vec -train input -output mybin10.txt -cbow 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15
./distance mybin10.txt
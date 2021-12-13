crypto: 
	g++ -c ./src/utils.cpp -o ./bin/utils.o
	g++ ./src/sm4_enc.cpp -o ./bin/sm4_enc ./bin/utils.o
	g++ ./src/sm4_dec.cpp -o ./bin/sm4_dec ./bin/utils.o
	g++ ./src/sm3.cpp -o ./bin/sm3 ./bin/utils.o
	mkdir ../info
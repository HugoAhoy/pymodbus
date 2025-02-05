#ifndef __utils_h
#define __utils_h

#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <ctime>
#include <time.h>
#include <random>

typedef std::bitset<8> Byte;
typedef std::bitset<32> Word;

Word BytesToWord(Byte& k1, Byte& k2, Byte& k3, Byte& k4);
void WordToBytes(Word w, Byte* ByteS);
void GenerateRandomBytes(Byte *Arr, int n);
void GenerateRandomWords(Word *Arr, int n);
void CharToByte(Byte* Block, char* buffer);
Byte GFMul(Byte a, Byte b);
Word ModTwoAdd(Word x, Word y);
std::string ReadFileToString(std::string path);
void StringToBytes(std::string Mess, Byte* Message);
void StringToWords(std::string mess, Word* Message, int n);
std::string WordsToString(Word* Mess, int n);

#endif
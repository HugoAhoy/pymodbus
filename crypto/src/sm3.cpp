#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <ctime>
#include <time.h>
#include <random>
#include <math.h>
#include "utils.h"

#define DEBUG

using namespace std;

const int padLen = 448;
const int padAll = 512;

Word IV[8] = {
    0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 
    0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
};

Word FetchTj(int j){
    /*
        Fetch the constant Tj from input j.
    */
   Word res;
   if(j<=15){
       res = 0x79cc4519;
   }
   else if(j<=63){
       res = 0x7a879d8a;
   }
   return res;
}

Word FFj(Word x, Word y, Word z, int j){
    /*
        Bool function FF, execute by int j.
    */
   Word res;
   if(j<=15){
       res = x ^ y ^ z;
   }
   else if(j<=63){
       res = (x & y) | (x & z) | (y & z);
   }
   return res;
}

Word GGj(Word x, Word y, Word z, int j){
    /*
        Bool function GG, execute by int j.
    */
   Word res;
   if(j<=15){
       res = x ^ y ^ z;
   }
   else if(j<=63){
       res = (x & y) | ((~x) & z);
   }
   return res;
}

Word P0(Word x){
    /*
        Permutation function P0.
    */
   Word tmpLeft, tmpRight;
   Word tmp1, tmp2;

   tmpLeft = x << 9;
   tmpRight = x >> 23;
   tmp1 = tmpLeft | tmpRight;

   tmpLeft = x << 17;
   tmpRight = x >> 15;
   tmp2 = tmpLeft | tmpRight;

   return x ^ tmp1 ^ tmp2;
}

Word P1(Word x){
    /*
        Permutation function P0.
    */
   Word tmpLeft, tmpRight;
   Word tmp1, tmp2;

   tmpLeft = x << 15;
   tmpRight = x >> 17;
   tmp1 = tmpLeft | tmpRight;

   tmpLeft = x << 23;
   tmpRight = x >> 9;
   tmp2 = tmpLeft | tmpRight;

   return x ^ tmp1 ^ tmp2;
}

void padding(string mess, int l, int k, Word* Message, int n){
    /*
        sm4 padding.
    */
   replace(mess.begin(), mess.end(), '\n', '0');
   mess += "1";
   for(int i=0; i<k; i++){
       mess += "0";
   }
   bitset<64> linfo = l;
   mess += linfo.to_string();
//    mess.erase(remove(mess.begin(), mess.end(), '\n'), mess.end());
//    cout << "mess: " << mess << endl;

   for(int i=0; i<n; i++){
    //    cout << "i = " << i << endl;
       Message[i] = (Word) mess.substr(i*32, (i+1)*32);
    //    cout << mess.substr(i*32, (i+1)*32) << endl;
   }
}

void MessExpansion(Word* MessBlock, Word* ExpandMess){
    /*
        Messsage expansion function.
    */
   Word tmpLeft, tmpRight;
   Word tmp1, tmp2;
   for(int i=0; i<16; i++){
       ExpandMess[i] = MessBlock[i];
   }
   for(int i=16; i<68; i++){
       tmpLeft = ExpandMess[i-3] << 15;
       tmpRight = ExpandMess[i-3] >> 17;
       tmp1 = tmpLeft|tmpRight;

       tmpLeft = ExpandMess[i-13] << 7;
       tmpRight = ExpandMess[i-13] >> 25;
       tmp2 = tmpLeft|tmpRight;

       ExpandMess[i] = P1(ExpandMess[i-16]^ExpandMess[i-9]^tmp1) ^ tmp2 ^ ExpandMess[i-6];
   }
   for(int i=0; i<64; i++){
       ExpandMess[68+i] = ExpandMess[i] ^ ExpandMess[i+4];
   }
}

void CF(Word* v, Word* MessBlock, int i, Word* NewV){
    /*
        Compression function.
    */
   Word ExpandMess[132];
   MessExpansion(MessBlock, ExpandMess);

   Word A, B, C, D, E, F, G, H;
   Word SS1, SS2, TT1, TT2;
   Word tmpLeft, tmpRight, tmp;
   A = v[0];
   B = v[1];
   C = v[2];
   D = v[3];
   E = v[4];
   F = v[5];
   G = v[6];
   H = v[7];

   for(int j=0; j<64; j++){
       tmpLeft = A << 12;
       tmpRight = A >> 20;
       tmp = tmpLeft|tmpRight;

       Word T = FetchTj(j);
    //    cout << "fetch T: " << T.to_string() << endl;
       tmpLeft = T << (j % 32);
       tmpRight = T >> (32 - (j%32));
       T = tmpLeft|tmpRight;
    //    cout << "here: " << T.to_string() << endl;

       SS1 = ModTwoAdd(ModTwoAdd(tmp, E), T);
       tmpLeft = SS1 << 7;
       tmpRight = SS1 >> 25;
       SS1 = tmpLeft | tmpRight;
       SS2 = SS1 ^ tmp;

       TT1 = ModTwoAdd(FFj(A, B, C, j), D);
       TT1 = ModTwoAdd(TT1, SS2);
       TT1 = ModTwoAdd(TT1, ExpandMess[68+j]);

       TT2 = ModTwoAdd(GGj(E, F, G, j), H);
       TT2 = ModTwoAdd(TT2, SS1);
       TT2 = ModTwoAdd(TT2, ExpandMess[j]);

       D = C;
       tmpLeft = B << 9;
       tmpRight = B >> 23;
       C = tmpLeft | tmpRight;

       B = A;
       A = TT1;
       H = G;
       tmpLeft = F << 19;
       tmpRight = F >> 13;
       G = tmpLeft | tmpRight;

       F = E;
       E = P0(TT2);
    }
    NewV[0] = A ^ v[0];
    NewV[1] = B ^ v[1];
    NewV[2] = C ^ v[2];
    NewV[3] = D ^ v[3];
    NewV[4] = E ^ v[4];
    NewV[5] = F ^ v[5];
    NewV[6] = G ^ v[6];
    NewV[7] = H ^ v[7];
}


int main(int argc, char* argv[]){
    
    string message;
    if(argc != 2){
        cout << "erro input, only one messgae is required. " << endl;
    }
    
    message = argv[1];
    // cout << "Check: " << message << endl;
    // #ifdef DEBUG
    //     string message = "011000010110001001100011";
    // #endif

    // #ifndef DEBUG
    //     string path = "./test/Message.txt";
    //     string message = ReadFileToString(path);
    // #endif

    int l = message.size();
    // cout << "message length: " << l << endl;
    int n = (ceil((l+1-padLen) / padAll) > 0) ? floor((l+1-padLen) / padAll) + 1 : 0;
    int k = n*padAll + padLen - (l + 1);
    n = ((l+1)+k+64) / 32;
    int N = (l+k+65) / 512;
    Word Message[n];

    clock_t time_begin_padding = clock();
    padding(message, l, k, Message, n);
    clock_t time_after_padding = clock();

    Word newV[8];
    clock_t time_begin = clock();
    for(int i=0; i<N; i++){
        Word MessBlock[16];
        for(int j=0; j<16; j++){
            MessBlock[j] = Message[i*16+j];
        }
        CF(IV, MessBlock, i, newV);
        for(int j=0; j<8; j++){
            IV[j] = newV[j];
        }
    }
    clock_t time_end = clock();

    // cout << "Final v: " << endl;
    // for(int i=0; i<8; i++){
    //     cout << hex << newV[i].to_ulong() << " ";
    // }
    // cout << endl;

    string finalV = "";
    finalV = WordsToString(newV, 8);
    ofstream outfile;
    outfile.open("./info/hash.txt");
    outfile << finalV;

    // cout << "Padding time: " << (time_after_padding - time_begin_padding)*1.0 / CLOCKS_PER_SEC << endl;
    // cout << "SM3 time: " << (time_end - time_begin)*1.0 / CLOCKS_PER_SEC << endl;
}

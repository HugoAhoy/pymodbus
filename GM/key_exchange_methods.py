from gmssl import sm2, sm3, sm4, func
import random
import math
import GM.sm2genkey as sm2genkey


ecc_table = sm2.default_ecc_table
n = int(ecc_table['n'], 16)
p = int(ecc_table['p'], 16)
a = int(ecc_table['a'], 16)
b = int(ecc_table['b'], 16)
g = ecc_table['g']
gx = g[0:len(g)//2]
gy = g[len(g)//2:]


if __name__ == "__main__":
    cnt = 0
    for idx in range(100):
        print(idx)
        # pa、pb是事先都知道的公钥
        # da、db是自己的私钥
        da, pa = sm2genkey.create_key_pair()
        db, pb = sm2genkey.create_key_pair()
        # print(da, pa, db, pb)
        # print(len(da))
        # print(len(pa))
        # print(len(db))
        # print(len(pb))
        w = math.ceil(math.ceil(math.log2(n))/2.0)-1
        ra = random.randint(1, n-1)
        tmp_sm2 = sm2.CryptSM2('', '')
        # 把RA发给B
        RA = tmp_sm2._kg(ra, g)
        rb = random.randint(1, n-1)
        # 把RB发给A
        RB = tmp_sm2._kg(rb, g)
        rbx = int(RB[0:len(RB)//2], 16)
        rby = int(RB[len(RB)//2:], 16)
        rax = int(RA[0:len(RA)//2], 16)
        ray = int(RA[len(RA)//2:], 16)
        bar_x2 = 2**w+(rbx & (2**w-1))
        bar_x1 = 2**w+(rax & (2**w-1))
        tB = (int(db, 16)+bar_x2*rb) % n
        tA = (int(da, 16)+bar_x1*ra) % n

        # verify equation

        # print((ray**2-rax**3-int(a, 16)*rax-int(b, 16)) % int(p, 16))
        # print((rby**2-rbx**3-a*rbx-b) % p)

        x1RA = tmp_sm2._kg(bar_x1, RA)
        h = math.floor((p**0.5+1)**2/n)

        ptsum = sm2genkey.add([int(pa[0:len(pa)//2], 16), int(pa[len(pa)//2:], 16)],
                            [int(x1RA[0:len(x1RA)//2], 16), int(x1RA[len(x1RA)//2:], 16)], a, p)
        # print(ptsum)
        V = tmp_sm2._kg(tB*h, hex(ptsum[0])[2:]+hex(ptsum[1])[2:])
        Vbit = bin(int(V[0:len(V)//2], 16))[2:] + bin(int(V[len(V)//2:], 16))[2:]
        Vbit = Vbit.zfill(512)

        x2RB = tmp_sm2._kg(bar_x2, RB)
        # h = math.floor((p**0.5+1)**2/n)

        ptsum = sm2genkey.add([int(pb[0:len(pb)//2], 16), int(pb[len(pb)//2:], 16)],
                            [int(x2RB[0:len(x2RB)//2], 16), int(x2RB[len(x2RB)//2:], 16)], a, p)

        U = tmp_sm2._kg(tA*h, hex(ptsum[0])[2:]+hex(ptsum[1])[2:])
        Ubit = bin(int(U[0:len(U)//2], 16))[2:] + bin(int(U[len(U)//2:], 16))[2:]
        Ubit = Ubit.zfill(512)

        # assert len(U) == 128 and len(V) == 128

        sm2a = sm2.CryptSM2(da, pa)
        sm2b = sm2.CryptSM2(db, pb)
        # ZA、ZB是事先都知道的
        ZA = sm2a._sm3_z(b'')
        ZB = sm2b._sm3_z(b'')
        # print(ZA, len(ZA))
        # print(ZB, len(ZB))

        # print("len vbit:", len(Vbit))
        # print("len ZA:", len(bin(int(ZA, 16))[2:]))
        # print("len ZB:", len(bin(int(ZB, 16))[2:]))
        zb = Vbit+bin(int(ZA, 16))[2:].zfill(256)+bin(int(ZB, 16))[2:].zfill(256)
        # print("len Zb:", len(zb))
        klen = 16
        # print(zb.encode('utf8').decode('utf8'))
        # print("len zb: ", len(zb))
        # KB是B的KDF
        KB = sm3.sm3_kdf(zb.encode('utf8'), klen)
        # print(KB, len(KB))

        za = Ubit+bin(int(ZA, 16))[2:].zfill(256)+bin(int(ZB, 16))[2:].zfill(256)
        # print("len za", len(za))

        klen = 16
        # print(zb)
        # KA是A的KDF，哈希之后发给B
        KA = sm3.sm3_kdf(za.encode('utf8'), klen)
        hash_KA = sm3.sm3_hash(bytearray.fromhex(KA))
        # print(KA, len(KA))

        # assert sm3.sm3_hash(bytearray.fromhex(
        #     KA)) == sm3.sm3_hash(bytearray.fromhex(KB))
        # assert KA == KB
        if KA != KB:
            cnt += 1

    print(cnt)

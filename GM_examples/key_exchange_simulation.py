from GM.key_exchange_methods import GenR, GenSymKey, ComputeXBar,ComputeT,ComputeFinalPoint
import GM.constant
from GM.constant import ZA, ZB

# Init priv key and pub key in client and server
privA = GM.constant.da
pubA = GM.constant.pa
pubB_c = GM.constant.pb
privB = GM.constant.db
pubB = GM.constant.pb
pubA_s = GM.constant.pa

# Client Generate RA and send to server
RA,rA = GenR()
# client.send(RA)

# Server get RA and Generate RB, rb, sending to client
RB, rB = GenR()
# server.send(RB)

# Client compute bar_x1_c, bar_x2_c
bar_x1_c = ComputeXBar(RA)
tA = ComputeT(privA, bar_x1_c, rA)
bar_x2_c = ComputeXBar(RB)
U = ComputeFinalPoint(tA, bar_x2_c, RB, pubB_c)
symkey_c = GenSymKey(U, ZA, ZB)
# client.send(hash(KDF))

# server get hash(KDF) and compute its own KDF, and check if they're same
bar_x2_s = ComputeXBar(RB)
tB = ComputeT(privB, bar_x2_s, rB)
bar_x1_s = ComputeXBar(RA)
V = ComputeFinalPoint(tB, bar_x1_s, RA, pubA_s)
symkey_s = GenSymKey(V, ZA, ZB)

assert symkey_c == symkey_s
print("succeed")

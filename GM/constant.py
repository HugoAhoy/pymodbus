from gmssl import sm2

# private key for server(db) and client(da)
da ='7098f9d29c01573aa5ad12717bf998f0b36fe6dc30138feea03e764077a4a34b'
db = '7fffe3487d53b50906d4db005e033ed78ac6fc9de93537aae27e30eccdf68f1a'

# public key for server(pb) and client(pa)
pa = 'd7ba85bbf9748bc1f4c92d1345b7a9f8a5d3a9d1aa155f37115dc960005e60c8fe8cbdd7d9271c5501f8187eb5c5398ed5b19f523b9c6434fc3a7498f61cb800'
pb = 'a3e8fc7c41c736fad165d0605478a8767a967ad2574da188e52d6cbb5acac10853fce1b765fa8c9a0b6c7efd12f6e6cef0d187d327260260ac9f47d93b3f3155'

# eclipse parameter ZA, ZB
sm2a = sm2.CryptSM2(da, pa)
sm2b = sm2.CryptSM2(db, pb)

ZA = sm2a._sm3_z(b'')
ZB = sm2b._sm3_z(b'')
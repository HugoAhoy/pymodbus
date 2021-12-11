from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

crypt_sm4 = CryptSM4()

key = bytes.fromhex('ea28bfe51f2aabb641e69e7f93ffd3ed')

crypt_sm4.set_key(key, SM4_ENCRYPT)
value = b'bjkgbhfvgfyhjkgvyukfyjhgbh,jgvykjhfyudcythf' #  bytes类型
print(value)
print(len(value))
encrypt_value = crypt_sm4.crypt_ecb(value) #  bytes类型
print(encrypt_value)
print(len(encrypt_value))
crypt_sm4.set_key(key, SM4_DECRYPT)
decrypt_value = crypt_sm4.crypt_ecb(encrypt_value) #  bytes类型
print(decrypt_value)
print(len(decrypt_value))
assert value == decrypt_value

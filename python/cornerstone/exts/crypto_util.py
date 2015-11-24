# coding: utf-8
import hashlib
import hmac
from Crypto.Cipher import AES
import os
import binascii


def encrypt_bytes(data, aes_iv, aes_key, hmac_key1, hmac_key2):
    # /
    raw_bytes = data

    # /
    raw_bytes_hash = hmac.new(
        hmac_key1,
        raw_bytes,
        hashlib.sha1
    ).digest()

    # /
    raw_and_hash = raw_bytes + raw_bytes_hash

    # /
    raw_and_hash_len = len(raw_and_hash)

    # /
    aes_block_size = 16

    aes_block_size_remainder = raw_and_hash_len % aes_block_size

    if aes_block_size_remainder == 0:
        data_and_hash_and_pad = raw_and_hash
    else:
        pad_bytes_count = aes_block_size - aes_block_size_remainder

        pad_bytes = os.urandom(pad_bytes_count)

        data_and_hash_and_pad = raw_and_hash + pad_bytes

    # /
    aes_obj = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    cry_bytes = aes_obj.encrypt(data_and_hash_and_pad)

    # /
    cry_bytes_hash = hmac.new(
        hmac_key2,
        cry_bytes,
        hashlib.sha1
    ).digest()

    # /
    cry_and_hash = cry_bytes + cry_bytes_hash

    # /
    return cry_and_hash


def decrypt_bytes(data, raw_len, aes_iv, aes_key, hmac_key1, hmac_key2):
    # /
    cry_and_hash = data
    # /
    cry_bytes_hash = cry_and_hash[-20:]

    cry_bytes = cry_and_hash[:-20]

    # /
    cry_bytes_hash_new = hmac.new(
        hmac_key2,
        cry_bytes,
        hashlib.sha1
    ).digest()

    if cry_bytes_hash_new != cry_bytes_hash:
        raise ValueError(data)

    # /
    aes_obj = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    raw_and_hash_and_pad = aes_obj.decrypt(cry_bytes)

    # /
    hash_len = 20

    raw_and_hash_len = raw_len + hash_len

    # /
    aes_block_size = 16

    aes_block_size_remainder = raw_and_hash_len % aes_block_size

    # /
    if aes_block_size_remainder == 0:
        pad_bytes_count = 0
    else:
        pad_bytes_count = aes_block_size - aes_block_size_remainder

    # /
    if pad_bytes_count == 0:
        raw_and_hash = raw_and_hash_and_pad
    else:
        raw_and_hash = raw_and_hash_and_pad[:-pad_bytes_count]

    # /
    raw_bytes = raw_and_hash[:raw_len]

    # /
    raw_bytes_hash = raw_and_hash[-hash_len:]

    # /
    raw_bytes_hash_new = hmac.new(
        hmac_key1,
        raw_bytes,
        hashlib.sha1
    ).digest()

    if raw_bytes_hash_new != raw_bytes_hash:
        raise ValueError(data)

    # /
    return raw_bytes


if __name__ == '__main__':
    # /
    # str and byte problem look：http://www.tuicool.com/articles/2MVRVv7
    aes_iv = 'a' * 16
    print(type(aes_iv))
    aes_iv = aes_iv.encode(encoding="utf-8")
    assert len(aes_iv) == 16

    aes_key = 'b' * 32
    aes_key = aes_key.encode(encoding="utf-8")
    assert len(aes_key) == 32

    hmac_key1 = 'c' * 48
    hmac_key1 = hmac_key1.encode(encoding="utf-8")

    assert len(hmac_key1) == 48

    hmac_key2 = 'd' * 48
    hmac_key2 = hmac_key2.encode(encoding="utf-8")
    assert len(hmac_key2) == 48

    # /
    input = 'test'.encode(encoding="utf-8")

    print(input)

    input_len = len(input)

    output = encrypt_bytes(
        data=input,
        aes_iv=aes_iv,
        aes_key=aes_key,
        hmac_key1=hmac_key1,
        hmac_key2=hmac_key2,
    )

    print(output)
    a=binascii.hexlify(output)
    change =binascii.unhexlify(a)
    print(a)
    print(change)
    input_new = decrypt_bytes(
        data=change,
        raw_len=input_len,
        aes_iv=aes_iv,
        aes_key=aes_key,
        hmac_key1=hmac_key1,
        hmac_key2=hmac_key2,
    )

    print(input_new)

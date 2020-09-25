#!/usr/bin/python
#-*- coding: utf-8 -*-


# ********************************
#    FileName: encryption.py
#    Author  : ghostwwl
#    Email   : ghostwwl@gmail.com
#    Note    :
# ********************************


__author__ = "ghostwwl"

from Crypto.Cipher import AES
import base64

# AES KEY的长度：
# AES-128 --> 16
# AES-192 --> 24
# AES-256 --> 32


class AesEncrypt(object):
    """
    AES-128/CBC/PKCS7
    """
    def __init__(self, key, iv="6eec8d629eab468a"):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')
        self.key_preprocess()

    def key_preprocess(self):
        """
        处理 key 到 AES-128 的需要长度
        :return:
        """
        key_length = len(self.key)
        if key_length < 16:
            self.key = self.key + b'0' * (16 - key_length)
        else:
            self.key = self.key[:16]


    def pkcs7padding(self, text):
        """
        使用PKCS7填充
        :param text:   需要填充的文本
        :return:
        """
        bytes_length = len(text.encode('utf-8'))
        mod_num = bytes_length % 16
        if mod_num == 0:
            return text
        padding_length = 16 - mod_num
        return text + chr(padding_length) * padding_length

    def pkcs7unpadding(self, text):
        bytes_length = len(text.encode('utf-8'))
        mod_num = bytes_length % 16
        assert mod_num == 0
        padding_char = text[-1]
        padding_len = ord(padding_char)
        padding_str = text[-padding_len:]
        if padding_str == chr(padding_len) * padding_len:
            return text[:-padding_len]
        return text


    def encrypt(self, text):
        enc_str = AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(self.pkcs7padding(text).encode('utf-8'))
        return base64.b64encode(enc_str).decode('utf-8', 'ignore')

    def decrypt(self, content):
        dec_str = AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(base64.b64decode(content)).decode("utf-8", 'ignore')
        return self.pkcs7unpadding(dec_str)

if __name__ == '__main__':
    key = '123465'
    a = AesEncrypt(key)
    s = 'A0600^^华为手机*华为*苹果手机*手机5g*小米手机*手机自营*小米*oppo手机*vivo手机*苹果*oppo*vivo*荣耀*小米10*a'
    e = a.encrypt(s)
    d = a.decrypt(e)
    print("encrypt:", e)
    print("decrypt:", d)

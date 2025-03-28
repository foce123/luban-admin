# -*- coding: utf-8 -*- 
"""
========================================================================================================================
@Author: 孟颖
@email: 652044581@qq.com
@date: 2023/4/20 10:19
@desc: 加密解密模块
========================================================================================================================
"""

import base64
import hashlib


class HashCipher:

    @staticmethod
    def md5(message):
        """
        Returns the MD5 hash of the message
        """
        return hashlib.md5(message.encode()).hexdigest()

    @staticmethod
    def sha1(message):
        """
        Returns the SHA1 hash of the message
        """
        return hashlib.sha1(message.encode()).hexdigest()

    @staticmethod
    def sha256(message):
        """
        Returns the SHA256 hash of the message
        """
        return hashlib.sha256(message.encode()).hexdigest()

    @staticmethod
    def sha512(message):
        """
        Returns the SHA512 hash of the message
        """
        return hashlib.sha512(message.encode()).hexdigest()


class Base64Cipher:
    @staticmethod
    def bytes_to_base64(bytes_data):
        """
        Converts bytes to base64 string
        """
        return base64.b64encode(bytes_data).decode('utf-8')

    @staticmethod
    def base64_to_bytes(base64_string):
        """
        Converts base64 string to bytes
        """
        return base64.b64decode(base64_string.encode('utf-8'))

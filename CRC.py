import random

from configReader import ConfigReader


class CRC:

    def __init__(self):
        self.cdw = ''

    def xor(self, a, b):
        result = []
        for i in range(0, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')

        return ''.join(result)

    def crcXor(self, a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')

        return ''.join(result)

    def crc(self, message, key):
        pick = len(key)

        tmp = message[:pick]

        while pick < len(message):
            if tmp[0] == '1':
                tmp = self.crcXor(key, tmp) + message[pick]
            else:
                tmp = self.crcXor('0' * pick, tmp) + message[pick]

            pick += 1

        if tmp[0] == "1":
            tmp = self.crcXor(key, tmp)
        else:
            tmp = self.crcXor('0' * pick, tmp)

        checkword = tmp
        return checkword

    def encodedData(self, data, key):
        l_key = len(key)
        append_data = data + '0' * (l_key - 1)
        remainder = self.crc(append_data, key)
        codeword = data + remainder
        self.cdw += codeword
        print("Remainder: ", remainder)
        print("Data: ", codeword)
        return codeword

    def checkError(self, data, key):
        r = self.crc(data, key)
        size = len(key)
        if r == (size - 1) * '0':
            return False, data[:len(data) - size + 1]
        else:
            return True, ""

from old_define import defineWord
from secrets import randbelow
import argparse
import re


symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"


def encrypt(text, action, key=None):
    if action:
        key = randbelow(72)
        if key == 0:
            key = 1
        print('[*] Encrypting...')
    else:
        key = key
    output = ""
    for letter in text:
        letterIndex = symbols.find(letter)
        if letterIndex == -1:
            output += letter
        else:
            letterIndex += key
            if letterIndex >= len(symbols):
                letterIndex -= len(symbols)
            elif letterIndex < 0:
                letterIndex += len(symbols)
            output += symbols[letterIndex]
    if action:
        print(output)
    return output


def decrypt(text, action):
    print('[*] Decrypting...')
    samples = {}
    output = []
    followup_keys = []
    max_keys = len(symbols)
    rx = re.compile('[^a-zA-Z]')
    print('[*] Building list of potential matches...')
    for key in range(1, max_keys + 1):
        samples[key] = [i for i in encrypt(text, action, key=key).split(' ')]
    for (k, v) in samples.items():
        w = rx.sub('', v[0])
        if len(w) >= len(v[0]) - 1:
            if defineWord(w):
                followup_keys.append(k)
    for i in followup_keys:
        output.append(encrypt(text, action, key=i))
    print('[!] Likely matches include the following:')
    print(*output, sep='\n')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text to or from Caesar.')
    parser.add_argument('-d',
                        '--decrypt',
                        action='store_false',
                        help='Decrypt flag; decrypt Caesar text.')
    parser.add_argument('text',
                        nargs='*',
                        action='store',
                        help='Text to encrypt or decrypt to/from Caesar.')
    args = parser.parse_args()
    action = args.decrypt
    text = ' '.join(args.text)
    if action:
        encrypt(text, action)
    else:
        decrypt(text, action)

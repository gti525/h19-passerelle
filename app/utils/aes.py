from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ENCRYPTION_KEY = "Buenos933-accole".encode("utf-8")
cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_KEY)


def encrypt(text):
    text = text.encode("utf-8")
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_KEY)

    ct_bytes = cipher.encrypt(pad(text, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')

    return ct


def decrypt(text):
    try:
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_KEY)
        ct = b64decode(text)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode("utf-8")
    except ValueError:
        print("Incorrect decryption")


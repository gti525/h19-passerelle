from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging

logger = logging.getLogger(__name__)

ENCRYPTION_KEY = "Buenos933-accole".encode("utf-8")
cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_KEY)


def encrypt(text):
    text = str(text).encode("utf-8")
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_KEY)

    ct_bytes = cipher.encrypt(pad(text, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')

    return ct


def decrypt(text):
    try:
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_KEY)
        ct = b64decode(text)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        if is_number(pt):
            return int(pt)
        else:
            return pt.decode("utf-8")
    except ValueError as e:
        logger.error("Incorrect decryption {}".format(str(e)))
    except Exception:
        logger.error("Incorrect decryption. {}".format(str(e)))


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes



TEXT = bytes("jyrgtnutnyutr jtyetrt ",encoding="utf-8")
SECRET_KEY = bytes("Buenos933-accole",encoding="utf-8")
IV = bytes("Buenos933-accole",encoding="utf-8")
cipher = AES.new(SECRET_KEY, AES.MODE_CBC,IV)
ct_bytes = cipher.encrypt(pad(TEXT, AES.block_size))
#iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
#result = json.dumps({'iv':iv, 'ciphertext':ct})
print("enrypted text: {}".format(ct))



import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
# We assume that the key was securely shared beforehand
try:

    ct = b64decode(ct)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", str(pt.decode("utf-8")))
except ValueError:
    print("Incorrect decryption")

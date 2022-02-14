import math
import random, string, base64
def encrypt(email):
    maxvar = 0
    for x in range(0, len(email)):
        if ord(email[x]) > maxvar:
            maxvar = ord(email[x])
    l = []
    for x in range(0, len(email)):
        l.append(ord(email[x]) / maxvar)
    l.append(0.639 + float("0." + str(maxvar) + str(random.randint(35835693, 95824689)) + str(len(str(maxvar)))))
    #print(l)
    return l

def decrypt(l):
    factor =  10 **int(str(l[len(l) - 1])[-1])
    #print(factor)
    val = float(l[len(l) - 1]) - 0.639
    maxvar = int(val * factor)
    #print(maxvar)
    decrypted = ""
    for x in range(0, (len(l) - 1)):
        if ((float(l[x]) * maxvar) - int(float(l[x]) * maxvar)) > 0.5:
            decrypted = decrypted + chr(math.ceil(float(l[x]) * maxvar))
        else:
            decrypted = decrypted + chr(math.floor(float(l[x]) * maxvar))
    return decrypted

def encryption(text):
    fvar = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase + '!@#$&', k = 15))
    svar = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase + '!@#$&', k = 15))
    text = fvar+text+svar
    enc = base64.b64encode(bytes(text, 'utf-8'))
    return enc

def decryption(enc):
    dec = str(base64.b64decode(enc))
    dec = dec[17:].replace(dec[-16:],'')
    return dec
#e = encryption("shivankawasthi")
#print(e)
#d = decryption(e)
#print(d)

#This file was created for testing purposes
from passlib.hash import pbkdf2_sha256
import Email_encrypt_decrypt, os
import platform

def new_user():
    #to fix Linux / Mac OS compatibility issue 
    global path
    path = ""
    if(platform.system() == 'Windows'):
        path = os.environ['APPDATA']
    elif(platform.system() == 'Linux'):
        path = os.path.expanduser("~") + os.sep + ".local" + os.sep + "share" + os.sep
    try:
        os.mkdir(path+"\\IIDS")
        new_user()
    except FileExistsError:
        pass
    fo = open(path+"\\IIDS\\u001.iidsfile", "w")
    fo.write(pbkdf2_sha256.encrypt("root", rounds = 2000000, salt_size = 16))
    fo.close()
    fo = open(path+"\\IIDS\\u002.iidsfile", "w")
    fo.write(pbkdf2_sha256.encrypt("toor", rounds = 2000000, salt_size = 16))
    fo.close()
    fo = open(path+"\\IIDS\\u003.iidsfile", "w")
    l = Email_encrypt_decrypt.encrypt(" ")
    for item in l:
        fo.write("%s\n" % item)
    fo.close()
    fo = open(path+"\\IIDS\\u004.txt","w")
    fo.write("1")
    fo.close()
    return "success"

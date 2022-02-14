# this is the backend of IIDS
import sqlite3
from datetime import datetime as dt
import base64
import platform
from emailsend import emailsend
import os
from Email_encrypt_decrypt import encryption, decryption,decrypt


def connect():
    #to fix Linux / Mac OS compatibility issue
    global path
    path = ""
    if(platform.system() == 'Windows'):
        path = os.environ['APPDATA']
    elif(platform.system() == 'Linux'):
        path = os.path.expanduser("~") + os.sep + ".local" + os.sep + "share" + os.sep
    try:
        os.mkdir(path+"\\IIDS")
    except FileExistsError:
        pass
    conn = sqlite3.connect(path+"\\IIDS\\syslogs.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS syslogs(date_time TEXT PRIMARY KEY, message TEXT, priority TEXT)")
    conn.commit()
    conn.close()

def add_activity(date_time, message, priority):
    connect()
    conn = sqlite3.connect(path+"\\IIDS\\syslogs.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO syslogs VALUES(?,?,?)",(encryption(date_time),encryption(message),priority))
    conn.commit()
    conn.close()

def find_activity(priority):
    #altered this function so that it goes well with forntend
    msg = []
    connect()
    conn = sqlite3.connect(path+"\\IIDS\\syslogs.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM syslogs WHERE priority=?",(priority,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    msg = decode(rows)
    return msg



def decode(rows):
    #altered this function so that it goes well with forntend
    message = []
    for row in rows:
        message.append(decryption(row[0]))
        message.append(decryption(row[1]))
        #print(str(base64.b64decode(row[0])))
        #print(str(base64.b64decode(row[1])))
    return message


def find_activity_interface():
    #altered this function so that it goes well with forntend
    finalMessage1 = []
    finalMessage2 = []
    #print("High priority events")
    finalMessage1 = find_activity("high")
    finalMessage1.insert(0,"HIGH PRIORITY EVENTS!!")
    if(len(finalMessage1) == 1):
        finalMessage1.append("NONE!")
    #print("Low priority events")
    finalMessage2 = find_activity("low")
    finalMessage2.insert(0,"LOW PRIORITY EVENTS!!")
    if(len(finalMessage2) == 1):
        finalMessage2.append("NONE!")
    return finalMessage1 + finalMessage2

def send_logs(priority):
    connect()
    conn = sqlite3.connect(path+"\\IIDS\\syslogs.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM syslogs WHERE priority=?",(priority,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    f = open(path+"\\IIDS\\logs.txt",'w')
    for row in rows:
        f.write(decryption(row[0]))
        f.write(decryption(row[1]))
        f.write("\n")
    f.close()
    lines = []
    with open(path+ "\\IIDS\\u003.iidsfile") as f:
        lines = f.read().splitlines()
    #fixed an issue that was caused by files created by bat file
    if(lines[len(lines) - 1] == "ECHO is off." or lines[len(lines) - 1] == " "):
        lines = lines[:len(lines) - 1]

    emailsend(decrypt(lines),
    "System logs!",
    "Your system just went offline. We are sending you current system logs. Please have a look asap.",
    path+"\\IIDS\\logs.txt")

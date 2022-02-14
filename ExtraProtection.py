import subprocess
import platform
import os
from CreateFiles import new_user

var1 = ""
var2 = ""
var3 = ""
def FindPath():
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
    return path


fo = open(FindPath()+"\\IIDS\\u001.iidsfile", "r")
var1 = fo.read()
fo.close()
fo = open(FindPath()+"\\IIDS\\u002.iidsfile", "r")
var2 = fo.read()
fo.close()
fo = open(FindPath()+"\\IIDS\\u003.iidsfile", "r")
var3 = fo.read()
fo.close()
var3 = var3.replace("\n", "\necho ")

try:
    os.mkdir(FindPath()+"\\BackgroundActivityManager")
except FileExistsError:
    pass

def DestroyProtection():
    if platform.system() == 'Windows':
        #added invisible execution mode for windows
        invisiblemodeFileContent = "CreateObject(\"Wscript.Shell\").Run \"\"\"\" & WScript.Arguments(0) & \"\"\"\", 0, False"
        fo = open(FindPath()+"\\BackgroundActivityManager\\WatchdogHelper.vbs", "w")
        fo.write(invisiblemodeFileContent)
        fo.close()
        Destroy = "taskkill /f /im cmd.exe /fi \"windowtitle eq YouCantDestroyMe\""
        fo = open(FindPath()+"\\BackgroundActivityManager\\Destructor.bat", "w")
        fo.write(Destroy)
        fo.close()
        os.system("wscript.exe " + FindPath() + "\\BackgroundActivityManager\\WatchdogHelper.vbs" + " " + FindPath()+"\\BackgroundActivityManager\\Destructor.bat")
        os.system("del " + FindPath() + "\\BackgroundActivityManager\\Destructor.bat")

def CreateAndInitialiseProtection():
    if platform.system() == 'Windows':
        #added invisible execution mode for windows
        invisiblemodeFileContent = "CreateObject(\"Wscript.Shell\").Run \"\"\"\" & WScript.Arguments(0) & \"\"\"\", 0, False"
        fo = open(FindPath()+"\\BackgroundActivityManager\\WatchdogHelper.vbs", "w")
        fo.write(invisiblemodeFileContent)
        fo.close()
        a = "@echo off\ntitle YouCantDestroyMe\n" + "attrib +h "+ FindPath() + "\\BackgroundActivityManager\n" + ":START\nif not exist "+FindPath()+"\\IIDS\\u001.iidsfile"+" ( echo "+ var1 +")>>" + FindPath() + "\\IIDS\\" +"u001.iidsfile"+"\nif not exist "+ FindPath() + "\\IIDS\\" + "u002.iidsfile"+ " ( echo " + var2 + ")>>" + FindPath() + "\\IIDS\\" +"u002.iidsfile" + "\nif not exist "+ FindPath() + "\\IIDS\\" + "u003.iidsfile"+ " ( echo " + var3 + ")>>" + FindPath() + "\\IIDS\\" +"u003.iidsfile" + "\n goto START"
        fo = open(FindPath()+"\\BackgroundActivityManager\\Watchdog.bat", "w")
        fo.write(a)
        fo.close()
        #subprocess.Popen(FindPath() + "\\BackgroundActivityManager" +"\\Watchdog.bat")
        os.system("wscript.exe " + FindPath() + "\\BackgroundActivityManager\\WatchdogHelper.vbs" + " " + FindPath()+"\\BackgroundActivityManager\\Watchdog.bat")
    #need to fix some issues with this part
    if platform.system() == 'Linux':
        a = "#!/bin/sh\nwhile true\ndo\nif [ ! -f "+ FindPath()+ "\\IIDS\\u001.iidsfile" +" ]\nthen\n" + "echo "+ var1 + " >> " + FindPath()+ "\\IIDS\\u001.iidsfile" +"\nfi" + "\nif [ ! -f "+ FindPath()+ "\\IIDS\\u002.iidsfile" +" ]\nthen\n" + "echo " + var2 + " >> " + FindPath() + "\\IIDS\\u002.iidsfile" + "\nfi" + "\nif [ ! -f "+ FindPath()+ "\\IIDS\\u003.iidsfile" +" ]\nthen\n" + "echo " + var3[:len(var3)] + "\nfi" + "\ndone"
        fo = open(FindPath()+"BackgroundActivityManagerWatchdog.sh", "w")
        fo.write(a)
        fo.close()
        os.system('chmod +x ' + FindPath() + "BackgroundActivityManager" +"Watchdog.sh")
        subprocess.Popen(FindPath() + "BackgroundActivityManager" +"Watchdog.sh")

import sys
import subprocess
from subprocess import Popen
from time import sleep

ADB_LOCATION = "./adb"
PHOTO_DIRECTORY = "/Users/scott/Documents/"

phone_ip_addresses = [
                        ["0","LMG710V41a9c9df"],
                        ["1","LMG710V7fbd8155"],
                        ["2","LMG710V86da3a0f"],
                        ["3","LMG710V6e9a6bb9"],
                        ["4","LMG710V307febb1"],
                        ["5","LMG710Ve2e9bcd9"],
                        ["6","LMG710Va67982ad"],
                        ["7","LMG710V5d1751ea"],
                        ["8","LMG710V8ef5f579"],
                        ["9","LMG710V70cde984"],
                        ["10","LMG710V769e1053"],
                        ["11","LMG710V750d9b8e"],
                        ["12","LMG710V6f6e8737"],
                        ["13","LMG710V5f09db80"],
                        ["14","LMG710V8df5fb04"],
                        ["15","LMG710Vdc87a2df"],
                        ["16","LMG710V5327ea38"],
                        ["17","LMG710Vef4ab08b"],
                        ["18","LMG710Ve504e7d0"],
                        ["19","LMG710Vac529a8a"],
                        ["20","LMG710Vdfc6f579"],
                        ["21","LMG710V36923c69"],
                        ["22","LMG710Vb785d370"],
                        ["23","LMG710V2c62c29c"]
                     ]

def sendImageCaptureCommandToAllPhones():
    commands = []
    for i in range(len(phone_ip_addresses)):
        phone_ip_address = phone_ip_addresses[i][1]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + ' shell am start -a android.media.action.IMAGE_CAPTURE')
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(3)

def sendTakePhotoCommandToAllPhones():
    commands = []
    for i in range(len(phone_ip_addresses)):
        phone_ip_address = phone_ip_addresses[i][1]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + ' shell input keyevent 27')
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(3)

def sendImageDeleteCommandToAllPhones():
    commands = []
    for i in range(len(phone_ip_addresses)):
        phone_ip_address = phone_ip_addresses[i][1]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + " shell rm -r /sdcard/DCIM/Camera/*")
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

def sendImageRenameCommandToAllPhones():
    commands = []
    for i in range(len(phone_ip_addresses)):
        phone_common_number = phone_ip_addresses[i][0]
        phone_ip_address = phone_ip_addresses[i][1]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + " shell mv /sdcard/DCIM/Camera/* /sdcard/DCIM/Camera/" + phone_common_number + "_" + phone_ip_address + ".jpg")
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(1)

def sendPullCommandToAllPhones():
    commands = []
    for i in range(len(phone_ip_addresses)):
        phone_ip_address = phone_ip_addresses[i][1]
        tempCommand = ADB_LOCATION + " -s " + phone_ip_address + " pull /sdcard/DCIM/Camera/" + phone_ip_addresses[i][0] + "_" + phone_ip_address + ".jpg " + PHOTO_DIRECTORY + phone_ip_addresses[i][0] + "_" + phone_ip_address + ".jpg "
        print(tempCommand)
        commands.append(tempCommand)
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

def pull():
    #scp scott@192.168.1.238:/sdcard/DCIM/Camera/0.jpg /users/scott/documents
    for i in range(len(phone_ip_addresses)):
        phone_ip_address = phone_ip_addresses[i][1]
        subprocess.Popen(ADB_LOCATION + " -s " + phone_ip_address + " shell scp scott@192.168.1.238:/sdcard/DCIM/Camera/" + phone_ip_addresses[i][0] + "_" + phone_ip_addresses[i][1] + ".jpg /users/scott/documents", shell=True)
        sleep(3)

def sendBrightnessToggle():
    for j in range(2):
        command = ""
        if j == 0:
            command = "shell input keyevent 220"
        elif j == 1:
            command = "shell input keyevent 221"
        commands = []
        for i in range(len(phone_ip_addresses)):
            phone_common_number = phone_ip_addresses[i][0]
            phone_ip_address = phone_ip_addresses[i][1]
            commands.append(ADB_LOCATION + " -s " + phone_ip_address + " " + command)
        procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
        for p in procs:
            p.wait()

def sendHybernationCommand():
    for j in range(10):
        commands = []
        for i in range(len(phone_ip_addresses)):
            phone_common_number = phone_ip_addresses[i][0]
            phone_ip_address = phone_ip_addresses[i][1]
            commands.append(ADB_LOCATION + " -s " + phone_ip_address + " shell input keyevent 220")
        procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
        for p in procs:
            p.wait()

def sendAwakeningCommand():
    for j in range(10):
        commands = []
        for i in range(len(phone_ip_addresses)):
            phone_common_number = phone_ip_addresses[i][0]
            phone_ip_address = phone_ip_addresses[i][1]
            commands.append(ADB_LOCATION + " -s " + phone_ip_address + " shell input keyevent 221")
        procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
        for p in procs:
            p.wait()

def sendHomeCommandToAllPhones():
        commands = []
        for i in range(len(phone_ip_addresses)):
            phone_common_number = phone_ip_addresses[i][0]
            phone_ip_address = phone_ip_addresses[i][1]
            commands.append(ADB_LOCATION + " -s " + phone_ip_address + " shell input keyevent KEYCODE_HOME")
        procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
        for p in procs:
            p.wait()
        sleep(3)

if(len(sys.argv) > 1 and sys.argv[1] == "-c"):
    while(True):
        sendAwakeningCommand()
        sendHybernationCommand()

elif(len(sys.argv) > 1 and sys.argv[1] == "-p"):
    while(True):
        sendHybernationCommand()
        sendBrightnessToggle()
else:
    #sendImageDeleteCommandToAllPhones()
    #sendImageCaptureCommandToAllPhones()
    #sendTakePhotoCommandToAllPhones()
    #sendImageRenameCommandToAllPhones()
    #sendHomeCommandToAllPhones()
    sendPullCommandToAllPhones()
    #pull()


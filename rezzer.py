import sys
import subprocess
from subprocess import Popen
from time import sleep

ADB_LOCATION = "./adb"
PHOTO_DIRECTORY = "/Users/scott/Documents/"

phone_ip_addresses = [
                        ["0","LMG710V37620827"],
                        ["46","LMG710Vad26ccb8"]
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

def sendToAllPhones(command, delay):
    commands = []
    i=0
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + " " + command)
        i = i + 1
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        sleep(delay)
        p.wait()

def sendPullCommandToAllPhones():
    commands = []
    for i in range(len(phone_ip_addresses)):
        phone_ip_address = phone_ip_addresses[i][1]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + " pull /sdcard/DCIM/Camera " + PHOTO_DIRECTORY)
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

sendImageDeleteCommandToAllPhones()
sendImageCaptureCommandToAllPhones()
sendTakePhotoCommandToAllPhones()
sendImageRenameCommandToAllPhones()
sendPullCommandToAllPhones()
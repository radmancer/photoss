from ipaddress import ip_address
import sys
import subprocess
from subprocess import Popen
from time import sleep

#it is currently not known for why python 3 complains about the nmap library not existing if the program is run in picture taking mode.
#WARNING: this if statement is a hack and a long-term solution needs to be researched.
if(len(sys.argv) > 1 and sys.argv[1] == "-c"):
    import nmap
    nm = nmap.PortScanner() 
    cidr2='192.168.1.1/24'


PHOTO_DIRECTORY = "/home/scott/Desktop"
ADB_LOCATION = "/usr/bin/adb"

#Array of phones connected to the Cox router.
# phone_ip_addresses = {
#                          ("0", "48:60:5F:2F:40:10", "unknown"):"192.168.0.198:5555",
#                          ("1", "48:60:5F:2E:F5:BF", "unknown"):"192.168.0.119:5555",
#                          ("2", "48:60:5F:2F:5B:47", "unknown"):"192.168.0.117:5555",
#                          ("3", "48:60:5F:2F:5B:44", "unknown"):"192.168.0.115:5555",
#                          ("4", "48:60:5F:2F:44:83", "unknown"):"192.168.0.125:5555",
#                          ("8", "48:60:5F:2F:4F:1B", "unknown"):"192.168.0.134:5555",
#                          ("12", "48:60:5F:2F:4F:1B", "unknown"):"192.168.0.220:5555",
#                          ("10", "48:60:5F:2F:2B:5B", "unknown"):"192.168.0.126:5555",
#                          ("13", "48:60:5F:2F:4F:52", "unknown"):"192.168.0.189:5555",
#                          ("6", "48:60:5F:2F:5B:4D", "unknown"):"192.168.0.124:5555",
#                          ("9", "48:60:5F:2F:2D:B0", "unknown"):"192.168.0.118:5555",
#                          ("7", "48:60:5F:2F:46:0E", "unknown"):"192.168.0.166:5555"
#                      }

#Array of phones connected to the Linksys router.
phone_ip_addresses = {
                         ("0", "48:60:5F:2F:40:10", "unknown"):"192.168.1.102:5555",
                         ("1", "48:60:5F:2E:F5:BF", "unknown"):"192.168.1.123:5555",
                         ("2", "48:60:5F:2F:29:F0", "unknown"):"192.168.1.126:5555",
                         ("3", "48:60:5F:2F:5B:44", "unknown"):"192.168.1.104:5555",
                         ("4", "48:60:5F:2F:5B:44", "unknown"):"192.168.1.117:5555",
                         ("5", "48:60:5F:2F:5B:47", "unknown"):"192.168.1.107:5555",
                         ("6", "48:60:5F:2F:5B:4D", "unknown"):"192.168.1.114:5555",
                         ("7", "48:60:5F:2F:46:0E", "unknown"):"192.168.1.100:5555",
                         ("8", "48:60:5F:2F:4F:1B", "unknown"):"192.168.1.113:5555",
                         ("9", "48:60:5F:2F:2D:B0", "unknown"):"192.168.1.112:5555",
                         ("10", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.127:5555",
                         ("11", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.115:5555",
                         ("12", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.135:5555",
                         ("13", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.118:5555",
                         ("14", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.125:5555",
                         ("15", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.101:5555",
                         ("16", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.143:5555",
                         ("17", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.120:5555",
                         ("18", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.103:5555",
                         ("19", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.116:5555",
                         ("20", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.122:5555",
                         ("21", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.142:5555",
                         ("22", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.119:5555",
                         ("23", "48:60:5F:2F:2B:5B", "unknown"):"192.168.1.138:5555"
                     }

def checkNewPhoneAgainstDictionary():
    temp_phone_ip_addresses = []
    for key, value in phone_ip_addresses.items():
        temp_phone_ip_addresses.append(phone_ip_addresses[(key[0], key[1], key[2])][:-5])
    
    a=nm.scan(hosts=cidr2, arguments='-sP') 

    android_ip_addresses = []

    for k,v in a['scan'].items(): 
        if str(v['status']['state']) == 'up':
            hostname = v['hostnames'][0]['name']
            if hostname[:7] == "android":
                android_ip_addresses.append(v['addresses']['ipv4'])
            
    print(set(android_ip_addresses) ^ set(temp_phone_ip_addresses))

commands = {
               "home": "shell input keyevent KEYCODE_HOME",
               "capture": "shell am start -a android.media.action.IMAGE_CAPTURE",
               "camera": "shell input keyevent KEYCODE_CAMERA",
               "disconnect": "disconnect",
               "usbmode": "usb",
               "tcpipreset" : "tcpip 5555",
               "devices" : "devices",
               "connect" : "connect ",
               "enter" : "shell input keyevent KEYCODE_ENTER",
               "brightdown" : "shell input keyevent 220",
               "brightup" : "shell input keyevent 221",
               "pull" : "pull /sdcard/DCIM/Camera " + PHOTO_DIRECTORY,
               "delete": "shell rm /sdcard/DCIM/Camera/*",
               "getmac" : "shell ip address show wlan0",
               "stayon" : "shell settings put global stay_on_while_plugged_in 3",
               "stayoff" : "shell settings put global stay_on_while_plugged_in 0",
               "awaken" : "shell input keyevent KEYCODE_HOME",
               "sleep" : "shell sleep 1",
               "kill" : "kill-server"
           }

def adb(command):
    subprocess.call(ADB_LOCATION + " " + command, shell=True)

def sendToAllPhones(command, delay):
    commands = []
    i=0
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + " " + command)
        i = i + 1
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(delay)

def reconnectAllPhones():
    for key, value in phone_ip_addresses.items():
        adb("connect " + phone_ip_addresses[(key[0], key[1], key[2])])

def sendImageRenameCommandToAllPhones():
    commands = []
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + " shell mv /sdcard/DCIM/Camera/* /sdcard/DCIM/Camera/" + phone_ip_address + "_" + key[1] + ".jpg")
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

def sendAwakenCommandToAllPhones():
    print("\n[YOUR PHONES ARE NOW BEING KEPT AWAKE] Press Ctrl + C to exit.\n")
    commands = []
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append("while true; do " + ADB_LOCATION + " -s " + phone_ip_address + " shell 'input keyevent KEYCODE_HOME && input keyevent 220 && input keyevent 221'; sleep 1; done")
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

def sendBrightnessCommandToAllPhones(command):
    for i in range(10):
        sendToAllPhones(command, 0.25)

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

def sendImageCaptureCommandToAllPhones():
    commands = []
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        #adb shell "am start -a android.media.action.IMAGE_CAPTURE" && \ sleep 1 && \ adb shell "input keyevent 27"
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + ' shell am start -a android.media.action.IMAGE_CAPTURE')
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(5)

def sendTakePhotoCommandToAllPhones():
    commands = []
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        #adb shell "am start -a android.media.action.IMAGE_CAPTURE" && \ sleep 1 && \ adb shell "input keyevent 27"
        commands.append(ADB_LOCATION + " -s " + phone_ip_address + ' shell input keyevent 27')
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(5)

#Main
while(True):
    if(len(sys.argv) > 1 and sys.argv[1] == "-c"):
        while(True):
            prompt = input("\nWhat do you wish to do?\n1 disconnect all devices.\n2 reconnect a device.\n3 reconnect all devices.\n4 awaken all phones.\n5 power conservation mode.\n6 check new phone ip against dictionary.\n0 exit.\n")
            subprocess.call("clear", shell=True)
            if(prompt == "1"):
                adb(commands["disconnect"])
                adb(commands["kill"])
            elif(prompt == "2"):
                phonemoniker = input("This is where you plug in the desired phone my lord.\nIN ORDER TO CONTINUE!!!!\nType any one of its common names like '12' or 'LG0000929669287' or 'LMG710V6f6e8737' ")
                phone_ip_address = ""
                for key, value in phone_ip_addresses.items():
                    if(phonemoniker == key[0]):
                        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
                    elif(phonemoniker == key[1]):
                        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
                    elif(phonemoniker == key[2]):
                        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
                print(phone_ip_address)
                adb(commands["connect"] + phone_ip_address)
                if(input("Connection successful? (y/n) ") == "n"):
                    adb(commands["disconnect"])
                    adb(commands["kill"])
                    input("You must have the desired phone attached via usb to continue. Press any key when ready.")
                    sleep(1)
                    adb(commands["usbmode"])
                    sleep(1)
                    adb(commands["tcpipreset"])
                    sleep(5)
                    adb(commands["connect"] + phone_ip_address)
                    reconnectAllPhones()
            elif(prompt == "3"):
                reconnectAllPhones()
                sendToAllPhones(commands["home"], 1)
                sendBrightnessCommandToAllPhones(commands["brightup"])
                sendAwakenCommandToAllPhones()
            elif(prompt == "4"):
                sendBrightnessCommandToAllPhones(commands["brightup"])
                sendAwakenCommandToAllPhones()
            elif(prompt == "5"):
                sendBrightnessCommandToAllPhones(commands["brightdown"])
                sendAwakenCommandToAllPhones()
            elif(prompt == "6"):
                checkNewPhoneAgainstDictionary()
            elif(prompt == "0"):
                exit(0)
            else:
                exit(1)

    elif(input("Take a photo now? (y/n)") == "y"):
        #sendBrightnessCommandToAllPhones(commands["brightup"])
        sendToAllPhones(commands["delete"], 1)
        sendToAllPhones(commands["home"], 1)
        print("Say cheese!")
        sleep(1)
        #sendToAllPhones(commands["capture"], 1)
        #sendToAllPhones(commands["sleep"], 1)
        #sendToAllPhones(commands["camera"], 1)
        sendImageCaptureCommandToAllPhones()
        sendTakePhotoCommandToAllPhones()
        sendImageRenameCommandToAllPhones()
        sendToAllPhones(commands["home"], 1)
        sendToAllPhones(commands["pull"], 0)
        sendBrightnessCommandToAllPhones(commands["brightdown"])
        sendAwakenCommandToAllPhones()
    else:
        exit(0)

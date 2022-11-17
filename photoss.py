from ipaddress import ip_address
import sys
import subprocess
from subprocess import Popen
from time import sleep
import sqlite3
import re

conn = sqlite3.connect('photoss.db')
cursor = conn.cursor()

"""#Cox#ssid:SETUP-DC9C#password:boast1432crumbs
                         ("10", "48:60:5F:2F:2B:5B", "LMG710V769e1053"):"192.168.0.126:5555",
                         ("12", "48:60:5F:2F:09:63", "LMG710V6f6e8737"):"192.168.0.220:5555",
                         ("13", "48:60:5F:2F:4F:52", "LMG710V5f09db80"):"192.168.0.189:5555"
                         ("7","",""):"192.168.1.145:5555"#crispy's phone
"""
"""#Linksys26737#ssid:zoob#password:zoobzoob
                         ("10", "48:60:5F:2F:2B:5B", "LMG710V769e1053"):"192.168.1.127:5555",
                         ("12", "48:60:5F:2F:09:63", "LMG710V6f6e8737"):"192.168.1.135:5555",
                         ("13", "48:60:5F:2F:4F:52", "LMG710V5f09db80"):"192.168.1.118:5555"
                         ("7","",""):"192.168.1.145:5555"#crispy's phone
"""
"""#NETGEAR#ssid:NETGEAR#password:empty string
                         ("10", "48:60:5F:2F:2B:5B", "LMG710V769e1053"):"192.168.1.5:5555",
                         ("12", "48:60:5F:2F:09:63", "LMG710V6f6e8737"):"192.168.1.2:5555",
                         ("13", "48:60:5F:2F:4F:52", "LMG710V5f09db80"):"192.168.1.3:5555"
"""

#The original set of phones, new phones could be added in the future.
#This datastructure is immediately loaded with an ip corresponding to the mac adddress seen in field 2.
phone_ip_addresses = {
                         ("0", "48:60:5F:2F:40:10", "unknown"):"192.168.1.102:5555",
                         ("1", "48:60:5F:2E:F5:BF", "unknown"):"192.168.1.123:5555",
                         ("2", "48:60:5F:2F:40:10", "LMG710V86da3a0f"):"192.168.1.126:5555",
                         ("3", "48:60:5F:2F:5B:44", "unknown"):"192.168.1.104:5555",
                         ("4", "48:60:5F:2F:5B:44", "unknown"):"192.168.1.117:5555",
                         ("6", "48:60:5F:2F:5B:4D", "unknown"):"192.168.1.114:5555",
                         ("8", "48:60:5F:2F:5B:4D", "unknown"):"192.168.1.118:5555"
                     }

commands = {
               "home": "shell input keyevent KEYCODE_HOME",
               "capture": "shell am start -a android.media.action.STILL_IMAGE_CAMERA",
               "camera": "shell input keyevent KEYCODE_CAMERA",
               "disconnect": "disconnect",
               "usbmode": "usb",
               "tcpipreset" : "tcpip 5555",
               "devices" : "devices",
               "connect" : "connect ",
               "enter" : "shell input keyevent KEYCODE_ENTER",
               "brightdown" : "shell input keyevent 220",
               "brightup" : "shell input keyevent 221",
               "pull" : "pull /sdcard/DCIM/Camera /Users/scott/Documents/",
               "delete": "shell rm /sdcard/DCIM/Camera/*",
               "getmac" : "shell ip address show wlan0"
           }

def refreshDictionary():
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        cursor.execute("SELECT ip_address FROM devices WHERE mac_address='" + key[1] + "'")
        phone_ip_addresses[(key[0], key[1], key[2])] = cursor.fetchone()[0]

def insertAll():
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        # Insert a row of data
        cursor.execute("INSERT INTO devices (slang_tag, mac_address, adb_device_name, ip_address) VALUES('" + key[0] + "','" + key[1] + "','" + key[2] + "','" + phone_ip_address + "')")
        # Save (commit) the changes
        conn.commit()

def selectAll():#[R]ead
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        cursor.execute("SELECT * FROM devices WHERE mac_address='" + key[1] + "'")
        print(cursor.fetchone())

def createTable():
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices (slang_tag TEXT, mac_address TEXT, adb_device_name TEXT, ip_address TEXT)''')
    # Save (commit) the changes
    conn.commit()

def clearAll():
    # Create table
    cursor.execute("DROP TABLE devices")
    # Save (commit) the changes
    conn.commit()

def adb(command):
    subprocess.call("./adb " + command, shell=True)
            
def updateDatabase(mac_address, ip_address):
    cursor.execute("UPDATE devices SET ip_address = '" + ip_address + "' WHERE mac_address = '" + mac_address + "'")
    # Save (commit) the changes
    conn.commit()
    print("Updated " + ip_address + "\n")
    # Insert a row of data
    #cursor.execute("INSERT INTO devices (mac_address, ip_address) VALUES('" + mac_address + "','" + ip_address + "')") 
    #single row returned
    #cursor.execute("SELECT ip_address FROM devices WHERE mac_address = '" + mac_address + "'")
    #print("Found your ip, sire: " + cursor.fetchone())
    #conn.close()

def getAllMacsAndIps(network_ip):
    ip_addresses = []
    mac_addresses = []
    output = subprocess.check_output("sudo nmap -sP " + network_ip + "/24", shell=True)
    output = output.split("\n")
    for i in range(len(output)):
        m = re.search("([0-9A-z][0-9A-z]:){5}[0-9A-z][0-9A-z]", output[i])
        if m != None:
            mac_addresses.append(m.group(0))
        n = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", output[i])
        if n != None:
            ip_addresses.append(n.group(0))

    if len(ip_addresses) > len(mac_addresses):
        print("More IPs listed than MAC addresses.\n")
        print(ip_addresses)
        print(mac_addresses)

    return (mac_addresses, ip_addresses)

    #commands = []
    #commands2 = []
    #stdout = []
    #i=0
    #j=0
    #for key, value in phone_ip_addresses.items():
    #    phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
    #    commands.append("./adb -s " + phone_ip_address + ' shell input text ".......DEVICE%sIP:%s' + phone_ip_address + '"')
    #    i = i + 1
    #procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    #for p in procs:
    #    p.wait()
    #for key, value in phone_ip_addresses.items():
    #    phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
    #    commands2.append("./adb -s " + phone_ip_address + ' shell "ip address show wlan0"')
    #    j = j + 1
#
    #procs = [ Popen(['/bin/bash', '-c', i], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in commands2 ]
    #for p in procs:
    #    p.wait()
    #    out, err = p.communicate()
    #    errcode = p.returncode
    #    stdout.append(out)
    #sleep(5)
    #mac_addresses = []
    #ip_addresses = []
    #for i in range(len(stdout)):
    #    m = re.search("link\/ether ([0-9A-z][0-9A-z]:){5}[0-9A-z][0-9A-z]", stdout[i])
    #    n = re.search("inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", stdout[i])
    #    mac_address = m.group(0)
    #    mac_address = mac_address.split()[1]
    #    ip_address = n.group(0)
    #    ip_address = ip_address.split()[1]
    #    mac_addresses.append(mac_address)
    #    ip_addresses.append(ip_address)
    #return (mac_addresses, ip_addresses)
    # wait for the process to terminate

def sendToAllPhones(command, delay):
    commands = []
    i=0
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append("./adb -s " + phone_ip_address + " " + command)
        i = i + 1
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()
    sleep(delay)

def reconnectAllPhones():
    for key, value in phone_ip_addresses.items():
        adb("connect " + phone_ip_addresses[(key[0], key[1], key[2])])

def showPhoneInfo():
    commands = []
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append("./adb -s " + phone_ip_address + ' shell input text "IP:' + phone_ip_address + 'MAC:' + key[1] + '"')
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

def sendBashCommandToAllPhones():
    commands = []
    for key, value in phone_ip_addresses.items():
        phone_ip_address = phone_ip_addresses[(key[0], key[1], key[2])]
        commands.append("./adb -s " + phone_ip_address + " shell mv /sdcard/DCIM/Camera/* /sdcard/DCIM/Camera/" + phone_ip_address + "_" + key[1] + ".jpg")
    procs = [ Popen(['/bin/bash', '-c', i]) for i in commands ]
    for p in procs:
        p.wait()

#Main
network_ip = "192.168.1.1"#linksys
#network_ip = "192.168.0.1"#cox

#macAndIps = getAllMacsAndIps(network_ip)
#macs = macAndIps[0]
#ips = macAndIps[1]
#for i in range(len(macs)):
#    updateDatabase(macs[i], ips[i])

#print("Updated the database my lord.\n")
#refreshDictionary()
#print("Updated local dictionary, good reading material...\n")
while(True):
    if(len(sys.argv) > 1 and sys.argv[1] == "-c"):
        while(True):
            input = raw_input("What do you wish to do, sire?\n1 disconnect all devices.\n2 reconnect a device.\n3 reconnect all devices\n4 power conservation mode. (turn screens down)\n5 update the data base with latest ip addresses.\n6 show phone info. \n7 select all from db.\n8 delete photos on all phones.\n9 create table\n0 exit program\n")
            if(input == "1"):
                adb(commands["disconnect"])
            elif(input == "2"):
                phonemoniker = raw_input("This is where you plug in the desired phone my lord.\nIN ORDER TO CONTINUE!!!!\nType any one of its common names like '12' or 'LG0000929669287' or 'LMG710V6f6e8737' ")
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
                if(raw_input("Connection successful? (y/n) ") == "n"):
                    adb(commands["disconnect"])
                    sleep(1)
                    adb(commands["usbmode"])
                    sleep(1)
                    raw_input("This is silly, but you must replug your phone in to continue. Press The Any Key to continue..")
                    sleep(1)
                    adb(commands["tcpipreset"])
                    sleep(5)
                    adb(commands["connect"] + phone_ip_address)
            elif(input == "3"):
                reconnectAllPhones()
                sendToAllPhones(commands["home"], 3)
                for i in range(10):
                    sendToAllPhones(commands["brightup"], 0.25)
                sendToAllPhones(commands["home"], 3)
            elif(input == "4"):
                for i in range(10):
                    sendToAllPhones(commands["brightdown"], 0.25)
                for i in range(10):
                    sendToAllPhones(commands["home"], 0)
            elif(input == "5"):
                macAndIps = getAllMacsAndIps(network_ip)
                macs = macAndIps[0]
                ips = macAndIps[1]
                for i in range(len(macs)):
                    updateDatabase(macs[i], ips[i])
                print("Updated the database my lord.\n")
                refreshDictionary()
                print("Updated local dictionary, good reading material...\n")
            elif(input == "6"):
                showPhoneInfo()
            elif(input == "7"):
                selectAll()
            elif(input == "8"):
                sendToAllPhones(commands["delete"], 5)
            elif(input == "9"):
                while(True):
                    sendToAllPhones(commands["brightup"], 0.25)
            elif(input == "0"):
                # We can also close the connection if we are done with it.
                # Just be sure any changes have been committed or they will be lost.
                conn.close()
                exit(0)
            else:
                # We can also close the connection if we are done with it.
                # Just be sure any changes have been committed or they will be lost.
                conn.close()
                exit(1)

            if(raw_input("Continue connecting devices? (y/n) ") == "n"):
                break

    elif(raw_input("Take a photo now? (y/n)") == "y"):
        #macAndIps = getAllMacsAndIps(network_ip)
        #macs = macAndIps[0]
        #ips = macAndIps[1]
        #for i in range(len(macs)):
            #updateDatabase(macs[i], ips[i])
        #refreshDictionary()
        sendToAllPhones(commands["delete"], 5)
        sendToAllPhones(commands["home"], 5)
        sendToAllPhones(commands["capture"], 5)
        sendToAllPhones(commands["camera"], 5)
        sendBashCommandToAllPhones()
        sleep(5)
        sendToAllPhones(commands["home"], 5)
        sendToAllPhones(commands["pull"], 0)
    else:
        exit(0)
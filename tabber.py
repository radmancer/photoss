import pyautogui
import subprocess
from subprocess import Popen
from time import sleep

#Array of phones connected to the Linksys router.
phone_ip_addresses = {
                         "0":"192.168.1.102:5000",
                         "1":"192.168.1.123:5000",
                         "2":"192.168.1.126:5000",
                         "3":"192.168.1.104:5000",
                         "4":"192.168.1.117:5000",
                         "5":"192.168.1.107:5000",
                         "6":"192.168.1.114:5000",
                         "7":"192.168.1.100:5000",
                         "8":"192.168.1.113:5000",
                         "9":"192.168.1.112:5000",
                         "10":"192.168.1.127:5000",
                         "11":"192.168.1.115:5000",
                         "12":"192.168.1.135:5000",
                         "13":"192.168.1.118:5000",
                         "14":"192.168.1.125:5000",
                         "15":"192.168.1.101:5000",
                         "16":"192.168.1.143:5000",
                         "17":"192.168.1.120:5000",
                         "18":"192.168.1.103:5000",
                         "19":"192.168.1.116:5000",
                         "20":"192.168.1.122:5000",
                         "21":"192.168.1.142:5000",
                         "22":"192.168.1.119:5000",
                         "23":"192.168.1.118:5000"
                     }

subprocess.call("chromium-browser " + phone_ip_addresses["1"], shell=True)
#screenWidth, screenHeight = pyautogui.size()
#currentMouseX, currentMouseY = pyautogui.position()
#pyautogui.moveTo(100, 150)
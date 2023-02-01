# photoss
A python program that sends out image capture commands to n amount of Android phones.

As of Jan 30, 2023: The architecture has changed to include Python Flask servers on every phone.
Servers known as "Rezzers" (Rezzer.py)

A terminal needed to be installed called Termux. (last known best version: com.termux_118.apk)
The Termux API is needed in order to control each phones' hardware. (last known best version: com.termux.api_51.apk)
As for setting up Termux and its API, follow these references:
https://wiki.termux.com/wiki/Termux:API
(It is important to source both .apks from F-Droid, otherwise functionality may break)
In addition to installing the API, you must run the command "pkg install termux-api" in Termux.
You must also enable "Allow write system settings" for Termux:API
Once this is all setup, run these test commands to turn down the brightness of the phone to 0 and back to 255:
"termux-brightness 0"
"termux-brightness 255"
In order for Termux to read and write files in the Android file system, run this command: termux-setup-storage
Next, run these commands in Termux:
"pkg install root-repo"
"pkg update"
"pkg install python"
"mkdir Source"
"cd Source"
"python -m venv venv"
". ./venv/bin/activate"
"pip install flask"
"export FLASK_APP=rezzer.py"
'export FLASK_ENV=""'
'export FLASK_DEBUG=""'
"chmod 777 scp.sh"
"pkg install sshpass"
"pkg install openssh"
"python rezzer.py"

In addition to Termux and Rezzer.py, there is a special shell script called scp.sh that is responsible for uploading images
back to the host computer. Make sure this shell script is chmod 777'd so that the Flask program can run it as a subprocess.

The Flask Server should already be installed by running the commands above, but here is the original article that details how to setup Flask:
https://opensource.com/article/20/8/python-android-mobile

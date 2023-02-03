#connect phone to internet.
#Install Termux and Termux-api APKs.
#Run: termux-setup-storage
#cp /sdcard/Download/setup.sh /data/data/com.termux/files/home
#chmod 777 setup.sh
#./setup.sh
pkg update
pkg install termux-api
pkg install root-repo
pkg install openssh
pkg install sshpass
mkdir Source
cd Source
cp /sdcard/Download/rezzer.py /data/data/com.termux/files/home/Source
cp /sdcard/Download/scp.sh /data/data/com.termux/files/home/Source
cp /sdcard/Download/python.sh /data/data/com.termux/files/home/Source
chmod 777 python.sh
chmod 777 scp.sh
pkg install python
read -p "Run: pip install flask"
read -p "Connect to local network. Log into host, run: ssh scott@192.168.1.136"
read -p "Run: cd Source"
read -p "Run: python -m venv venv"
read -p "Run: . ./venv/bin/activate"
read -p "Run: export FLASK_APP=rezzer.py"
read -p 'Run: export FLASK_DEBUG=""'
read -p "Run: python rezzer.py"
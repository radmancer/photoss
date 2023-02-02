pkg install termux-api
termux-setup-storage
read -p "Enable 'Allow write system settings' for Termux:API [Press any key to continue]"
termux-setup-storage
pkg install root-repo
pkg update
pkg install openssh
mkdir Source
cd Source
cp /sdcard/Download/rezzer.py /data/data/com.termux/files/home/Source
cp /sdcard/Download/scp.sh /data/data/com.termux/files/home/Source
chmod 777 scp.sh
pkg install python
pip install flask
python -m venv venv
. ./venv/bin/activate
export FLASK_APP=rezzer.py
export FLASK_DEBUG=""
read -p "Setup complete, SSH into host machine once and press Ctrl+C [Press any key to continue]"
read -p "run: 'python rezzer.py' to start the server. [Press any key to continue]"
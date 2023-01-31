sshpass -p 'xgp15a2' scp 0.jpg scott@192.168.1.136:/Users/scott/Desktop
cp /sdcard/Download/post.py /data/data/com.termux/files/home/Source


cd Source
python -m venv venv
. ./venv/bin/activate
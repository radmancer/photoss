#Retail Password: L310MC570G
#Install Termux and Termux API on phone.
#On the phone, connect to The Internet.
#Switch to Termux on the phone.
#termux-setup-storage
#cp /sdcard/Download/setup.sh /data/data/com.termux/files/home
#chmod 777 setup.sh
#./setup.sh (run this script)
yes | pkg update
pkg install termux-api
termux-camera-photo -c 0 test.jpg & rm test.jpg
pkg install termux-auth
pkg install openssh
#grab ip address with ifconfig
whoami
passwd
#enter 'xgp15a2'
sshd
#pkg install termux-services
#!!!!Now connect back to zoob network
# -Still manually entering commands
# ifconfig
# -Find the ipaddress
# whoami
# -Find the username
# echo {unitnumber} > unit.id
# -from the host computer: run:
#ssh -p 8022 [username]@[ipaddress]
#exit from phone terminal: exit
#To place your public key on a new phone.
#ssh-copy-id -p 8022 [username]@[ipaddress]

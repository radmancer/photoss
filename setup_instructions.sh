#Install Termux and Termux API on phone.
#On the phone, connect to The Internet.
#Switch to Termux on the phone.
pkg update
pkg install termux-api
termux-camera-photo -c 0 test.jpg & rm test.jpg
pkg install termux-auth
pkg install openssh
#grab ip address with ifconfig
ifconfig
whoami
passwd
#enter 'xgp15a2'
sshd
#from the host computer: run:
ssh -p 8022 [username]@[ipaddress]
#exit from phone terminal: exit
#To place your public key on a new phone.
ssh-copy-id -p 8022 [username]@[ipaddress]

#!/bin/bash

# Define an array to hold all 50 IP addresses
declare -a ip_addresses=(
	"192.168.1.102"
	"192.168.1.123"
	"192.168.1.126"
	"192.168.1.104"
	"192.168.1.117"
	"192.168.1.107"
	"192.168.1.114"
	"192.168.1.100"
	"192.168.1.113"
	"192.168.1.112"
	"192.168.1.127"
	"192.168.1.115"
	"192.168.1.135"
	"192.168.1.118"
	"192.168.1.125"
	"192.168.1.101"
	"192.168.1.143"
	"192.168.1.120"
	"192.168.1.103"
	"192.168.1.116"
	"192.168.1.122"
	"192.168.1.142"
	"192.168.1.119"
	"192.168.1.118"
	# add remaining IP addresses here
)

declare -a ip_addresses=(
	"192.168.1.113 u0_a237 6"
	"192.168.1.118 u0_a235 13"
	"192.168.1.122 u0_a234 20"
	"192.168.1.121 u0_a234 24"
	"192.168.1.142 u0_a235 25"
	"192.168.1.139 u0_a234 26"
)

# Define a function to run an ssh command on an Android phone
#function run_ssh_command {
	# $1 is the IP address of the Android phone
#	my_ip=$1
#	userid=$2
#	shift 2
#	eval "ssh -p 8022 $userid@$my_ip $@"
#}


function blast {
	filename="$1.jpg"
	# Loop through the IP addresses and launch 50 threads to run ssh commands
	for ip in "${ip_addresses[@]}"
	do
		my_ip=`echo $ip | awk '{print $1}'`
		my_username=`echo $ip | awk '{print $2}'`
		my_phoneid=`echo $ip | awk '{print $3}'`
		filepath="/data/data/com.termux/files/$my_phoneid.$filename"
		(ssh -p 8022 $my_username@$my_ip termux-camera-photo -c 0 $filepath) &
	done

	# Wait for all threads to complete
	wait

	# Loop through the IP addresses and launch 50 threads to run ssh commands
	for ip in "${ip_addresses[@]}"
	do
		my_ip=`echo $ip | awk '{print $1}'`
		my_username=`echo $ip | awk '{print $2}'`
		my_phoneid=`echo $ip | awk '{print $3}'`
		filepath="/data/data/com.termux/files/$my_phoneid.$filename"
		eval "scp -P 8022 $my_username@$my_ip:$filepath ./"
	done
}


filedir="/data/data/com.termux/files/"
blast $1


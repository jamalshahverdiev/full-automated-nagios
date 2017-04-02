#!/usr/bin/env python2.7
import subprocess
import sys
sys.path.insert(0, './lib')
from nagiossrvclivars import ipadd, nserver, password, enter, successfully, nrpe, nagios

print("")
print(' The program is going to install and configure the '+nagios+' '+nserver+' automatically.')
print(' It is supposed that you have already added all '+ipadd+' list of client hosts to the "clients.txt" file.')
print(' Users must be "root" with the same '+password+' on all hosts ...')
print("")
print("=====================================================================================")
print("")
print(' Firstly we must install/configure '+nagios+' '+nserver+' and secondly clients.')
print("")

choose = ""

while choose != "3":
    print("Choose one of following options:")
    print('1. To install and configure '+nagios+' '+nserver+', type "1" and press '+enter+'.')
    print('2. To install and configure '+nrpe+' agents to all client hosts, type "2" and press '+enter+'.')
    print('3. To exit type "3" and press '+enter+'.')
    print("")
    choose = raw_input("  Please choose the installation option: ")
    if choose == "1":
        subprocess.call("python2.7 nagios-server.py", shell=True)
        print("")
        print("")
    elif choose == "2":
        subprocess.call("python2.7 nagios-clients.py", shell=True)
        print(''+nrpe+' and necessary plugins '+successfully+' installed and configured on all servers!!!')
        print("")
        print("")
    elif choose == "3":
        sys.exit()
    else:
        print("  You can choose options, only '1','2' or '3' !!!")


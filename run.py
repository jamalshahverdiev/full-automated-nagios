#!/usr/bin/env python

import subprocess
import sys

print("")
print(" The program is going to install and configure the Nagios server automatically.")
print(" It is supposed that you have already added all IP addresses of client hosts to the 'clients.txt' file.")
print(" Users must be 'root' with the same passwords on all hosts ...")
print("")
print("=====================================================================================")
print("")
print(" Firstly we must install/configure Nagios server and secondly clients.")
print("")

choose = ""

while choose != "3":
    print("Choose one of following options:")
    print("1. To install and configure Nagios server, type 1 and press 'Enter'.")
    print("2. To install and configure 'Nrpe' agents to all client hosts, type 2 and press 'Enter'.")
    print("3. To exit type 3 and press 'Enter'.")
    print("")
    choose = raw_input("  Please choose the installation option: ")
    if choose == "1":
        subprocess.call("python nagios-server.py", shell=True)
        print("Nagios server successfully installed and configured!!!")
        print("")
        print("")
    elif choose == "2":
        subprocess.call("python nagios-clients.py", shell=True)
        print("Nrpe and necessary plugins successfully installed and configured on all servers!!!")
        print("")
        print("")
    elif choose == "3":
        sys.exit()
    else:
        print("  You can choose options, only '1','2' or '3' !!!")

